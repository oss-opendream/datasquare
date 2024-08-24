'''
issue_id를 기준으로 issue데이터와 issue_comment를 불러옵니다.
댓글을 등록하면 issue_comment를 생성하고 추가로 출력합니다.
'''


from fastapi import APIRouter, Request, HTTPException, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse


from app.crud.issue_crud import IssueData
from app.crud.issue_comment_crud import IssueCommentData
from app.schemas.user_schema import User
from app.utils.get_current_user import get_current_user
from app.crud.noti import get_notification_count


issue_comment_router = APIRouter(prefix='/issue_comment')
templates = Jinja2Templates(directory='app/templates')


@issue_comment_router.post('/create')
async def create_issue_comment(issue_id: int = Form(...),
                               comment: str = Form(...),
                               current_user: User = Depends(get_current_user)):
    '''issue_commnet 생성 함수 입니다.'''

    IssueCommentData(current_user.profile_id).create_issue_comment(
        issue_id, comment)

    ret = RedirectResponse(
        url=f'/data_request/view?issue_id={issue_id}', status_code=303)

    return ret


@issue_comment_router.post('/modify')
async def modify_issue_comment(comment_id: int = Form(...),
                               content: str = Form(...),
                               current_user: User = Depends(get_current_user)):
    '''issue_comment 수정 함수입니다.'''

    comment = IssueCommentData(current_userid=current_user.profile_id).modified_issue_comment(
        comment_id=comment_id, content=content)

    issue_id = comment.within

    ret = RedirectResponse(
        url=f'/data_request/view?issue_id={issue_id}', status_code=303)

    return ret


@issue_comment_router.post('/delete')
async def delete_issue_comment(issue_id: int = Form(...),
                               comment_id: int = Form(...),
                               current_user: User = Depends(get_current_user)):
    '''issue_commnet 삭제 함수 입니다.'''

    IssueCommentData(
        current_userid=current_user.profile_id).delete_issue_comment(comment_id)

    ret = RedirectResponse(
        url=f'/data_request/view?issue_id={issue_id}', status_code=303)

    return ret