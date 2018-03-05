from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from database_setup import Category
from database_setup import Item

Base = declarative_base()
engine = create_engine('postgresql://vagrant:root@localhost:5432/vagrant')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

class DBOperations ():
    
    def createOperation(self, instance):
        session = Session()
        session.add(instance)
        session.commit()
        
    def createItem (self):
        item = Item(name="Snowboard", description="It is a snowboard")
        session = Session()
        category = session.query(Category).filter(Category.name == "Snowboarding")
        item.category_id = category[0].id
        session.add(item)
        session.commit()