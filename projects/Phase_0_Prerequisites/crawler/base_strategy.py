import re
from urllib.parse import urljoin, urlparse, urldefrag
from bs4 import BeautifulSoup
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
            # Copy để không ảnh hưởng đến việc trích xuất comment sau này nếu chúng nằm trong main_content
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
                for item in items[:3]:  # Chỉ lấy 3 bình luận đầu tiên
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
                    # Nếu là container to, ta khó tách 3 cái nếu không có selector item. 
                    # Tạm thời lấy text nhưng giới hạn độ dài hoặc hy vọng fallback dưới tốt hơn.
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
                comments = "\n---\n".join(comments_texts[:3]) # Lấy 3 cái đầu

        return description, comments
