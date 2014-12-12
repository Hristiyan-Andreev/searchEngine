from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from createDB import Page

Base = declarative_base
engine = create_engine("sqlite:///pages.db")
session = Session(bind=engine)


def keywords_to_base(string):
    links = []
    keywords_list = string.split()

    for keyword in keywords_list:
        keyword_query = "%" + keyword + "%"
        sites_by_title = session.query(Page).filter(Page.title.ilike(keyword_query))
        for site in sites_by_title:
            site_info = {"url": site.url, "title": site.title, "description": site.description}
            links.append(site_info)

        sites_by_desc = session.query(Page).filter(Page.description.ilike(keyword_query))
        for site in sites_by_desc:
            site_info = {"url": site.url, "title": site.title, "description": site.description}
            if site_info not in links:
                links.append(site_info)
    print(links)
    return links
