import requests
from bs4 import BeautifulSoup, Comment


def filter_tags(element):
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
        'style'
    ]
    if element.parent.name not in blacklist:
        return True
    return False


def connect_page(url):
    # Connect to a page. Try again after 2 seconds
    try:
        result = requests.get(url, timeout=2)
    except requests.ConnectionError:
        return ''
    return result


def scrape_links(html):
    soup = BeautifulSoup(html, features='html.parser')
    links = soup.find_all('a', href=True)
    return links


def extract_data(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    comments = soup.find_all(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()
    texts = soup.find_all(text=True)
    filtered_text = filter(filter_tags, texts)

    return " ".join([i.strip() for i in filtered_text])


def write_data_to_file(html, url, file_id):
    extracted_text = extract_data(html)
    with open(file_id, 'w') as f:
        f.writelines("URL:" + url)
        f.writelines(extracted_text)
