'''Team에 대한 CRUD 기능을 제공'''


from typing import List, Optional

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
                new_team = TeamProfile(team_name=team,
                                       team_manager='')
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

    def get_all(self,) -> TeamProfile:
        ''' "team_profile" 테이블의 모든 레코드를 TeamProfile 객체로 출력하는 함수'''

        with next(self.db.get_db()) as db_session:

            teams = db_session \
                .query(TeamProfile, PersonalProfile) \
                .outerjoin(PersonalProfile, TeamProfile.team_manager == PersonalProfile.profile_id) \
                .all()

        return teams

    def get_team_name_one(self, team_profile_id: int):
        '''팀 아이디를 받아서 팀 이름 리턴 함수'''

        with next(self.db.get_db()) as db_session:
            team = db_session.query(TeamProfile).filter(
                TeamProfile.profile_id == team_profile_id).one_or_none()
            if team:
                team_name = team.team_name

        return team_name

    def get_team_id(self, team_name: str):
        '''팀 이름을 받아서 팀 아이디 리턴 함수'''

        with next(self.db.get_db()) as db_session:

            team = db_session.query(TeamProfile).filter(
                TeamProfile.team_name == team_name).one()
            team_id = team.profile_id

        return team_id

    def get_team_profile(self, team_profile_id: int) -> TeamProfile:
        '''"team_profile" 테이블 내 "team_profile_id"와 일치하는 TeamProfile 객체 반환 함수'''

        with next(self.db.get_db()) as db_session:
            team_profile = db_session \
                .query(TeamProfile) \
                .filter(TeamProfile.profile_id == team_profile_id) \
                .one_or_none()

        return team_profile

    def modify_team_info(
            self,
            team_names: List[str],
            profile_ids: List[Optional[str]],
            team_manager_ids: List[Optional[int]],
            delete_flags: List[str],
    ):
        '''team_profile row 수정, 삭제 및 추가 session commit 함수'''

        profile_ids = [int(pid) if pid.isdigit()
                       else None
                       for pid in profile_ids]

        team_manager_ids = [int(pid) if pid.isdigit()
                            else None
                            for pid in team_manager_ids]

        with next(self.db.get_db()) as db_session:

            for profile_id, team_name, team_manager_id, delete_flag in zip(
                    profile_ids,
                    team_names,
                    team_manager_ids,
                    delete_flags,
            ):

                if profile_id is not None:
                    if delete_flag == 'true':
                        profile_to_be_deleted = db_session \
                            .query(TeamProfile) \
                            .filter(TeamProfile.profile_id == profile_id) \
                            .one_or_none()
                        db_session.delete(profile_to_be_deleted)

                    elif team_name.strip():
                        profile_to_be_updated = db_session \
                            .query(TeamProfile) \
                            .filter(TeamProfile.profile_id == profile_id) \
                            .one_or_none()

                        profile_to_be_updated.team_name = team_name
                        profile_to_be_updated.team_manager = team_manager_id

                        db_session.add(profile_to_be_updated)

                else:
                    if team_name.strip():
                        new_team_profile = TeamProfile(
                            team_name=team_name,
                            team_manager=team_manager_id
                        )
                        db_session.add(new_team_profile)

            db_session.commit()

            for team_profile in db_session.query(TeamProfile).all():
                db_session.refresh(team_profile)

    def modify_team_info_profile(
            self,
            origin_name: str,
            team_name: str,
            team_intro: str
    ):
        '''team 프로필 설정 함수'''

        with next(self.db.get_db()) as db_session:

            team = db_session.query(TeamProfile).filter(
                TeamProfile.team_name == origin_name).one_or_none()

            print(team)

            if team:
                team.team_name = team_name
                team.team_introduction = team_intro

                db_session.commit()
