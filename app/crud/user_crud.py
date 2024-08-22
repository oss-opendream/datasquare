'''사용자 데이터에 대해 CRUD 기능을 제공.'''

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy.orm import joinedload
from sqlalchemy import update

from app.schemas.user_schema import UserCreate, User
from app.models.profile import PersonalProfile, TeamProfile, TeamMembership, Admin
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

    def get_user_password(self, data: str, key: str):

        with next(self.db.get_db()) as db_session:
            column = getattr(PersonalProfile, key)
            personal_data = db_session.query(PersonalProfile) \
                .filter(column == data) \
                .one_or_none()

        return personal_data

    def get_user(self, data: str, key: str) -> User:
        '''주어진 사용자 정보로 데이터베이스에서 사용자의 정보.'''

        with next(self.db.get_db()) as db_session:
            column = getattr(PersonalProfile, key)
            personal_data = db_session.query(PersonalProfile, TeamProfile) \
                .filter(column == data) \
                .join(TeamMembership, PersonalProfile.profile_id == TeamMembership.member_id) \
                .join(TeamProfile, TeamMembership.team_id == TeamProfile.profile_id) \
                .all()

            for person, team in personal_data:
                user_data = User(profile_id=person.profile_id,
                                 name=person.name,
                                 email=person.email,
                                 phone_number=person.phone_number,
                                 profile_image=person.profile_image,
                                 department=team.team_name,
                                 team_id=team.profile_id
                                 )

        return user_data

    def create_admin_re(self,
                        name,
                        email,
                        password):

        with next(self.db.get_db()) as db_session:
            admin_db = Admin(username=name,
                             email=email,
                             password=self.pwd_context.hash(
                                 password),
                             )

            db_session.add(admin_db)
            db_session.commit()
            db_session.refresh(admin_db)

    def is_admin_table(self):

        with next(self.db.get_db()) as db_session:
            row = db_session.query(Admin).count()

        return row

    def update_user_data(self, user_profile_id, update_date):

        with next(self.db.get_db()) as db_session:

            user_data = db_session.query(PersonalProfile) \
                .filter(PersonalProfile.profile_id == user_profile_id) \
                .one_or_none()

            user_data.name = update_date.name
            user_data.email = update_date.email
            user_data.phone_number = update_date.phone_number
            user_data.profile_image = update_date.profile_image

            db_session.commit()
            # db_session.update(update_data)

    def get_admin_data(self, email):
        with next(self.db.get_db()) as db_session:

            admin_data = db_session.query(Admin) \
                .filter(Admin.email == email) \
                .one_or_none()

        return admin_data
