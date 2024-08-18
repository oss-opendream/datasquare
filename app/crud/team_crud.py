'''Team에 대한 CRUD 기능을 제공.'''

from sqlalchemy.orm import Session

from app.models.database import datasquare_db
from app.models.profile import  TeamProfile


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
