from sqlalchemy import Column, Integer, ForeignKey, Text, String
from sqlalchemy.orm import relationship
from app.models import database


Base = database.Base


class Issue(Base):
    __tablename__ = 'issue'

    issue_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    publisher_id = Column(Integer, ForeignKey(
        'personal_profile.profile_id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    requested_team = Column(Integer, nullable=False)
    is_private = Column(Integer, nullable=False)
    created_at = Column(String, nullable=False)
    modified_at = Column(String, nullable=False)

    publisher = relationship(
        'PersonalProfile', back_populates='issues_published')
    issue_comments = relationship(
        'IssueComment', back_populates='commented_issue')


class IssueComment(Base):
    __tablename__ = 'issue_comment'

    comment_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    publisher_id = Column(Integer, ForeignKey(
        'personal_profile.profile_id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    within = Column(Integer, ForeignKey('issue.issue_id', onupdate='CASCADE',
                    ondelete='CASCADE'), nullable=False)   # ondelete에 대한 옵션 논의 필요
    content = Column(Text, nullable=False)

    publisher = relationship(
        'PersonalProfile', back_populates='comments_published')
    commented_issue = relationship(
        'Issue', back_populates='issue_comments')
