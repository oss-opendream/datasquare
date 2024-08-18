''' Issue와 관련된 metadata 관리 테이블에 대한 객체를 정의하기 위한 모듈 '''


from sqlalchemy import Column, Integer, ForeignKey, Text, String
from sqlalchemy.orm import relationship

from app.models.database import Base, datasquare_db


Base.metadata.create_all(bind=datasquare_db.engine)


class Issue(Base):
    __tablename__ = 'issue'

    issue_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    publisher = Column(Integer, ForeignKey('personal_profile.profile_id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    requested_team = Column(Integer, ForeignKey('team_profile.profile_id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    is_private = Column(Integer, nullable=False)
    created_at = Column(Text, nullable=False)
    modified_at = Column(Text, nullable=False)

    # Relationships
    publisher = relationship('PersonalProfile', back_populates='issues')
    requested_team = relationship('TeamProfile', back_populates='issues')
    comments = relationship('IssueComment', back_populates='issue')

class IssueComment(Base):
    __tablename__ = 'issue_comment'

    comment_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    publisher = Column(Integer, ForeignKey('personal_profile.profile_id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    within = Column(Integer, ForeignKey('issue.issue_id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    content = Column(Text, nullable=False)

    # Relationships
    publisher = relationship('PersonalProfile', back_populates='comments')
    issue = relationship('Issue', back_populates='comments')