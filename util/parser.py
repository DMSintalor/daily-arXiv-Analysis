import re
from datetime import datetime

import lxml
from lxml.etree import ElementBase

from util.functional import cleanup
from util.struct import LinkStruct


class Parser:
    @staticmethod
    def link(elements):
        if isinstance(elements, lxml.etree._Element):
            text = ''.join(elements.xpath('./text()')[0])
            href = ''.join(elements.xpath('./@href')[0])
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

    @staticmethod
    def article_link(element: ElementBase):
        article_link, pdf_link = element.xpath('./span/a/@href')[:2]
        return {'link': cleanup(article_link), 'pdf_link': cleanup(pdf_link)}

    @staticmethod
    def article_info(element: ElementBase):
        title = element.xpath('./div/div[1]/text()')
        authors = element.xpath('//*[@id="dlpage"]/dl/dd[5]/div/div[2]//text()')
        subjects = element.xpath(
            '//*[@id="dlpage"]/dl/dd[5]/div/div[@class="list-subjects"]/span[@class="primary-subject"]/text()'
        )
        return {
            'title': cleanup(title),
            'authors': cleanup(authors),
            'subjects': cleanup(subjects)
        }

    @staticmethod
    def dateline(text: str) -> datetime:
        date_pattern = re.compile(r'\b(\d{1,2}\s+[a-zA-Z]+\s+\d{4})\b')
        match = date_pattern.search(text)
        if match:
            extracted_date_str = match.group(1)
            extracted_date = datetime.strptime(extracted_date_str, "%d %b %Y")
            return extracted_date
        else:
            print("No date found.")
