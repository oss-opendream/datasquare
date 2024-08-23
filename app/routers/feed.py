'''Issue feed 관련 라우터 정의 모듈'''


from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.utils.get_current_user import get_current_user
from app.schemas.user_schema import User
from app.crud.feed_crud import IssueData, Team
from app.crud.noti import get_notification_count

router = APIRouter()
templates = Jinja2Templates(directory='templates')


# @router.get('/feed')
@router.get('/feed', name='feed')
async def read_dashboard(request: Request,
                         order: str = 'desc',
                         current_user: User = Depends(get_current_user)):
    '''조직 내 공개된 전체 이슈 목록 출력 라우터'''

    team = Team()
    teams_list = team.get_all()

    issue = IssueData(current_user_profile=current_user,
                      order=order)
    issue_data = issue.get_all()

    return templates.TemplateResponse(
        'pages/feed.html',
        {
            'request': request,
            'teams': teams_list,
            'issues': issue_data,
            'notification_count': get_notification_count(current_user.profile_id)
        }
    )


@router.get('/feed/my_issues', name='my_issues')
async def read_my_issues(request: Request,
                         order: str = 'desc',
                         current_user: User = Depends(get_current_user)):
    '''현재 접속자가 작성한 이슈 목록 출력 라우터'''

    team = Team()
    teams_list = team.get_all()

    issue = IssueData(current_user_profile=current_user,
                      order=order)
    issue_data = issue.get_current_users()

    return templates.TemplateResponse(
        'pages/feed.html',
        {
            'request': request,
            'teams': teams_list,
            'issues': issue_data,
            'notification_count': get_notification_count(current_user.profile_id)
        }
    )


@router.get('/feed/search', name='search_feed')
async def search_issues(request: Request,
                        keyword="",
                        team="",
                        order: str = 'desc',
                        current_user: User = Depends(get_current_user)):
    '''제목 또는 팀으로 검색된 이슈 목록 출력 함수'''

    team_data = Team()
    teams_list = team_data.get_all()

    issue = IssueData(current_user_profile=current_user,
                      order=order)
    result_data = issue.search(keyword=keyword, team=team)

    return templates.TemplateResponse(
        'pages/feed.html',
        {
            'request': request,
            'teams': teams_list,
            'issues': result_data,
            'notification_count': get_notification_count(current_user.profile_id)
        }
    )
