from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from model.outputMixin import OutputMixin

Base = declarative_base()


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    des = Column(String)

    def to_json(self):
        return {"name":self.name, "des": self.des}

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    roles = relationship(Role, secondary='users_roles')

    def to_json(self):
        roles = []
        for r in self.roles:
            roles.append(r.to_json())

        return {"first_name": self.first_name, "last_name":self.last_name,
                "email": self.email, "roles": roles}

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class UserRole(Base):
   __tablename__ = 'users_roles'
   user_id = Column(
      Integer,
      ForeignKey('users.id'),
      primary_key=True)

   role_id = Column(
      Integer,
      ForeignKey('roles.id'),
      primary_key=True)