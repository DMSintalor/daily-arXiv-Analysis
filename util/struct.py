from typing import List


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
    subjects: str
    date: str
