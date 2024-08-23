'''
서비스 메타데이터 데이터베이스 및 외부 데이터베이스 연결을 위한 
SQLAlchemy Engine 객체 생성 및 세션 관리 모듈
'''


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATASQUARE_DATABASE_URI = 'sqlite:///models/dsdb.db'
# ORG_DATABASE_URI = 'postgre://'


class Database:
    '''
    데이터베이스 연결을 위한 engine 객체, connection pool을 생성하는 class

    Args:
        param db_uri: 연결할 database URI
    '''

    def __init__(self, db_uri):
        self.db_uri = db_uri
        self.engine = create_engine(self.db_uri)
        self.sessionlocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    def get_db(self):
        '''
        DB 세션 관리 함수
        '''

        db = self.sessionlocal()
        try:
            yield db
        finally:
            db.close()


Base = declarative_base()

datasquare_db = Database(DATASQUARE_DATABASE_URI)
# org_db = Database(ORG_DATABASE_URI).get_db()
