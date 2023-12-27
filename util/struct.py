from datetime import datetime
from typing import List

from util.functional import cleanup


class BaseStruct:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f'{self.__class__.__name__}({self.__dict__})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__})'

    def __call__(self, *args, **kwargs):
        return {k: v if isinstance(v, datetime) else str(v) for k, v in self.__dict__.items()}

    def update(self, key, val):
        setattr(self, key, val)

    def update_list(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class LinkStruct(BaseStruct):
    text: str
    href: str

    def __init__(self, text, href, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.href = href

    def __str__(self):
        return self.href

    def __repr__(self):
        return self.href


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
