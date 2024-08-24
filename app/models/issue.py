'''Issue와 관련된 metadata 관리 테이블에 대한 객체를 정의하기 위한 모듈'''


from sqlalchemy import Column, Integer, ForeignKey, Text, String
from sqlalchemy.orm import relationship

from app.models.database import Base


class Issue(Base):
    ''''issue' 테이블 관련 모델 class'''

    __tablename__ = 'issue'

    issue_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    publisher = Column(Integer, ForeignKey('personal_profile.profile_id',
                       onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    requested_team = Column(Integer, ForeignKey(
        'team_profile.profile_id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    is_private = Column(Integer, nullable=False)
    created_at = Column(Text, nullable=False)
    modified_at = Column(Text, nullable=False)
    is_deleted = Column(Integer, nullable=False)

    publisher_re = relationship('PersonalProfile', back_populates='issues_re')
    comments_re = relationship('IssueComment', back_populates='issue_re')


class IssueComment(Base):
    ''''issue_comment' 테이블 관련 모델 class'''

    __tablename__ = 'issue_comment'

    comment_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    publisher = Column(Integer, ForeignKey('personal_profile.profile_id',
                       onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    within = Column(Integer, ForeignKey('issue.issue_id',
                    onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    content = Column(Text, nullable=False)
    is_deleted = Column(Integer, nullable=False)

    publisher_re = relationship(
        'PersonalProfile', back_populates='comments_re')
    issue_re = relationship('Issue', back_populates='comments_re')
