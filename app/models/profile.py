''' 사용자 및 팀 metadata 관리 테이블에 대한 객체를 정의하기 위한 모듈 '''


from sqlalchemy import Column, Integer, ForeignKey, BLOB, Text, String
from sqlalchemy.orm import relationship

from app.models.database import Base, datasquare_db
from app.models.issue import *


Base.metadata.create_all(bind=datasquare_db.engine)


class PersonalProfile(Base):
    __tablename__ = 'personal_profile'

    profile_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    profile_image = Column(BLOB)

    # Relationships
    teams_re = relationship('TeamProfile', back_populates='team_manager_re')
    issues_re = relationship('Issue', back_populates='publisher_re')
    comments_re = relationship('IssueComment', back_populates='publisher_re')
    memberships_re = relationship('TeamMembership', back_populates='member_re')

class TeamProfile(Base):
    __tablename__ = 'team_profile'

    profile_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    team_name = Column(String, unique=True, nullable=False)
    team_introduction = Column(Text, nullable=False)
    team_manager = Column(Integer, ForeignKey('personal_profile.profile_id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    profile_image = Column(BLOB)

    # Relationships
    team_manager_re = relationship('PersonalProfile', back_populates='teams_re')
    members_re = relationship('TeamMembership', back_populates='team_re')

class TeamMembership(Base):
    __tablename__ = 'team_membership'

    membership_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    member_id = Column(Integer, ForeignKey('personal_profile.profile_id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    team_id = Column(Integer, ForeignKey('team_profile.profile_id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)

    # Relationships
    member_re = relationship('PersonalProfile', back_populates='memberships_re')
    team_re = relationship('TeamProfile', back_populates='members_re')
