from urllib.parse import urlparse


def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''


# Get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''


def edit_url(link, parent_link):
    link_parsed = urlparse(link)
    parent_parsed = urlparse(parent_link)

    if link_parsed.netloc is '':
        new_link = link_parsed._replace(scheme='https', netloc=parent_parsed.netloc)
    else:
        new_link = link_parsed._replace(scheme='https')
    return new_link.geturl()
