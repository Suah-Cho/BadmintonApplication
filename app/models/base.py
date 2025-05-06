from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

# Reflect 옵션 설정
metadata = MetaData()
Base = declarative_base(metadata=metadata)


def reflect_tables(engine):
    """
    기존 데이터베이스 테이블을 반영
    """
    metadata.reflect(bind=engine)
