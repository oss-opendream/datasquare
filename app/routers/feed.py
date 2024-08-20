'''Issue feed 관련 라우터 정의 모듈'''


from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.routers.sign import get_current_user
from app.schemas.user_schema import User
from app.crud.feed_crud import IssueData, Team


router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/feed')
async def read_dashboard(request: Request,
                         current_user: User = Depends(get_current_user)):
    '''조직 내 공개된 전체 이슈 목록 출력 라우터'''

    team = Team()
    teams_list = team.get_all()

    # current_userid: 현재 user의 personal_profile 테이블 중 profile_id
    issue = IssueData(current_user.profile_id)
    issue_data = issue.get_all()

    return templates.TemplateResponse(
        'pages/feed.html',
        {
            'request': request,
            'teams': teams_list,
            'issues': issue_data
        }
    )


@router.get('/feed/my_issues')
async def read_my_issues(request: Request,
                         current_user: User = Depends(get_current_user)):
    '''현재 접속자가 작성한 이슈 목록 출력 라우터'''

    team = Team()
    teams_list = team.get_all()

    # current_userid: 현재 user의 personal_profile 테이블 중 profile_id
    issue = IssueData(current_user.profile_id)
    issue_data = issue.get_current_users()

    return templates.TemplateResponse(
        'pages/feed.html',
        {
            'request': request,
            'teams': teams_list,
            'issues': issue_data
        }
    )


@ router.get('/feed/search')
async def search_issues(request: Request,
                        keyword="",
                        team="",
                        current_user: User = Depends(get_current_user)):
    '''제목 또는 팀으로 검색된 이슈 목록 출력 함수'''

    team_data = Team()
    teams_list = team_data.get_all()

    # current_userid: 현재 user의 personal_profile 테이블 중 profile_id
    issue = IssueData(current_user.profile_id)
    result_data = issue.search(keyword=keyword, team=team)

    return templates.TemplateResponse(
        'pages/feed.html',
        {
            'request': request,
            'teams': teams_list,
            'issues': result_data
        }
    )
