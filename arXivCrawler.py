import argparse
import asyncio
import time

import tqdm
from requests.sessions import Session
from lxml import etree
from lxml.etree import ElementBase
import re

from database import DatabaseController
from util.functional import get_cfg, cleanup
from util.parser import Parser

from database.model import Article
from util.struct import ArticleStruct, LinkStruct


class Crawler:
    def __init__(self, cfg):
        self.cfg = cfg
        self.database_controller = DatabaseController(cfg)
        self.article_nums = 0
        self.index_url = 'https://arxiv.org/list/cs/pastweek?skip=0&show=5'
        self.base_url = 'https://arxiv.org'
        self.sess = Session()
        self.dom = None
        self._init()

    def _init(self):
        self.dom = self.get_dom()

    def get_article_num(self):
        row = self.get_element_by_xpath(self.dom, '//*[@id="dlpage"]/small[1]')[0]
        row_txt = ''.join(row.xpath('.//text()'))

        pattern = r'total of (\d+) entries'
        match = re.search(pattern, row_txt)
        if match:
            result = match.group(1)
            self.article_nums = int(result)
        else:
            raise Exception('get article num error')
        print(f'get {self.article_nums} articles')

    def join_url(self, url):
        return f'{self.base_url}/{str(url).lstrip("/")}'

    def get_dom(self, url=None) -> ElementBase:
        res = self.sess.get(url if url else self.index_url)
        dom: ElementBase = etree.HTML(res.content)
        return dom

    @staticmethod
    def get_element_by_xpath(dom: ElementBase, xpath: str) -> ElementBase:
        return dom.xpath(xpath)

    async def get_articles(self):
        self.get_article_num()
        articles_per_page = self.cfg['crawler']['articles_per_page']
        pbar = tqdm.tqdm(total=self.article_nums, desc='Getting Articles')
        for i in range(0, self.article_nums, articles_per_page):
            url = self.join_url('/list/cs/pastweek?skip={}&show={}'.format(i // articles_per_page, articles_per_page))
            dom = self.get_dom(url)
            articles_link_list = dom.xpath('//*[@id="dlpage"]/dl/dt')
            articles_cont_list = dom.xpath('//*[@id="dlpage"]/dl/dd')
            articles = zip(articles_link_list, articles_cont_list)
            for link_box, art_info in articles:
                article_info = ArticleStruct()
                link_dic = Parser.article_link(link_box)
                info_dic = Parser.article_info(art_info)
                article_info.update_list(**link_dic)
                article_info.update_list(**info_dic)
                await self.database_controller.push_wait_queue('waiting_articles', str(article_info.link))
                pbar.update(1)
            time.sleep(.5)

    async def get_article_detail(self):
        add_cnt = 0
        pass_cnt = 0
        pbar = tqdm.tqdm(desc='Getting detail')
        url = await self.database_controller.pop_wait_queue('waiting_articles')
        while url:
            with self.database_controller.mysql.get_db() as db:
                try:
                    cnt = db.query(Article).filter_by(link=self.join_url(url)).count()
                    if cnt == 0:
                        article = self.get_article_content(url.decode())
                        art = Article(**article())
                        db.add(art)
                        db.commit()
                        add_cnt += 1
                        if add_cnt % 50 == 0:
                            time.sleep(10)
                    else:
                        pass_cnt += 1
                except Exception as e:
                    print(e, url)
                    await self.database_controller.push_wait_queue('waiting_articles', url)
            url = await self.database_controller.pop_wait_queue('waiting_articles')
            pbar.update(1)
            pbar.set_postfix_str('{} articles added, {} articles passed'.format(add_cnt, pass_cnt))

    def get_article_content(self, article_link: str) -> ArticleStruct:
        url = self.join_url(article_link)
        dom = self.get_dom(url)
        title = ''.join(dom.xpath('//*[@id="abs"]/h1/text()')).strip()
        abstract = ''.join(dom.xpath('//*[@class="abstract mathjax"]/text()')).strip()
        authors = ''.join(dom.xpath('//*[@id="abs"]/div[2]//text()')).strip().replace('Authors:', '')
        subjects = ''.join(dom.xpath('//*[@class="primary-subject"]/text()')).strip()
        journal = ''.join(dom.xpath('//*[@class="subheader"]/h1/text()')).strip()
        date = Parser.dateline(cleanup(dom.xpath('//*[@class="dateline"]/text()')))
        pdf_link = Parser.link(dom.xpath('//*[@class="abs-button download-pdf"]')[0])
        article = ArticleStruct(
            title=title,
            abstract=abstract,
            authors=authors,
            link=LinkStruct(title, url),
            pdf_link=pdf_link,
            doi=str(article_link).strip('/abs/'),
            journal=journal,
            subjects=subjects,
            date=date
        )
        return article


def make_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'task',
        type=str,
        help='<1>: get hrefs\n<2>: get details\n<3>: all tasks',
        choices=['1', '2', '3']
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = make_args()
    crawler = Crawler(get_cfg())
    if args.task == '1':
        asyncio.run(crawler.get_articles())
    elif args.task == '2':
        asyncio.run(crawler.get_article_detail())
    elif args.task == '3':
        asyncio.run(crawler.get_articles())
        asyncio.run(crawler.get_article_detail())
