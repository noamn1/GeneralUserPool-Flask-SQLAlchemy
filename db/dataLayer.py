import io
import os

from flask import send_file
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.user import User


class DataLayer:

    def __connect(self):
        self._engine = create_engine('mysql+pymysql://root:Q1w2e3r4@localhost/General_User_Pool')
        self._Session = sessionmaker(bind=self._engine)

    def __init__(self):
        self.__connect()

    def get_user_by_email(self, email):
        session = self._Session()
        user = session.query(User).filter_by(email=email).first()
        print(user)
        return user

    def get_all_users(self):
        session = self._Session()
        users = session.query(User).all()
        print(users)
        return users


