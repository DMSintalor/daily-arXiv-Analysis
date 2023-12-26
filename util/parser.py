from lxml.etree import ElementBase

from util.struct import LinkStruct


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
