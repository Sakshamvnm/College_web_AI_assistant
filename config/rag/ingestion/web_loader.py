import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse


class WebsiteLoader:

    def __init__(self):
        self.base_url = "https://www.academiacollege.edu.np"
        self.visited = set()

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                          "AppleWebKit/537.36 "
                          "Chrome/120 Safari/537.36"
        })

    def normalize_url(self, url):

        parsed = urlparse(url)

        # Remove fragments such as:
        # #navbarOffcanvas
        # #first-year
        # #second-year
        # #
        parsed = parsed._replace(fragment="")

        # Remove trailing slash except for homepage
        path = parsed.path

        if path != "/" and path.endswith("/"):
            path = path.rstrip("/")

        parsed = parsed._replace(path=path)

        return urlunparse(parsed)

    def is_valid_url(self, url):

        parsed = urlparse(url)
        base = urlparse(self.base_url)

        # Only Academia College
        if parsed.netloc != base.netloc:
            return False

        # Ignore URL fragments
        if parsed.fragment:
            return False

        # Ignore query parameters
        # This prevents:
        # ?page=1
        # ?page=2
        # ?category=...
        # ?sport=...
        if parsed.query:
            return False

        path = parsed.path.lower()

        # Ignore downloadable/non-HTML files
        ignored = (
            ".jpg", ".jpeg", ".png", ".gif",
            ".css", ".js", ".svg", ".ico",
            ".mp4", ".mp3", ".zip", ".rar",
            ".pdf", ".doc", ".docx", ".xls", ".xlsx",
            ".ppt", ".pptx"
        )

        if path.endswith(ignored):
            return False

        return True

    def load_page(self, url):

        try:

            print(f"Reading: {url}")

            response = self.session.get(
                url,
                timeout=20
            )

            response.raise_for_status()

            # Only process HTML pages
            content_type = response.headers.get(
                "Content-Type",
                ""
            ).lower()

            if "text/html" not in content_type:
                return "", []

            soup = BeautifulSoup(
                response.text,
                "lxml"
            )

            # Find links BEFORE removing tags
            links = []

            for a in soup.find_all("a", href=True):

                link = urljoin(url, a["href"])

                # Normalize URL
                link = self.normalize_url(link)

                if self.is_valid_url(link):
                    links.append(link)

            # Remove unnecessary content
            for tag in soup([
                "script",
                "style",
                "noscript",
                "nav",
                "footer",
                "header",
                "form"
            ]):
                tag.decompose()

            text = soup.get_text(
                "\n",
                strip=True
            )

            return text, links

        except Exception as e:

            print(f"Error reading {url}: {e}")

            return "", []

    def load_website(self, max_pages=50):

        documents = []

        queue = [self.normalize_url(self.base_url)]

        while queue and len(documents) < max_pages:

            url = queue.pop(0)

            url = self.normalize_url(url)

            if url in self.visited:
                continue

            self.visited.add(url)

            text, links = self.load_page(url)

            if text:

                documents.append({
                    "filename": f"website_{len(documents) + 1}",
                    "text": text,
                    "url": url,
                    "source_type": "website"
                })

            # Add new links
            for link in links:

                link = self.normalize_url(link)

                if (
                    link not in self.visited
                    and link not in queue
                    and self.is_valid_url(link)
                ):
                    queue.append(link)

        print()
        print("=" * 60)
        print(f"Website pages collected: {len(documents)}")
        print("=" * 60)

        return documents


if __name__ == "__main__":

    loader = WebsiteLoader()

    documents = loader.load_website(
        max_pages=50
    )

    print("\nFirst 3 pages:\n")

    for doc in documents[:3]:

        print("-" * 60)
        print("URL:", doc["url"])
        print("Text:", doc["text"][:500])