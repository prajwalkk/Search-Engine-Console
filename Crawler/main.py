import logging
import time
from collections import deque
from datetime import datetime
from pathlib import Path

from Crawler.Domain import get_domain_name, edit_url
from Crawler.Spider import *

MAX_COUNT = 3000
BASE_URL = "https://cs.uic.edu/"
DOMAIN = "uic.edu"
BLACK_LIST = ['.gif', '.jpeg', '.jpg', '.ps', '.ppt', '.mp4',
              '.mp3', '.svg', 'mailto:', 'favicon', '.ico',
              '.css', '.apk', '.js', '.png', '.gif', '.pdf',
              '.doc', '@', 'tel']

date_now = str(datetime.now().strftime('%Y%m%d'))
PROJECT_PATH = 'CrawledData/' + date_now + "/"
log_file = date_now + ".log"


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
            target_link = self.url_queue.popleft().rstrip('/')
            if target_link not in self.crawled:
                response = connect_page(target_link)
                if response is not None:
                    if response.status_code == requests.codes.ok and \
                            'text/html' in response.headers['Content-Type'] and \
                            self.valid_link(response.url) \
                            and response.url.rstrip('/') not in self.crawled:
                        # Status code 200, html file and no external redirect
                        # also check if redirected file is going to same URL
                        # print("Success: writing to file:", self.count)
                        self.count += 1
                        print(self.count, "URL Scraping:", target_link)
                        self.crawled.add(target_link)
                        self.get_links(response.text, response.url)
                        try:
                            write_data_to_file(response.text, response.url, PROJECT_PATH + str(self.count))
                            logging.info(str(self.count) + ". URL Scraping: " + target_link)
                        except ValueError:
                            print("No data to parse in link ", target_link)
                            logging.error("No data to parse in link " + target_link)
                            self.count -= 1
                    else:
                        try:
                            print("Response Failed ", target_link, response.status_code)
                        except:
                            print("Response Failed ", target_link)
                        logging.error("Response Failed" + target_link)


if __name__ == '__main__':
    logging.basicConfig(filename=log_file, level=logging.INFO)
    start = time.process_time()
    crawler = WebCrawler(BASE_URL)
    crawler.run_scraper()
    print("Time taken:", time.process_time() - start)
