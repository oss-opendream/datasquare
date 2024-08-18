'''
    issue 목록 쿼리 후 Jinja2 template용 데이터로 출력하기 위한 모듈
'''
import base64

from sqlalchemy.orm import Session

from app.models.database import datasquare_db
from app.models.issue import Issue
from app.models.profile import PersonalProfile, TeamProfile, TeamMembership


class IssueData:
    '''
    "issue" 테이블에서 쿼리된 이슈 데이터에 대한 class
    '''

    def __init__(self, current_userid: str, db: Session = datasquare_db) -> None:
        self.db = db
        self.current_userid = current_userid

    def __create_base_query(self):
        '''
        Context manager 기반 Base query 객체 생성 함수
        '''
        with next(self.db.get_db()) as db_session:
            base_query = db_session \
                .query(Issue, PersonalProfile, TeamProfile) \
                .filter(Issue.is_private == 0) \
                .union(
                    db_session
                    .query(Issue, PersonalProfile, TeamProfile)
                    .filter(Issue.publisher_id == self.current_userid)
                )

            return base_query

    def __format_issue_data(self, queried_data):
        '''
        쿼리된 이슈 데이터를 Jinja2 template용 변수로 가공하여 출력하는 함수
        '''

        formatted_data = []

        for issue, personal_profile, team_profile in queried_data:
            formatted_data.append(
                {
                    'title': issue.title,
                    'content': issue.content,
                    'author_name': personal_profile.name,
                    'team': team_profile.team_name,
                    'profile_pic': base64.b64encode(personal_profile.profile_image).decode('utf-8')
                }
            )

        return formatted_data

    def get_all(self):
        '''
        조직 내 공개된 전체 이슈 및 내 이슈 목록 출력 함수
        '''

        base_query = self.__create_base_query()

        issues = base_query \
            .join(PersonalProfile, Issue.publisher_id == PersonalProfile.profile_id) \
            .join(TeamMembership, PersonalProfile.profile_id == TeamMembership.member_id) \
            .join(TeamProfile, TeamMembership.team_id == TeamProfile.profile_id) \
            .all()

        result_data = self.__format_issue_data(issues)

        return result_data

    def get_current_users(self):
        '''
        현재 접속 유저의 전체 이슈 목록 출력 함수
        '''

        base_query = self.__create_base_query()

        issues = base_query \
            .join(PersonalProfile, Issue.publisher_id == PersonalProfile.profile_id) \
            .join(TeamMembership, PersonalProfile.profile_id == TeamMembership.member_id) \
            .join(TeamProfile, TeamMembership.team_id == TeamProfile.profile_id) \
            .filter(Issue.publisher_id == self.current_userid) \
            .all()

        result_data = self.__format_issue_data(issues)

        return result_data

    def search(self, keyword: str = "", team: str = ""):
        '''
        제목 또는 팀명으로 검색된 이슈 목록 출력 함수
        '''

        base_query = self.__create_base_query()

        search_result = base_query \
            .join(PersonalProfile, Issue.publisher_id == PersonalProfile.profile_id) \
            .join(TeamMembership, PersonalProfile.profile_id == TeamMembership.member_id) \
            .join(TeamProfile, TeamMembership.team_id == TeamProfile.profile_id) \
            .filter(TeamProfile.team_name.contains(team)) \
            .filter(Issue.title.contains(keyword)) \
            .all()

        result_data = self.__format_issue_data(search_result)

        return result_data


class Team:
    '''
    "team_profile" 테이블 관련 쿼리된 데이터에 대한 class
    '''

    def __init__(self, db: Session = datasquare_db) -> None:
        self.db = db

    def __create_base_query(self):
        '''
        Context manager 기반 Base query 객체 생성 함수
        '''
        with next(self.db.get_db()) as db_session:
            base_query = db_session \
                .query(TeamProfile)

            return base_query

    def get_all(self):
        '''
        "team_profile" 테이블의 team_name, profile_id 출력 함수
        '''

        base_query = self.__create_base_query()

        teams = base_query \
            .with_entities(
                TeamProfile.team_name,
                TeamProfile.profile_id
            ) \
            .all()
        return teams
