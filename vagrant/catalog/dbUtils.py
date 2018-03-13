from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from database_setup import Category, Item

Base = declarative_base()
engine = create_engine('postgresql://vagrant:root@localhost:5432/vagrant')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()


class DBOperations ():
    
# CRUDL Operations for Category Table

    def addCategory(self, categoryInstance):
        session.add(categoryInstance)
        session.commit()
        return True
    
    def fetchCategories (self):
        return session.query(Category)
    
    def fetchCategory (self, categoryID):
        return session.query(Category).filter(Category.id == categoryID).one()
    
    def editCategory(self, categoryID, categoryInstance):
        category = session.query(Category).filter(Category.id == categoryID).one()
        category.name = categoryInstance.name
        session.commit()
        return True
    
    def deleteCategory (self, categoryID):
        categoryToDelete = session.query(Category).filter(Category.id == categoryID).one()
        session.delete(categoryToDelete)
        session.commit()
        return True

    
# CRUDL Operations for Item Table

    def addItem (self, categoryID, itemInstance):
        if session.query(Category).filter(Category.id == categoryID) != None:
            itemInstance.category_id = categoryID
            session.add(itemInstance)
            session.commit()
            return True
        else:
            return False
        
    def fetchItemsInCategory (self, categoryID):
        return session.query(Item).filter(Item.category_id == categoryID)
    
    def fetchItem (self, itemID):
        return session.query(Item).filter(Item.id == itemID).one()
    
    def editItem(self, itemID, itemInstance):
        category = session.query(Item).filter(Item.id == itemID).one()
        category.name = itemInstance.name
        session.commit()
        return True
    
    def deleteItem (self, itemID):
        itemToDelete = session.query(Item).filter(Item.id == itemID).one()
        session.delete(itemToDelete)
        session.commit()
        return True
