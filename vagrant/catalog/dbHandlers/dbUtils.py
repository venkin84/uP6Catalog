from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import desc

from database_setup import Category, Item, User, UserRole

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
        return session.query(Category).filter(Category.id == categoryID).first()
    
    def editCategory(self, categoryID, categoryInstance):
        category = session.query(Category).filter(Category.id == categoryID).first()
        category.name = categoryInstance.name
        session.commit()
        return True
    
    def deleteCategory (self, categoryID):
        categoryToDelete = session.query(Category).filter(Category.id == categoryID).first()
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

    def fetchLatestItems (self):
        return session.query(Item).order_by(desc(Item.created_date)).limit(9)
    
    def fetchItem (self, itemID):
        return session.query(Item).filter(Item.id == itemID).first()
    
    def editItem(self, itemID, itemInstance):
        item = session.query(Item).filter(Item.id == itemID).first()
        item.name = itemInstance.name
        item.description = itemInstance.description
        item.category_id = itemInstance.category_id
        session.commit()
        return True
    
    def deleteItem (self, itemID):
        itemToDelete = session.query(Item).filter(Item.id == itemID).first()
        session.delete(itemToDelete)
        session.commit()
        return True
    
    
    # CRUDL Operations for Users Table
    
    def addUser (self, userInstance):
        session.add(userInstance)
        session.commit()
        return True
    
    def fetchUser (self, email_address):
        return session.query(User).filter(User.email_address == email_address).first()
    
    def isUserAdmin(self, email_address):
        user = session.query(User).filter(User.email_address == email_address).first()
        if user != None:
            if user.role == UserRole.admin:
                return True
        return False

    def setUserAdmin (self, email_address):
        user = session.query(User).filter(User.email_address == email_address).first()
        if not user:
            return False
        else:
            if not (user.role == UserRole.admin):
                user.role = UserRole.admin
                session.commit()
            return True

            
            
