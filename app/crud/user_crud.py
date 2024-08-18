'''사용자 데이터에 대해 CRUD 기능을 제공.'''

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.schemas.user_schema import UserCreate
from app.models.profile import PersonalProfile, TeamProfile, TeamMembership
from app.models.database import datasquare_db


class UserData:
    '''
    User Data에 관련된 Tabel에 대한 CRUD 작업 class
    '''

    def __init__(self, db: Session = datasquare_db):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_user(self, user_create : UserCreate) -> None:
        '''회원 가입 정보를 DB에 적재.'''

        with next(self.db.get_db()) as db_session:
            personal_db = PersonalProfile(name=user_create.name,
                                  email=user_create.email,
                                  password=self.pwd_context.hash(
                                      user_create.password
                                      ),
                                  phone_number=user_create.phone_number
                                  )
            
            db_session.add(personal_db)
            db_session.commit()
            db_session.refresh(personal_db)

            team_db = TeamMembership(
                        member_id=personal_db.profile_id,
                        team_id=db_session.query(TeamProfile) \
                            .filter_by(team_name=user_create.department) \
                            .first().profile_id
                    )
            
            db_session.add(team_db)
            db_session.commit()

    def get_user(self, email : str) -> list:
        '''주어진 사용자의 Email 정보로 데이터베이스에서 사용자의 존재 여부를 확인.'''

        with next(self.db.get_db()) as db_session:
            personal_data = db_session.query(PersonalProfile) \
                                        .filter(PersonalProfile.email == email) \
                                        .first()
            
        return personal_data


##############################
# 암호화 객체 (bcrypt 사용)
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def create_user(db: Session, user_create: UserCreate):
#     '''회원 가입 정보를 DB에 적재.'''

#     # 회원가입 정보 저장
#     personal_db = PersonalProfile(name=user_create.name,
#                                   email=user_create.email,
#                                   password=pwd_context.hash(
#                                       user_create.password),
#                                   phone_number=user_create.phone_number)

#     db.add(personal_db)
#     db.commit()
#     db.refresh(personal_db)

#     # 부서 추가
#     team_db = TeamMembership(
#         member_id=personal_db.profile_id,
#         team_id=db.query(TeamProfile).filter_by(
#             team_name=user_create.department).first().profile_id
#     )

#     db.add(team_db)
#     db.commit()


# def get_user(db: Session, email : str):
#     '''주어진 사용자의 Email 정보로 데이터베이스에서 사용자의 존재 여부를 확인.'''

#     return db.query(PersonalProfile).filter(
#         PersonalProfile.email == email).first()

