from connection import Base
from createDB import Website
from createDB import Page
from createDB import Keyword
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class SQLmanager:

    def __init__(self):
        engine = create_engine("sqlite:///pages.db")
        Base.metadata.create_all(engine)
        self.session = Session(bind=engine)

    def website_to_base(self, domain, soup):
        website = Website()
        website.url = "http://" + domain
        website.Title = soup.title.string
        website.Domain = domain
        website.page_count = len(soup.find_all('a'))
        self.session.add(website)
        self.session.commit()

    def page_to_base(self, url, soup, domain):
        page = Page()
        page.url = url
        page.title = soup.title.string
        try:
            description = soup.find(attrs={"property": "og:description"}).get("content")
        except Exception:
            description = ''
        page.description = description
        site = self.session.query(Website).filter(Website.Domain == domain).one()
        page.website = site
        self.session.add(page)
        self.session.commit()

    def keywords_to_base(self, string):
        keywords = string.split()
        results = []
        page = {}
        urls = []
        for page in self.session.query(Page):
            for keyword in keywords:
                if keyword in page.title or keyword in page.description:
                    page["url"] = page.url
                    page["title"] = page.title
                    page["description"] = page.description
                    if page.url not in urls:
                        results.append(page)
                    urls.append(page.url)
        return results
