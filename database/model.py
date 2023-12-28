from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from . import DatabaseController

db = DatabaseController()
Base = db.get_base()


class Article(Base):
    __tablename__ = 'Article'

    id = Column(Integer, primary_key=True)
    title = Column(String(length=300), nullable=False)
    abstract = Column(String(length=5000), nullable=False)
    authors = Column(String(length=300), nullable=False)
    link = Column(String(length=300), nullable=False)
    pdf_link = Column(String(length=300), nullable=False)
    doi = Column(String(length=100))
    journal = Column(String(length=100))
    subjects = Column(String(length=100))
    date = Column(DateTime, nullable=False)
    # 0:unread; 1:read; 2:collected; -1:dislike
    status = Column(Integer, default=0)

    article_operations = relationship("ArticleOperations", back_populates="article")

    def __init__(self, title, abstract, authors, link, pdf_link, doi, journal, subjects, date):
        self.title = title
        self.abstract = abstract
        self.authors = authors
        self.link = link
        self.pdf_link = pdf_link
        self.doi = doi
        self.journal = journal
        self.subjects = subjects
        self.date = date

    def to_dict(self, fields=None):
        if fields is None:
            return {
                'id': self.id,
                'title': self.title,
                'abstract': self.abstract,
                'authors': self.authors,
                'link': self.link,
                'pdf_link': self.pdf_link,
                'doi': self.doi,
                'journal': self.journal,
                'date': self.date.strftime('%Y-%m-%d')
            }
        else:
            return {getattr(self, field) for field in fields}


class ArticleOperations(Base):
    __tablename__ = 'ArticleOperations'

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('Article.id'), nullable=False)
    operate_id = Column(Integer)

    article = relationship("Article", back_populates="article_operations")


db.create_db()
