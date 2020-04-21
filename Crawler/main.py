from collections import deque
from datetime import datetime
from pathlib import Path

from Crawler.Domain import get_domain_name, edit_url
from Crawler.Spider import *

MAX_COUNT = 3000
BASE_URL = "https://cs.uic.edu"
DOMAIN = "uic.edu"
BLACK_LIST = ['.gif', '.jpeg', '.jpg', '.ps', '.ppt', '.mp4',
              '.mp3', '.svg', 'mailto:', 'favicon', '.ico',
              '.css', '.apk', '.js', '.png', '.gif', '.pdf',
              '.doc', '@', 'tel']

PROJECT_PATH = 'CrawledData/' + str(datetime.now().strftime('%Y%m%d')) + "/"


class WebCrawler:
    def __init__(self, base_url):

        self.url_queue = deque()
        self.count = 0
        self.url_queue.append(base_url)
        self.crawled = set()
        Path(PROJECT_PATH).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def valid_link(url):
        # check domain and extension return ''if invalid. return link if valid
        if any(word in BLACK_LIST for word in url):
            return False
        elif DOMAIN != get_domain_name(url):
            # Filter out bad domains
            return False
        else:
            # Link Valid
            return True

    def get_links(self, html, url):
        links = scrape_links(html)
        relevant_links = set()
        for link in links:
            a_tag_text = link['href']
            if not any(bad_links in a_tag_text for bad_links in ['tel', 'mailto', '#']):
                a_url = edit_url(link['href'], url)
                if self.valid_link(a_url) and a_url not in self.crawled:
                    self.url_queue.append(a_url)
                    relevant_links.add(a_url)

    def run_scraper(self):
        while self.count < MAX_COUNT:
            target_link = self.url_queue.popleft()
            if target_link not in self.crawled:
                self.count += 1
                print("URL Scraping:", target_link)
                self.crawled.add(target_link)
                response = connect_page(target_link)
                if response is not None:
                    if response.status_code == requests.codes.ok:
                        print("Success: writing to file:", self.count)
                        self.get_links(response.text, response.url)
                        write_data_to_file(response.text, response.url, PROJECT_PATH + str(self.count))
                    else:
                        print("Response Failed")


if __name__ == '__main__':
    crawler = WebCrawler(BASE_URL)
    crawler.run_scraper()
