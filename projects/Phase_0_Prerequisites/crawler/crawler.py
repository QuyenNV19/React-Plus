from fetcher import PageFetcher
from config import CrawlerRunConfig

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
