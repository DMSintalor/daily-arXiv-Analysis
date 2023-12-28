from fastapi import APIRouter, Response, status
from starlette.requests import Request

from database.model import Article
from util.EnumCode import ArticleStatus, SubCode2SubText, SubText2SubCode

router = APIRouter(prefix='/subject', tags=['subject'])


@router.get('/all')
def get_subjects(request: Request, ):
    with request.app.db_controller.mysql.get_db() as db:
        subjects = db.query(Article.subjects).distinct().all()
    subjects = [{'text': it[0], 'code': SubText2SubCode.__getitem__(it[0])} for it in subjects]
    return subjects


@router.get('/articles')
def get_articles_by_subject(request: Request, subject: str):
    with request.app.db_controller.mysql.get_db() as db:
        articles = db.query(Article).filter_by(subjects=getattr(SubCode2SubText, subject.upper())).all()
    articles = [it.to_dict(fields=['title', 'subjects', 'doi', 'date', 'status']) for it in articles]
    return articles
