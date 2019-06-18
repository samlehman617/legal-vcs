#!/usr/bin/env python3
import re, datetime
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup as BS

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def main():
    print('begin')
    raw_html = simple_get('http://uscode.house.gov/download/download.shtml')
    html = BS(raw_html, 'html.parser')
    # print(html)
    updated = html.find('h3').text
    download =  ''
    for a in html.find_all('a'):
        if a.text == '[XHTML]':
            download = a
    print(updated)
    print(download.text)
    # for h in html.find('h3'):
        # if h['class'] == 'releasepointinformation':
        #    print(h.text)
    release = re.search(r'\d{3}-\d{3}', updated).group()
    print(release)

if __name__=='__main__':
    main()
