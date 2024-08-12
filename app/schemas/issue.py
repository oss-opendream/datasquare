from sqlalchemy import Column, Integer, ForeignKey, BLOB, Text, String
from sqlalchemy.orm import relationship
from app.models import database

Base = database.Base


class PersonalProfile(Base):
    __tablename__ = 'personal_profile'

    profile_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    profile_image = Column(BLOB)

    teams_managed = relationship('TeamProfile', back_populates='manager')
    issues_published = relationship('Issue', back_populates='publisher')
    comments_published = relationship(
        'IssueComment', back_populates='publisher')
    memberships = relationship('TeamMembership', back_populates='member')


class TeamProfile(Base):
    __tablename__ = 'team_profile'

    profile_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    team_name = Column(String, nullable=False)
    team_introduction = Column(Text, nullable=False)
    team_manager = Column(Integer, ForeignKey(
        'personal_profile.profile_id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    profile_image = Column(BLOB)

    manager = relationship('PersonalProfile', back_populates='teams_managed')
    memberships = relationship('TeamMembership', back_populates='team')


class Issue(Base):
    __tablename__ = 'issue'

    issue_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    publisher_id = Column(Integer, ForeignKey(
        'personal_profile.profile_id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    requested_team = Column(Integer, nullable=False)
    is_private = Column(Integer, nullable=False)
    created_at = Column(String, nullable=False)
    modified_at = Column(String, nullable=False)

    publisher = relationship(
        'PersonalProfile', back_populates='issues_published')


# 하단부 모델 코드 별도 모듈화 필요

# class IssueComment(Base):
#     __tablename__ = 'issue_comment'

#     comment_id = Column(Integer, primary_key=True, unique=True, nullable=False)
#     publisher_id = Column(Integer, ForeignKey(
#         'personal_profile.profile_id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
#     within = Column(Integer, nullable=False)
#     content = Column(Text, nullable=False)

#     publisher = relationship(
#         'PersonalProfile', back_populates='comments_published')


# class OrgDatabase(Base):
#     __tablename__ = 'org_database'

#     database_id = Column(Integer, primary_key=True,
#                          unique=True, nullable=False)
#     database = Column(String, nullable=False)

#     tables = relationship('OrgDatabaseTable', back_populates='database')


# class OrgDatabaseTable(Base):
#     __tablename__ = 'org_database_table'

#     table_id = Column(Integer, primary_key=True, unique=True, nullable=False)
#     table_name = Column(String, nullable=False)
#     within_db = Column(Integer, ForeignKey('org_database.database_id',
#                        onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)

#     database = relationship('OrgDatabase', back_populates='tables')


# class DatabaseTag(Base):
#     __tablename__ = 'database_tag'

#     id = Column(Integer, primary_key=True, unique=True, nullable=False)
#     tag_name = Column(String, nullable=False)

#     relationships = relationship(
#         'DatabaseTagRelationship', back_populates='tag')


# class DatabaseTagRelationship(Base):
#     __tablename__ = 'database_tag_relationship'

#     relationship_id = Column(Integer, primary_key=True,
#                              unique=True, nullable=False)
#     tag_id = Column(Integer, ForeignKey('database_tag.id',
#                     onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
#     database_id = Column(Integer, ForeignKey(
#         'org_database.database_id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)

#     tag = relationship('DatabaseTag', back_populates='relationships')
#     database = relationship('OrgDatabase')


# class TeamMembership(Base):
#     __tablename__ = 'team_membership'

#     membership_id = Column(Integer, primary_key=True,
#                            unique=True, nullable=False)
#     member_id = Column(Integer, ForeignKey(
#         'personal_profile.profile_id', onupdate="CASCADE", ondelete="RESTRICT"))
#     team_id = Column(Integer, ForeignKey(
#         'team_profile.profile_id', onupdate="CASCADE", ondelete="RESTRICT"))

#     member = relationship('PersonalProfile', back_populates='memberships')
#     team = relationship('TeamProfile', back_populates='memberships')
