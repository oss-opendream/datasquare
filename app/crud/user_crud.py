'''사용자 데이터에 대해 CRUD 기능을 제공.'''

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy.orm import joinedload

from app.schemas.user_schema import UserCreate
from app.models.profile import PersonalProfile, TeamProfile, TeamMembership
from app.models.database import datasquare_db


class UserData:
    '''User Data에 관련된 Tabel에 대한 CRUD 작업 class'''

    def __init__(self, db: Session = datasquare_db):
        self.db = db
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def create_user(self, user_create: UserCreate) -> None:
        '''회원 가입 정보를 DB에 적재.'''

        with next(self.db.get_db()) as db_session:
            personal_db = PersonalProfile(name=user_create.name,
                                          email=user_create.email,
                                          password=self.pwd_context.hash(
                                              user_create.password),
                                          phone_number=user_create.phone_number,
                                          profile_image=user_create.image
                                          )

            db_session.add(personal_db)
            db_session.commit()
            db_session.refresh(personal_db)

            team_db = TeamMembership(
                member_id=personal_db.profile_id,
                team_id=db_session.query(TeamProfile)
                .filter_by(team_name=user_create.department)
                .first().profile_id
            )

            db_session.add(team_db)
            db_session.commit()

    def get_user(self, data: str, key: str):
        '''주어진 사용자 정보로 데이터베이스에서 사용자의 존재 여부를 확인.'''

        with next(self.db.get_db()) as db_session:
            column = getattr(PersonalProfile, key)
            personal_data = db_session.query(PersonalProfile) \
                .filter(column == data) \
                .one_or_none()

        return personal_data

    def create_admin(self):

        with next(self.db.get_db()) as db_session:
            admin_db = PersonalProfile(name='admin',
                                       email='admin@admin.com',
                                       password=self.pwd_context.hash(
                                           'admin'),
                                       phone_number=0,
                                       profile_image=None
                                       )

            db_session.add(admin_db)
            db_session.commit()
            db_session.refresh(admin_db)
