import urllib.request
import urllib.error
import http.cookiejar
import time

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
