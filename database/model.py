from sqlalchemy import Column, Integer, String, DateTime, Boolean

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
    date = Column(DateTime, nullable=False)

    def __init__(self, title, abstract, authors, link, pdf_link, doi, journal, date):
        self.title = title
        self.abstract = abstract
        self.authors = authors
        self.link = link
        self.pdf_link = pdf_link
        self.doi = doi
        self.journal = journal
        self.date = date

    def to_dict(self):
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


db.create_db()
