from fastapi import APIRouter, Response, status, HTTPException
from starlette.requests import Request

from database.model import Article, ArticleOperations
from util.EnumCode import ArticleStatus, ArticleOperateCode

router = APIRouter(prefix='/operate', tags=['operate'])

op_dict = {
    ArticleOperateCode.READ: ArticleStatus.READ,
    ArticleOperateCode.COLLECT: ArticleStatus.COLLECTED,
    ArticleOperateCode.DISLIKE: ArticleStatus.DISLIKE,
    ArticleOperateCode.DisCOLLECT: ArticleStatus.UNREAD,
    ArticleOperateCode.SHARE: ArticleStatus.READ,
}


def update_option(request: Request, article_id, operate_id):
    with request.app.db_controller.mysql.get_db() as db:
        article = db.query(Article).filter_by(id=article_id).first()
        if article is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        article.status = op_dict.get(operate_id, ArticleStatus.READ)
        op = ArticleOperations(article_id=article_id, operate_id=operate_id)
        db.add(op)
        db.commit()


@router.post("/read")
async def read_article(request: Request, article_id: int):
    try:
        update_option(request, article_id, ArticleOperateCode.READ)
        return Response("OK", status_code=status.HTTP_200_OK)
    except Exception as e:
        return e


@router.post("/collect")
async def collect_article(request: Request, article_id: int):
    try:
        update_option(request, article_id, ArticleOperateCode.COLLECT)
        return Response("OK", status_code=status.HTTP_200_OK)
    except Exception as e:
        return e


@router.post("/dis_collect")
async def dis_collect_article(request: Request, article_id: int):
    try:
        update_option(request, article_id, ArticleOperateCode.DisCOLLECT)
        return Response("OK", status_code=status.HTTP_200_OK)
    except Exception as e:
        return e


@router.post("/dislike")
async def dislike_article(request: Request, article_id: int):
    try:
        update_option(request, article_id, ArticleOperateCode.DISLIKE)
        return Response("OK", status_code=status.HTTP_200_OK)
    except Exception as e:
        return e
