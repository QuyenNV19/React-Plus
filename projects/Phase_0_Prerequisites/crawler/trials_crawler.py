import urllib.request
import urllib.error
import http.cookiejar
import time
import re
from urllib.parse import urljoin, urlparse, urldefrag
from bs4 import BeautifulSoup
from collections import deque
from abc import ABC, abstractmethod

class DeepCrawlStrategy(ABC):
    @abstractmethod
    def crawl(self, start_url, max_depth, max_pages, fetcher, same_domain_only) -> list[dict]:
        pass

    def _extract_links(self, html_content, base_url):
        links = []
        soup = BeautifulSoup(html_content, "html.parser")

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            full_url = urljoin(base_url, href)
            full_url, _ = urldefrag(full_url)

            parsed = urlparse(full_url)

            if parsed.scheme in {"http", "https"} and parsed.netloc:
                links.append(full_url)

        return links

    def _extract_info(self, html_content, url):
        soup = BeautifulSoup(html_content, "html.parser")

        products = []
        items = soup.find_all("div", class_="product-item")

        for item in items:
            try:
                a_tag = item.select_one("h3.product-title a")
                if not a_tag:
                    continue

                name = a_tag.get("title") or a_tag.get_text(strip=True)
                product_url = urljoin(url, a_tag["href"])

                # IMAGE
                img_tag = item.select_one("picture source")
                image_url = None
                if img_tag and img_tag.get("srcset"):
                    image_url = img_tag["srcset"]
                else:
                    img2 = item.select_one("img")
                    if img2:
                        image_url = img2.get("src")

                # PRICE
                price_tag = item.select_one("div.product-price span")
                price = int(re.sub(r"[^\d]", "", price_tag.text)) if price_tag else None

                # RATING
                rating_tag = item.select_one("div.rating-star-count")
                rating = float(rating_tag.text) if rating_tag else None

                # SOLD
                sold_tag = item.select_one("div.feature-sold")
                sold = int(re.sub(r"[^\d]", "", sold_tag.text)) if sold_tag else 0

                products.append({
                    "name": name,
                    "url": product_url,
                    "image_url": image_url,
                    "price": price,
                    "rating": rating,
                    "sold": sold,
                    "description": None,  # sẽ fill ở bước detail
                    "comments": None     # sẽ fill ở bước detail
                })

            except Exception:
                continue

        return products

    def _extract_details(self, html_content):
        """Trích xuất cả mô tả và bình luận trong một lần parse HTML"""
        soup = BeautifulSoup(html_content, "html.parser")
        description = None
        comments = None

        # --- 1. TRÍCH XUẤT MÔ TẢ ---
        main_content = soup.select_one("#content-product") or soup.select_one("#product-detail")
        if main_content:
            # Copy để không làm ảnh hưởng đến soup gốc khi decompose
            import copy
            content_copy = copy.copy(main_content)
            for comment_box in content_copy.select(".list-comment, .comment-list, .content-comment"):
                comment_box.decompose()
            description = content_copy.get_text(separator="\n", strip=True)
        else:
            selectors = ["div.product-description", "#description", ".product-content", ".pr-content"]
            for sel in selectors:
                desc_tag = soup.select_one(sel)
                if desc_tag:
                    parent_id = desc_tag.find_parent(id=True)
                    if parent_id and "comment" in parent_id.get("id", "").lower():
                        continue
                    description = desc_tag.get_text(separator="\n", strip=True)
                    break

        # --- 2. TRÍCH XUẤT BÌNH LUẬN (Lấy 3 cái đầu) ---
        item_selectors = [".item-comment", ".review-item", ".comment-item", ".comment-box"]
        comments_list = []
        
        # Thử tìm các item riêng lẻ trước
        for sel in item_selectors:
            items = soup.select(sel)
            if items:
                for item in items[:3]:  
                    comments_list.append(item.get_text(separator=" ", strip=True))
                break
        
        if comments_list:
            comments = "\n---\n".join(comments_list)
        else:
            # Fallback: Nếu không tìm thấy item riêng lẻ, tìm container và lấy text
            comment_selectors = [".list-comment", "#comment-list", ".review-list", ".customer-reviews", ".content-comment"]
            for sel in comment_selectors:
                comments_div = soup.select_one(sel)
                if comments_div:
                    comments = comments_div.get_text(separator="\n", strip=True)
                    break
        
        if not comments:
            content_divs = soup.select(".content")
            comments_texts = []
            for div in content_divs:
                classes = div.get("class", [])
                id_val = (div.get("id", "") or "").lower()
                if any(k in "".join(classes).lower() or k in id_val for k in ["comment", "review", "danh-gia"]):
                    text = div.get_text(separator="\n", strip=True)
                    if text:
                        comments_texts.append(text)
            if comments_texts:
                comments = "\n---\n".join(comments_texts[:3]) 

        return description, comments

