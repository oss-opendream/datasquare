'''
    Issue와 관련된 metadata 관리 테이블에 대한 객체를 정의하기 위한 모듈
'''
from sqlalchemy import Column, Integer, ForeignKey, Text, String
from sqlalchemy.orm import relationship

from app.models.database import Base, datasquare_db


Base.metadata.create_all(bind=datasquare_db.engine)


class Issue(Base):
    '''
    "issue" 테이블에 대한 객체를 정의하는 class
    '''
    __tablename__ = 'issue'

    issue_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    publisher_id = Column(Integer,
                          ForeignKey(
                              'personal_profile.profile_id',
                              onupdate='CASCADE',
                              ondelete='RESTRICT'
                          ),
                          nullable=False)
    requested_team = Column(Integer, nullable=False)
    is_private = Column(Integer, nullable=False)
    created_at = Column(String, nullable=False)
    modified_at = Column(String, nullable=False)

    publisher = relationship(
        'PersonalProfile', back_populates='issues_published')
    issue_comments = relationship(
        'IssueComment', back_populates='commented_issue')


class IssueComment(Base):
    '''
    "issue_comment" 테이블에 대한 객체를 정의하는 class
    '''
    __tablename__ = 'issue_comment'

    comment_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    publisher_id = Column(Integer,
                          ForeignKey(
                              'personal_profile.profile_id',
                              onupdate='CASCADE',
                              ondelete='RESTRICT'
                          ),
                          nullable=False)
    within = Column(Integer,
                    ForeignKey(
                        'issue.issue_id',
                        onupdate='CASCADE',
                        ondelete='CASCADE'  # ondelete에 대한 옵션 논의 필요
                    ),
                    nullable=False)
    content = Column(Text, nullable=False)

    publisher = relationship(
        'PersonalProfile', back_populates='comments_published')
    commented_issue = relationship(
        'Issue', back_populates='issue_comments')
