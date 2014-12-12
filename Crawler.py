import urllib
import requests
import bs4
from AddToBase import SQLmanager


class Crawler():

    def __init__(self):
        self.domain = ''
        self.scanned_urls = []
        self.to_scan = []
        self.manager = SQLmanager()

    def is_ingoing(self, url):
        if self.domain in url[0: 50]:
            return True
        else:
            return False

    def __prepare_link(self, url, href):
        return urllib.parse.urljoin(url, href)

    def valid_page(self, soup, url):
        if not self.is_ingoing(url):
            return False

        if '#' in url:
            return False

        if url in self.scanned_urls:
            return False

        try:
            soup.title()
        except Exception:
            return False

        return True

    def scan_website(self, domain):
        self.domain = domain

        request = requests.get("http://" + domain)
        html = request.text
        soup = bs4.BeautifulSoup(html)

        self.manager.website_to_base(domain, soup)
        self.scan_page('http://' + domain)
        while (len(self.to_scan) != 0):
            self.scan_page(self.to_scan.pop())

    def scan_page(self, url):
        request = requests.get(url)
        html = request.text
        soup = bs4.BeautifulSoup(html)

        self.manager.page_to_base(url, soup, self.domain)

        print(url)
        self.scanned_urls.append(url)

        for link in soup.find_all('a'):
            new_link = self.__prepare_link(url, link.get('href'))
            if self.valid_page(soup, new_link):
                self.to_scan.append(new_link)


def main():
    crawler = Crawler()
    crawler.scan_website('mattcutts.com/blog')

if __name__ == '__main__':
    main()
