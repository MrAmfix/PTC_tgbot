from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    userid = Column(String, primary_key=True)
    tgid = Column(String)
    name = Column(String)

    def __repr__(self):
        return f'Users(userid = {self.userid}, tgid = {self.tgid}, name = {self.name})'
