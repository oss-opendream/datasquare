from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class OrgDatabase(Base):
    __tablename__ = 'org_database'

    database_id = Column(Integer, primary_key=True,
                         autoincrement=True, nullable=False, unique=True)
    database_name = Column(Text, nullable=False, unique=True)

    tables = relationship("OrgDatabaseTable", back_populates="database")
    tag_relationships = relationship(
        "DatabaseTagRelationship", back_populates="database")


class OrgDatabaseTable(Base):
    __tablename__ = 'org_database_table'

    table_id = Column(Integer, primary_key=True,
                      autoincrement=True, nullable=False, unique=True)
    table_name = Column(Text, nullable=False)
    within_db = Column(Integer, ForeignKey('org_database.database_id',
                       onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)

    database = relationship("OrgDatabase", back_populates="tables")
    columns = relationship("OrgDatabaseTableColumn", back_populates="table")


class OrgDatabaseTableColumn(Base):
    __tablename__ = 'org_database_table_column'

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, unique=True)
    column_name = Column(Text, nullable=False)
    ordinal_position = Column(Integer, nullable=False)
    data_type = Column(Text, nullable=False)
    within_table = Column(Integer, ForeignKey(
        'org_database_table.table_id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)

    table = relationship("OrgDatabaseTable", back_populates="columns")


class DatabaseTag(Base):
    __tablename__ = 'database_tag'

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, unique=True)
    tag_name = Column(Text, nullable=False, unique=True)

    tag_relationships = relationship(
        "DatabaseTagRelationship", back_populates="tag")


class DatabaseTagRelationship(Base):
    __tablename__ = 'database_tag_relationship'

    relationship_id = Column(Integer, primary_key=True,
                             autoincrement=True, nullable=False, unique=True)
    tag_id = Column(Integer, ForeignKey('database_tag.id',
                    onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    database_id = Column(Integer, ForeignKey(
        'org_database.database_id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)

    tag = relationship("DatabaseTag", back_populates="tag_relationships")
    database = relationship("OrgDatabase", back_populates="tag_relationships")
