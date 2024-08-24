'''Team에 대한 CRUD 기능을 제공'''

from sqlalchemy.orm import Session

from app.models.database import datasquare_db
from app.models.profile import TeamProfile, TeamMembership, PersonalProfile


class TeamData:
    '''
    Team에 관련된 Table에서의 CRUD 작업 class
    '''

    def __init__(self, db: Session = datasquare_db) -> None:
        '''TeamData 클래스의 초기화 메서드'''
        self.db = db

    def get_team_name(self) -> list:
        '''모든 Team 부서 리스트를 DB에서 반환하는 함수'''

        with next(self.db.get_db()) as db_session:
            team_list = db_session.query(TeamProfile).all()
            departments = [team.team_name for team in team_list]

        return departments

    def get_current_user_team_data(self, current_userid: int) -> TeamProfile:
        '''특정 사용자의 팀 프로필 추출하는 함수'''

        with next(self.db.get_db()) as db_session:
            current_user_team_data = db_session \
                .query(TeamProfile) \
                .join(TeamMembership, TeamMembership.team_id == TeamProfile.profile_id) \
                .filter(TeamMembership.member_id == current_userid) \
                .one_or_none()

        return current_user_team_data

    def create_teams(self, team_names: list[str]) -> None:
        ''' 팀 프로필을 생성하는 함수 '''

        with next(self.db.get_db()) as db_session:
            for team in team_names:
                new_team = TeamProfile(team_name=team)
                db_session.add(new_team)

            db_session.commit()
            db_session.refresh(new_team)

    def get_team_members(self, team_id: int) -> list[PersonalProfile]:
        '''특정 팀에 해당하는 멤버 정보를 반환하는 함수'''

        with next(self.db.get_db()) as db_session:
            members = db_session.query(PersonalProfile) \
                                .filter(TeamMembership.team_id == team_id) \
                                .join(TeamMembership,
                                      TeamMembership.member_id == PersonalProfile.profile_id
                                      ) \
                                .all()

        return members

    def __create_base_query(self, db_session: Session) -> Session:
        '''Context manager 기반 Base query 객체 생성 함수'''

        base_query = db_session \
            .query(TeamProfile)

        return base_query

    def get_all(self) -> TeamProfile:
        ''' "team_profile" 테이블의 team_name과 profile_id를 출력 함수'''

        with next(self.db.get_db()) as db_session:
            base_query = self.__create_base_query(db_session)

            teams = base_query \
                .with_entities(
                    TeamProfile.team_name,
                    TeamProfile.profile_id
                ) \
                .all()

        return teams

    def get_team_name_one(self, team_profile_id: int):
        '''팀 아이디를 받아서 팀 이름 리턴 함수'''

        with next(self.db.get_db()) as db_session:
            team = db_session.query(TeamProfile).filter(
                TeamProfile.profile_id == team_profile_id).one_or_none()
            team_name = team.name

        return team_name

    def get_team_id(self, team_name: str):
        '''팀 이름을 받아서 팀 아이디 리턴 함수'''

        with next(self.db.get_db()) as db_session:

            team = db_session.query(TeamProfile).filter(
                TeamProfile.team_name == team_name).one()
            team_id = team.profile_id

        return team_id
