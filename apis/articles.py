from fastapi import APIRouter, Response, status
from starlette.requests import Request

from database.model import Article
from util.EnumCode import ArticleStatus, SubCode2SubText

router = APIRouter(prefix='/articles', tags=['articles'])


def get_article_by_status(request: Request, skip: int = 0, limit: int = 10, status_id=None, sub=None):
    fields = ['title', 'subjects', 'doi', 'date', 'status']
    with request.app.db_controller.mysql.get_db() as db:
        articles = db.query(
            *[getattr(Article, field) for field in fields]
        )
        if status_id is not None:
            articles = articles.filter_by(status=ArticleStatus.UNREAD)
        if sub is not None:
            articles = articles.filter_by(subjects=getattr(SubCode2SubText, sub.upper()))
        max_skip = articles.count()
        if skip > max_skip or limit > 50:
            return Response('Invalid request.', status.HTTP_403_FORBIDDEN)
        articles = articles.offset(skip).limit(limit).all()
    articles = [{
        field: article[i] if field != 'date' else article[i].strftime('%Y-%m-%d')
        for i, field in enumerate(fields)
    } for article in articles]
    return articles, max_skip


@router.get('/all')
def get_articles(request: Request, skip: int = 0, limit: int = 10, sub=None):
    articles, count = get_article_by_status(request, skip, limit, sub=sub)
    return {'articles': articles, 'count': count}


@router.get('/unread')
def get_articles_unread(request: Request, skip: int = 0, limit: int = 10, sub=None):
    articles, count = get_article_by_status(request, skip, limit, ArticleStatus.UNREAD, sub=sub)
    return {'articles': articles, 'count': count}


@router.get('/read')
def get_articles_read(request: Request, skip: int = 0, limit: int = 10, sub=None):
    articles, count = get_article_by_status(request, skip, limit, ArticleStatus.READ, sub=sub)
    return {'articles': articles, 'count': count}


@router.get('/collect')
def get_articles_collect(request: Request, skip: int = 0, limit: int = 10, sub=None):
    articles, count = get_article_by_status(request, skip, limit, ArticleStatus.COLLECTED, sub=sub)
    return {'articles': articles, 'count': count}


@router.get('/dislike')
def get_articles_collect(request: Request, skip: int = 0, limit: int = 10, sub=None):
    articles, count = get_article_by_status(request, skip, limit, ArticleStatus.DISLIKE, sub=sub)
    return {'articles': articles, 'count': count}
