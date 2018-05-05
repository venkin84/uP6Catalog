from sqlalchemy import Column, ForeignKey, Integer, String
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


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(500), nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow())
    category_id = Column(Integer, ForeignKey('category.id'))
    
    @property
    def serialize(self):
        return {
           'id'          : self.id,
           'name'        : self.name,
           'description' : self.description,
           'category'    : self.category_id,
           'created_date': [self.created_date.strftime("%Y-%m-%d"), self.created_date.strftime("%H:%M:%S")]
        }
    
class User(Base):
    __tablename__ = 'users'
    
    name = Column(String(150), nullable=False)
    email_address = Column(String(250), nullable=False, primary_key=True)
    is_admin = Column(Boolean, default=False)

engine = create_engine('postgresql://vagrant:root@localhost:5432/vagrant')
Base.metadata.create_all(engine)
