# model.py
import os

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Sequence

try:
    url = os.environ.get('DATABASE_URL')
    url = url.split('postgres://')[1]
    engine = create_engine('postgresql+psycopg2://oywafgwhonrxjc'
                           ':1fb26b2f767713170d4a21a7a92edcf077c34b0ebdc0f0ac5f2958005bdb35c0@ec2-52-19-170-215.eu'
                           '-west-1.compute.amazonaws.com:5432/dajoliaojhf3su'.format(url),
                           convert_unicode=True, encoding='utf8')
except:
    print('Something wrong with database url')
else:
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False, bind=engine))
    Base = declarative_base()
    Base.query = db_session.query_property()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, Sequence('user_id'), primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), unique=True, nullable=False)
    name = Column(String(20), unique=False, nullable=False)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    new_user = User(username='guest',
                    password='guest',
                    name='Genius')
    db_session.add(new_user)
    db_session.commit()
