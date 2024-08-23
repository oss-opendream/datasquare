'''Issue 생성하는 창을 띄우고 Issue, IssueComment를 생성하는 파일입니다.'''


from fastapi import APIRouter, Request, HTTPException, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from app.crud.issue_crud import IssueData
from app.crud.issue_comment_crud import IssueCommentData
from app.crud.team_crud import TeamData
from app.schemas.user_schema import User
from app.utils.get_current_user import get_current_user
from app.crud.noti import get_notification_count


router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.post('/issue/publish', name='data_request')
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
        new_issue.issue_id, 'Init new issue!!!!')

    ret = RedirectResponse(
        url=f'/issue/view?issue_id={new_issue.issue_id}',
        status_code=303
    )

    return ret


@router.get('/issue/publish', response_class=HTMLResponse, name='data_request')
async def issue_pulish(request: Request,
                       current_user: User = Depends(get_current_user)
                       ):
    '''
    이슈 발행 페이지 함수입니다.
    team 종류 데이터를 받아서 html로 보냅니다.
    '''

    departments = TeamData().get_team_name()
    ret = templates.TemplateResponse(
        'pages/issue_publish.html',
        {
            'request': request,
            'departments': departments,
            'notification_count': get_notification_count(current_user.profile_id)
        }
    )

    return ret


@router.post('/issue/modified', name='data_modified')
async def modified_issue(issue_id: int = Form(...),
                         title: str = Form(...),
                         content: str = Form(...),
                         requested_team: str = Form(...),
                         is_private: int = Form(...),
                         current_user: User = Depends(get_current_user)
                         ):
    '''
    issue data 수정한 것을 반영하는 함수 입니다.
    issue/view/issue_id={Issue.issue_id} 페이지로 Redirect합니다.
    '''

    new_issue = IssueData(
        current_userid=current_user.profile_id).modified_issue(issue_id=issue_id,
                                                               title=title,
                                                               content=content,
                                                               requested_team=requested_team,
                                                               is_private=is_private
                                                               )

    IssueCommentData(current_user.profile_id).create_issue_comment(
        new_issue.issue_id, 'Modified issue!!!!')

    ret = RedirectResponse(
        url=f'/issue/view?issue_id={new_issue.issue_id}',
        status_code=303
    )

    return ret


@ router.get('/issue/modified', response_class=HTMLResponse, name='data_modified')
async def issue_modified_page(request: Request,
                              issue_id: int,
                              current_user: User = Depends(get_current_user)
                              ):
    '''
    이슈 수정 페이지 함수입니다.
    이슈 아이디 정보를 받아와서 표시합니다.
    '''

    issue = IssueData(current_userid=current_user).read_issue(
        issue_id=issue_id)

    if not issue:
        raise HTTPException(status_code=404, detail='Issue not found')

    departments = TeamData().get_team_name()

    ret = templates.TemplateResponse(
        'pages/issue_modified.html',
        {
            'request': request,
            'departments': departments,
            'issue': issue,
            'notification_count': get_notification_count(current_user.profile_id)
        }
    )

    return ret


@router.post('/issue/deleted', name='data_modified')
async def deleted_issue(issue_id: int = Form(...),
                        current_user: User = Depends(get_current_user)
                        ):
    '''
    issue data 수정한 것을 반영하는 함수 입니다.
    issue/view/issue_id={Issue.issue_id} 페이지로 Redirect합니다.
    '''

    try:
        IssueData(current_userid=current_user.profile_id).delete_issue(
            issue_id=issue_id)
        ret = RedirectResponse(url='/feed', status_code=303)
    except PermissionError:
        ret = RedirectResponse(
            url=f'/issue/view?issue_id={issue_id}',
            status_code=303
        )

    return ret