class BFSDeepCrawlStrategy(DeepCrawlStrategy):
    def crawl(self, start_url, max_depth, max_pages, fetcher, same_domain_only):
        results = []
        visited = set()
        queue = deque([(start_url, 0)])
        initial_domain = urlparse(start_url).netloc

        product_map = {}  # url -> product

        while queue and len(results) < max_pages:
            url, depth = queue.popleft()

            if url in visited or depth > max_depth:
                continue

            visited.add(url)

            content = fetcher.fetch(url)
            if not content:
                continue

            # -------------------------
            # 1. LIST PAGE
            # -------------------------
            infos = self._extract_info(content, url)

            for p in infos:
                product_map[p["url"]] = p
                results.append(p)

            # -------------------------
            # 2. DETAIL PAGE (GET DESCRIPTION)
            # -------------------------
            for p in infos:
                time.sleep(1) # Delay between product detail requests
                detail_html = fetcher.fetch(p["url"])
                if detail_html:
                    p["description"], p["comments"] = self._extract_details(detail_html)

            # -------------------------
            # 3. CRAWL LINKS
            # -------------------------
            if depth < max_depth:
                for link in self._extract_links(content, url):
                    if link not in visited:
                        if not same_domain_only or urlparse(link).netloc == initial_domain:
                            queue.append((link, depth + 1))

        return results


class CrawlerRunConfig:
    def __init__(self, deep_crawl_strategy: DeepCrawlStrategy, max_depth=2, max_pages=50,
                 same_domain_only=True, timeout=10.0, headers=None):
        self.deep_crawl_strategy = deep_crawl_strategy
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.same_domain_only = same_domain_only
        self.timeout = timeout
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }


class PageFetcher:
    def __init__(self, headers=None, timeout=10):
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.timeout = timeout
        # Set up cookie handling to look more like a browser session
        self.cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))

    def fetch(self, url, retries=3, backoff=2):
        for attempt in range(retries):
            try:
                request = urllib.request.Request(url, headers=self.headers)
                with self.opener.open(request, timeout=self.timeout) as response:
                    if response.status == 200:
                        return response.read()
            except (urllib.error.URLError, ConnectionResetError) as error:
                reason = getattr(error, 'reason', error)
                print(f"[Retry {attempt + 1}/{retries}] {url} -> {reason}")
                if attempt < retries - 1:
                    time.sleep(backoff * (attempt + 1))
                else:
                    print(f"[URL Error] {url} -> {reason}")
            except Exception as error:
                print(f"[Fetch Error] {url} -> {error}")
                break
        return None

class WebCrawler:
    def run(self, url: str, config: CrawlerRunConfig) -> list[dict]:
        fetcher = PageFetcher(
            headers=config.headers,
            timeout=config.timeout
        )
        
        return config.deep_crawl_strategy.crawl(
            start_url=url,
            max_depth=config.max_depth,
            max_pages=config.max_pages,
            fetcher=fetcher,
            same_domain_only=config.same_domain_only
        )

if __name__ == "__main__":
    entry_url = "https://chiaki.vn/"

    bfs_strategy = BFSDeepCrawlStrategy()
    config = CrawlerRunConfig(
        deep_crawl_strategy=bfs_strategy,
        max_depth=1,
        max_pages=5,   # 🔥 lấy 5 sản phẩm
        same_domain_only=True
    )

    crawler = WebCrawler()

    print(f"\n--- ĐANG CRAWL {config.max_pages} SẢN PHẨM ---\n")

    results = crawler.run(entry_url, config)

    for i, p in enumerate(results, 1):
        print(f"\n[{i}] ------------------------")
        print(f"Tên        : {p.get('name')}")
        print(f"URL        : {p.get('url')}")
        print(f"Image      : {p.get('image_url')}")
        print(f"Giá        : {p.get('price')}")
        print(f" Rating     : {p.get('rating')}")
        print(f" Đã bán     : {p.get('sold')}")
        print(f" Mô tả      : {p.get('description')[:5000] if p.get('description') else None}...")
        print(f" Bình luận  : {p.get('comments')[:5000] if p.get('comments') else 'Không có bình luận'}...")
