import base64

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.models.database import Base, SessionLocal, engine
from app.models.issue import Issue
from app.models.profile import PersonalProfile, TeamProfile, TeamMembership


Base.metadata.create_all(bind=engine)

router = APIRouter()
templates = Jinja2Templates(directory='templates')


def get_db():
    '''
    DB 세션 관리 함수
    '''

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/feed')
async def read_dashboard(request: Request, db: Session = Depends(get_db)):
    '''
    조직 내 공개된 전체 이슈 목록 출력 함수
    '''

    # retrieve teams list
    teams = db.query(TeamProfile).with_entities(
        TeamProfile.team_name, TeamProfile.profile_id).all()

    issue_base_query = db.query(
        Issue, PersonalProfile, TeamProfile).filter(Issue.is_private == 0)
    issues = issue_base_query.join(PersonalProfile, Issue.publisher_id == PersonalProfile.profile_id) \
        .join(TeamMembership, PersonalProfile.profile_id == TeamMembership.member_id) \
        .join(TeamProfile, TeamMembership.team_id == TeamProfile.profile_id).all()

    issue_data = []

    for issue, personal_profile, team_profile in issues:

        issue_data.append(
            {
                'title': issue.title,
                'content': issue.content,
                'author_name': personal_profile.name,
                'team': team_profile.team_name,
                'profile_pic': base64.b64encode(personal_profile.profile_image).decode('utf-8')
            }
        )

    return templates.TemplateResponse('feed.html',
                                      {
                                          'request': request,
                                          'teams': teams,
                                          'issues': issue_data
                                      }
                                      )


@router.get('/feed/my_issues')
async def read_my_issues(request: Request, db: Session = Depends(get_db)):
    '''
    현재 접속자가 작성한 이슈 목록 출력 함수
    '''

    teams = db.query(TeamProfile).with_entities(
        TeamProfile.team_name, TeamProfile.profile_id).all()
    # 'author_id='에 로그인 유저 ID 값 입력 필요(예시 ID: 1)
    issue_base_query = db.query(
        Issue, PersonalProfile, TeamProfile).filter(Issue.publisher_id == 1)
    issues = issue_base_query.join(PersonalProfile, Issue.publisher_id == PersonalProfile.profile_id) \
        .join(TeamMembership, PersonalProfile.profile_id == TeamMembership.member_id) \
        .join(TeamProfile, TeamMembership.team_id == TeamProfile.profile_id).all()

    issue_data = []

    for issue, personal_profile, team_profile in issues:
        issue_data.append(
            {
                'title': issue.title,
                'content': issue.content,
                'author_name': personal_profile.name,
                'team': team_profile.team_name,
                'profile_pic': base64.b64encode(personal_profile.profile_image).decode('utf-8')
            }
        )

    return templates.TemplateResponse('feed.html',
                                      {
                                          'request': request, 'teams': teams, 'issues': issue_data
                                      }
                                      )


@router.get('/feed/search')
async def search_issues(request: Request, keyword: str, team=str, db: Session = Depends(get_db)):
    '''
    제목으로 검색된 이슈 목록 출력 함수
    '''

    teams = db.query(TeamProfile).with_entities(
        TeamProfile.team_name, TeamProfile.profile_id).all()

    issue_base_query = db.query(Issue, PersonalProfile, TeamProfile) \
        .filter(Issue.is_private == 0)

    search_result = issue_base_query.join(PersonalProfile, Issue.publisher_id == PersonalProfile.profile_id) \
        .join(TeamMembership, PersonalProfile.profile_id == TeamMembership.member_id) \
        .join(TeamProfile, TeamMembership.team_id == TeamProfile.profile_id) \
        .filter(TeamProfile.team_name.contains(team)) \
        .filter(Issue.title.contains(keyword)) \
        .all()

    result_data = []

    for issue, personal_profile, team_profile in search_result:

        result_data.append({
            'title': issue.title,
            'content': issue.content,
            'author_name': personal_profile.name,
            'team': team_profile.team_name,
            'profile_pic': base64.b64encode(personal_profile.profile_image).decode('utf-8')
        })

    return templates.TemplateResponse('feed.html', {'request': request, 'teams': teams, 'issues': result_data})
