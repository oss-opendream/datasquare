'''Issue 생성하는 창을 띄우고 Issue, IssueComment를 생성하는 파일입니다.'''


from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from app.crud.issue_crud import IssueData
from app.crud.issue_comment_crud import IssueCommentData
from app.schemas.user_schema import User
from app.routers.sign import get_current_user


router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.post('/issue/publish')
async def create_issue(title: str = Form(...),
                       content: str = Form(...),
                       requested_team: str = Form(...),
                       is_private: int = Form(...),
                       current_user: User = Depends(get_current_user)
                       ):
    '''
    Issue, IssueComment 객체를 생성하고 데이터베이스에 저장,
    issue/view/issue_id={Issue.issue_id} 페이지로 Redirect합니다.
    '''

    issue_data = IssueData(current_user.profile_id)

    new_issue = issue_data.create_issue(
        title=title,
        content=content,
        requested_team=requested_team,
        is_private=is_private
    )

    IssueCommentData(current_user.profile_id).create_issue_comment(
        new_issue.issue_id)

    return RedirectResponse(
        url=f'/issue/view?issue_id={new_issue.issue_id}',
        status_code=303
    )


@router.get('/issue/publish', response_class=HTMLResponse)
async def issue_pulish(request: Request,
                       current_user: User = Depends(get_current_user)
                       ):
    '''
    이슈 발행 페이지 함수입니다.
    '''

    return templates.TemplateResponse('issue_publish.html', {'request': request})
