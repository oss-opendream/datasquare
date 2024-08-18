'''
    Issue feed 관련 라우터 정의 모듈
'''
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.crud.feed import IssueData, Team


router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/feed')
async def read_dashboard(request: Request):
    '''
    조직 내 공개된 전체 이슈 목록 출력 라우터
    '''

    team = Team()
    teams_list = team.get_all()

    issue = IssueData(current_userid=2)
    issue_data = issue.get_all()

    return templates.TemplateResponse('feed.html',
                                      {
                                          'request': request,
                                          'teams': teams_list,
                                          'issues': issue_data
                                      }
                                      )


@router.get('/feed/my_issues')
async def read_my_issues(request: Request):
    '''
    현재 접속자가 작성한 이슈 목록 출력 라우터
    '''

    team = Team()
    teams_list = team.get_all()

    issue = IssueData(current_userid=2)
    issue_data = issue.get_current_users()

    return templates.TemplateResponse('feed.html',
                                      {
                                          'request': request, 'teams': teams_list, 'issues': issue_data
                                      }
                                      )


@router.get('/feed/search')
async def search_issues(request: Request, keyword: str, team=str):
    '''
    제목 또는 팀으로 검색된 이슈 목록 출력 함수
    '''

    team = Team()
    teams_list = team.get_all()

    issue = IssueData(current_userid=2)
    result_data = issue.search(keyword=keyword, team=team)

    return templates.TemplateResponse('feed.html', {'request': request, 'teams': teams_list, 'issues': result_data})
