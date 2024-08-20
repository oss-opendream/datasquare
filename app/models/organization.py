''' 회사 내 DB와 관련된 metadata 관리 테이블에 대한 객체를 정의하기 위한 모듈 '''


from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.models.database import Base, datasquare_db


# Base.metadata.create_all(bind=datasquare_db.engine)


class OrgDatabase(Base):
    __tablename__ = 'org_database'

    database_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    database = Column(String, unique=True, nullable=False)

    # Relationships
    tables_re = relationship('OrgDatabaseTable', back_populates='database_re')
    tags_re = relationship('DatabaseTagRelationship', back_populates='database_re')

class OrgDatabaseTable(Base):
    __tablename__ = 'org_database_table'

    table_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    table_name = Column(String, nullable=False)
    within_db = Column(Integer, ForeignKey('org_database.database_id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)

    # Relationships
    database_re = relationship('OrgDatabase', back_populates='tables_re')

class DatabaseTag(Base):
    __tablename__ = 'database_tag'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    tag_name = Column(String, unique=True, nullable=False)

    # Relationships
    relationships_re = relationship('DatabaseTagRelationship', back_populates='tag_re')

class DatabaseTagRelationship(Base):
    __tablename__ = 'database_tag_relationship'

    relationship_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    tag_id = Column(Integer, ForeignKey('database_tag.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    database_id = Column(Integer, ForeignKey('org_database.database_id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)

    # Relationships
    tag_re = relationship('DatabaseTag', back_populates='relationships_re')
    database_re = relationship('OrgDatabase', back_populates='tags_re')