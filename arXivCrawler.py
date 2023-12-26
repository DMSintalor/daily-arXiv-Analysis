from typing import Optional, List

import requests
from requests.sessions import Session
from lxml import etree
from lxml.etree import ElementBase
import re


class BaseStruct:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f'{self.__class__.__name__}({self.__dict__})'


class LinkStruct(BaseStruct):
    text: str
    href: str

    def __init__(self, text, href, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.href = href


class ArticleStruct(BaseStruct):
    title: str
    abstract: str
    authors: List[str]
    link: LinkStruct
    pdf_link: LinkStruct
    doi: str
    journal: str
    year: str
    month: str
    day: str
    hour: str
    minute: str
    second: str
    category: str
    comment: str
    comment_num: int
    view_num: int
    download_num: int
    comment_link: LinkStruct


class Parser:
    @staticmethod
    def link(elements):
        if isinstance(elements, ElementBase):
            text = ''.join(elements.xpath('./text()'))
            href = ''.join(elements.xpath('./@href'))
            return LinkStruct(text, href)
        elif isinstance(elements, list):
            results = []
            for ele in elements:
                text = ''.join(ele.xpath('./text()'))
                href = ''.join(ele.xpath('./@href'))
                results.append(LinkStruct(text, href))
            return results
        else:
            raise TypeError(f'elements type is {type(elements)}')


class Crawler:
    def __init__(self):
        self.article_nums = 0
        self.index_url = 'https://arxiv.org/list/cs/pastweek?skip=0&show=5'
        self.base_url = 'https://arxiv.org'
        self.sess = Session()
        self.dom = None
        self._init()
        self.get_article_num()

    def _init(self):
        self.dom = self.get_dom()

    def get_article_num(self):
        row = self.get_element_by_xpath(self.dom, '//*[@id="dlpage"]/small[1]')[0]
        row_txt = ''.join(row.xpath('.//text()'))

        pattern = r'total of (\d+) entries'
        match = re.search(pattern, row_txt)
        if match:
            result = match.group(1)
            self.article_nums = result
        else:
            raise Exception('get article num error')

    def join_url(self, url):
        return f'{self.index_url}/{url.lstrip("/")}'

    def get_dom(self, url=None) -> ElementBase:
        res = self.sess.get(url if url else self.index_url).content
        dom: ElementBase = etree.HTML(res)
        return dom

    @staticmethod
    def get_element_by_xpath(dom: ElementBase, xpath: str) -> ElementBase:
        return dom.xpath(xpath)

    def get_article_links(self, page_num: int) -> List[LinkStruct]:
        pass


if __name__ == '__main__':
    crawler = Crawler()
