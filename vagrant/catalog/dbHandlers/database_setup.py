from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import Sequence
from sqlalchemy.sql.sqltypes import DateTime, Boolean
import datetime

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, Sequence('category_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow())
    items = relationship("Item", cascade="all, delete, delete-orphan")
    user_id = Column(String(150), ForeignKey('users.email_address'))


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(500), nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow())
    category_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(String(150), ForeignKey('users.email_address'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category_id,
            'user': self.user_id,
            'created_date': [self.created_date.strftime("%Y-%m-%d"),
                             self.created_date.strftime("%H:%M:%S")]
        }


class User(Base):
    __tablename__ = 'users'

    name = Column(String(150), nullable=False)
    email_address = Column(String(250), nullable=False, primary_key=True)
    identity_server = Column(Integer, nullable=False)
    role = Column(Integer, default=1)
    items = relationship("Category", cascade="all, delete, delete-orphan")
    items = relationship("Item", cascade="all, delete, delete-orphan")


engine = create_engine('postgresql://vagrant:root@localhost:5432/vagrant')
Base.metadata.create_all(engine)


class IdentityServer(Enum):
    google = 1
    facebook = 2


class UserRole(Enum):
    user = 1
    admin = 2
