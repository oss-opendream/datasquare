'''Team에 대한 CRUD 기능을 제공.'''

from sqlalchemy.orm import Session

from app.models.database import datasquare_db
from app.models.profile import TeamProfile, TeamMembership


class TeamData:
    '''
    Team에 관련된 Table에서의 CRUD 작업 class.
    '''

    def __init__(self, db: Session = datasquare_db) -> None:
        self.db = db

    def get_team_name(self) -> list:
        '''모든 Team 부서 list를 DB에서 반환.'''

        with next(self.db.get_db()) as db_session:
            team_list = db_session.query(TeamProfile).all()
            departments = [team.team_name for team in team_list]

        return departments

    def get_current_user_team_name(self, current_userid):

        with next(self.db.get_db()) as db_session:
            current_user_team_name = db_session \
                .query(TeamProfile) \
                .join(TeamMembership, TeamMembership.team_id == TeamProfile.profile_id) \
                .filter(TeamMembership.member_id == current_userid) \
                .one_or_none().team_name

        return current_user_team_name

    # def get_team_member(self, team_id):

    #     with next(self.db.get_db()) as db_session:

    #         team_member = db
