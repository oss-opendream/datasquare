'''이슈 목록을 쿼리하고 Jinja2 템플릿에 맞게 데이터를 가공하는 모듈'''


import base64

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.database import datasquare_db
from app.models.issue import Issue
from app.models.profile import PersonalProfile, TeamProfile, TeamMembership
from app.schemas.user_schema import User


class FeedData:
    '''이슈 데이터를 쿼리하고 Jinja2 템플릿용으로 가공하는 클래스'''

    def __init__(self,
                 current_user_profile: User,
                 order: str = "desc",
                 db: Session = datasquare_db) -> None:
        '''FeedData 클래스의 초기화 메서드'''

        self.db = db
        self.current_user_id = current_user_profile.profile_id
        self.current_user_name = current_user_profile.name
        self.current_user_team_id = current_user_profile.team_id
        self.current_user_team_name = current_user_profile.department
        self.issue_order = order

    def __create_base_query(self, db_session: Session) -> Session:
        '''기본 쿼리 객체를 생성하는 함수'''

        base_query = db_session \
            .query(Issue, PersonalProfile, TeamProfile) \
            .outerjoin(PersonalProfile, Issue.publisher == PersonalProfile.profile_id) \
            .outerjoin(TeamMembership, PersonalProfile.profile_id == TeamMembership.member_id) \
            .outerjoin(TeamProfile, TeamMembership.team_id == TeamProfile.profile_id) \
            .filter(Issue.is_deleted == 0) \
            .filter(or_(
                Issue.is_private == 0,
                Issue.publisher == self.current_user_id,
                Issue.requested_team == self.current_user_team_id
            )
            )

        return base_query

    def __format_issue_data(self, queried_data: list) -> list:
        '''쿼리된 이슈 데이터를 Jinja2 template용 변수로 가공하여 출력하는 함수'''

        formatted_data = []

        for issue, personal_profile, team_profile in queried_data:
            profile_picture_bin = None

            if personal_profile.profile_image is None:
                with open(file='app/static/images/default_user_thumb.png', mode='rb') as f:
                    profile_picture_bin = f.read()
            else:
                profile_picture_bin = personal_profile.profile_image

            formatted_data.append(
                {
                    'id': issue.issue_id,
                    'title': issue.title,
                    'content': issue.content,
                    'author_name': personal_profile.name,
                    'team': team_profile.team_name,
                    'profile_pic': base64.b64encode(profile_picture_bin).decode('utf-8'),
                    'created_at': issue.created_at,
                }
            )

        return formatted_data

    def get_all(self) -> Issue:
        '''공개된 전체 이슈와 현재 사용자의 이슈 목록을 조회하는 함수'''

        with next(self.db.get_db()) as db_session:
            base_query = self.__create_base_query(db_session)

            if self.issue_order == "asc":
                issues = base_query.order_by(Issue.created_at.asc()).all()
            else:
                issues = base_query.order_by(Issue.created_at.desc()).all()

        result_data = self.__format_issue_data(issues)

        return result_data

    def get_current_users(self) -> Issue:
        '''현재 사용자가 생성한 이슈와 요청된 팀의 이슈 목록을 조회하는 함수'''

        with next(self.db.get_db()) as db_session:

            base_query = self.__create_base_query(db_session)

            if self.issue_order == "asc":
                issues = base_query \
                    .filter(or_(Issue.publisher == self.current_user_id,
                                Issue.requested_team == self.current_user_team_id)) \
                    .order_by(Issue.created_at.asc()) \
                    .all()
            else:
                issues = base_query \
                    .filter(or_(Issue.publisher == self.current_user_id,
                                Issue.requested_team == self.current_user_team_id)) \
                    .order_by(Issue.created_at.desc()) \
                    .all()

        result_data = self.__format_issue_data(issues)

        return result_data

    def search(self, keyword: str, team: str) -> Issue:
        '''제목 또는 팀명으로 검색된 이슈 목록을 조회하는 함수'''

        with next(self.db.get_db()) as db_session:
            base_query = self.__create_base_query(db_session)

            if self.issue_order == "asc":
                search_result = base_query \
                    .filter(TeamProfile.team_name.contains(team)) \
                    .filter(or_(Issue.title.contains(keyword),
                                Issue.content.contains(keyword)
                                )) \
                    .order_by(Issue.created_at.asc()) \
                    .all()
            else:
                search_result = base_query \
                    .filter(TeamProfile.team_name.contains(team)) \
                    .filter(or_(Issue.title.contains(keyword),
                                Issue.content.contains(keyword)
                                )) \
                    .order_by(Issue.created_at.desc()) \
                    .all()

        result_data = self.__format_issue_data(search_result)

        return result_data
