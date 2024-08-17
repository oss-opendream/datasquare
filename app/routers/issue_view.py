'''
issue_view.py
issue_id를 기준으로 issue데이터와 issue_comment를 불러옵니다.
댓글을 등록하면 issue_comment를 생성하고 추가로 출력합니다.
'''
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.models.database import Base, engine, get_db
from app.models.issue import Issue, IssueComment
from app.utils.time import current_time


Base.metadata.create_all(bind=engine)

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/issue/view/issue_id={issue_id}', response_class=HTMLResponse)
async def issue_views(request: Request,
                      issue_id: int,
                      db: Session = Depends(get_db)):
    '''
    이슈 조회 함수입니다.
    issue_id를 기준으로 issue 데이터와
    issue_comment.within == issue.issue_id인 issue_comment데이터를 불러옵니다.
    '''
    issue = db.query(Issue).filter(
        Issue.issue_id == issue_id).one_or_none()
    if not issue:
        raise HTTPException(status_code=404, detail='Issue not found')

    comments = db.query(IssueComment).filter(
        IssueComment.within == issue_id).all()
    if not comments:
        raise HTTPException(status_code=404, detail='Issue_Comments not found')

    return templates.TemplateResponse('issue_view.html',
                                      {'request': request, 'issue': issue, 'comments': comments})
