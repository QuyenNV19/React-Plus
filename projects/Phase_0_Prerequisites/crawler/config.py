from base_strategy import DeepCrawlStrategy

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
