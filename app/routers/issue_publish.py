'''
issue_publish.py
Issue 생성하는 창을 띄우고 Issue, IssueComment를 생성하는 파일입니다.
'''
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.models.database import Base, engine, get_db
from app.models.issue import Issue, IssueComment
from app.utils.time import current_time


Base.metadata.create_all(bind=engine)

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.post('/issue/publish')
async def create_issue(title: str = Form(...),
                       content: str = Form(...),
                       requested_team: str = Form(...),
                       is_private: int = Form(...),
                       db: Session = Depends(get_db)
                       ):
    '''
    Issue, IssueComment 객체를 생성하고 데이터베이스에 저장,
    issue/view/issue_id={Issue.issue_id} 페이지로 Redirect합니다.
    '''
    ###
    # test user_id
    user_id = '1'
    ###
    now = current_time()
    new_issue = Issue(
        title=title,
        content=content,
        publisher_id=user_id,
        requested_team=requested_team,
        is_private=is_private,
        created_at=now,
        modified_at=now
    )
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)

    # 새로운 IssueComment 객체 생성
    new_comment = IssueComment(
        publisher_id=user_id,
        within=new_issue.issue_id,
        content='Init new issue!!!!'
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return RedirectResponse(url=f'/issue/view/issue_id={new_issue.issue_id}', status_code=303)


@router.get('/issue/publish', response_class=HTMLResponse)
async def issue_pulish(request: Request, db: Session = Depends(get_db)):
    '''
    이슈 발행 페이지 함수입니다.
    '''
    issues = db.query(Issue).all()
    return templates.TemplateResponse('issue_publish.html', {'request': request, 'issues': issues})
