from typing import Optional, Union
from database.models import User, Base
from config import DB_PORT, DB_HOST, DB_PASS, DB_USER, DB_NAME, DB_ADAPTER
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


path = f"{DB_ADAPTER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(path)
Base.metadata.create_all(engine)


def with_session(func):
    def wrapper(*args, **kwargs):
        with sessionmaker(bind=engine)() as session:
            return func(session=session, *args, **kwargs)
    return wrapper


class DataBase:
    @staticmethod
    @with_session
    def get_user_tgid(userid: str, session: Session = None) -> Optional[str]:
        user = session.query(User).filter_by(userid=userid).first()
        return None if user is None else user.tgid

    @staticmethod
    @with_session
    def add_tgid_to_user(userid: str, tgid: Union[str, int], session: Session = None) -> bool:
        user = session.query(User).filter_by(userid=str(userid)).first()
        if user is None:
            return False
        user.tgid = tgid
        session.commit()
        return True

    @staticmethod
    @with_session
    def add_userid(userid: str, session: Session = None):
        user = session.query(User).filter_by(userid=userid).first()
        if user is None:
            session.add(User(userid=userid))
            session.commit()
            return True
        return False


    @staticmethod
    @with_session
    def check_user(userid: str, session: Session = None) -> Optional[User]:
        return session.query(User).filter_by(userid=userid).first()
