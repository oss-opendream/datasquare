'''이슈 페이지 관리 라우터 모듈'''


from fastapi import APIRouter, Request, HTTPException, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from app.crud.issue_crud import IssueData
from app.crud.issue_comment_crud import IssueCommentData
from app.crud.noti import get_notification_count
from app.crud.team_crud import TeamData
from app.crud.user_crud import UserData
from app.schemas.user_schema import User
from app.utils.get_current_user import get_current_user


data_request_router = APIRouter(prefix='/data_request')
templates = Jinja2Templates(directory='app/templates')


@data_request_router.get('/publish', response_class=HTMLResponse, name='data_request')
async def issue_pulish(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    '''이슈 발행 페이지 함수'''

    departments = TeamData().get_team_name()
    ret = templates.TemplateResponse(
        'pages/data_request.html',
        {
            'request': request,
            'departments': departments,
            'notification_count': get_notification_count(current_user.profile_id)
        }
    )

    return ret


@data_request_router.get('/view', response_class=HTMLResponse, name='issue_views')
async def issue_views(
    request: Request,
    issue_id: int,
    current_user: User = Depends(get_current_user)
):
    '''이슈 조회 페이지 함수'''

    issue_data = IssueData(current_user.profile_id).read_issue(issue_id)
    if not issue_data:
        raise HTTPException(status_code=404, detail='Issue not found')

    comments = IssueCommentData(
        current_user.profile_id).read_issue_comments(issue_id)

    requested_team_name = TeamData().get_team_name_one(
        issue_data[0].requested_team)

    ret = templates.TemplateResponse(
        'pages/data_request_view.html',
        {
            'request': request,
            'issue': issue_data[0],
            'publisher': issue_data[1],
            'publisher_team': issue_data[2],
            'comments': comments,
            'team_name': requested_team_name,
            'current_user': current_user,
            'notification_count': get_notification_count(current_user.profile_id)
        }
    )

    return ret


@ data_request_router.post('/publish')
async def create_issue(title: str = Form(...),
                       content: str = Form(...),
                       requested_team: str = Form(...),
                       is_private: int = Form(...),
                       current_user: User = Depends(get_current_user)
                       ):
    '''새로운 Issue와 초기 IssueComment를 생성하고 저장'''

    issue_data = IssueData(current_user.profile_id)

    team_id = TeamData().get_team_id(requested_team)
    new_issue = issue_data.create_issue(
        title=title,
        content=content,
        requested_team=team_id,
        is_private=is_private
    )

    IssueCommentData(current_user.profile_id).create_issue_comment(
        new_issue.issue_id, 'Init new issue!!!!')

    ret = RedirectResponse(
        url=f'/data_request/view?issue_id={new_issue.issue_id}',
        status_code=303
    )

    return ret


@data_request_router.post('/edit')
async def update_issue(
    issue_id: int = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    requested_team: str = Form(...),
    is_private: int = Form(...),
    current_user: User = Depends(get_current_user)
):
    '''issue data 수정한 것을 반영하는 함수'''

    team_id = TeamData().get_team_id(requested_team)
    IssueData(current_userid=current_user.profile_id) \
        .update_issue_data(
            issue_id=issue_id,
            title=title,
            content=content,
            requested_team=team_id,
            is_private=is_private
    )

    IssueCommentData(current_userid=current_user.profile_id) \
        .create_issue_comment(
            issue_id=issue_id,
            content='Modified issue!!!!'
    )

    ret = RedirectResponse(
        url=f'/data_request/view?issue_id={issue_id}',
        status_code=303
    )

    return ret


@data_request_router.get('/edit', response_class=HTMLResponse)
async def issue_edit_page(request: Request,
                          issue_id: int,
                          current_user: User = Depends(get_current_user)
                          ):
    '''이슈 수정 페이지'''

    issue = IssueData(current_userid=current_user).read_issue(
        issue_id=issue_id)

    print()
    if not issue:
        raise HTTPException(status_code=404, detail='Issue not found')

    departments = TeamData().get_team_name()
    selected_team_name = TeamData().get_team_name_one(issue.requested_team)

    ret = templates.TemplateResponse(
        'pages/data_request_edit.html',
        {
            'request': request,
            'departments': departments,
            'selected_team_name': selected_team_name,
            'issue': issue,
            'notification_count': get_notification_count(current_user.profile_id)
        }
    )

    return ret


@data_request_router.post('/delete')
async def delete_issue(issue_id: int = Form(...),
                       current_user: User = Depends(get_current_user)
                       ):
    '''issue data 수정 함수'''

    try:
        IssueData(current_userid=current_user.profile_id).delete_issue_data(
            issue_id=issue_id)
        ret = RedirectResponse(url='/feed', status_code=303)
    except PermissionError:
        ret = RedirectResponse(
            url=f'/data_request/view?issue_id={issue_id}',
            status_code=303
        )

    return ret
