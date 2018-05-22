from flask import Flask

from pageHandlers import dashboardPage, addCategoryPage, editCategoryPage, deleteCategoryPage, loginPage
from pageHandlers import addItemPage, viewItemsPage, editItemPage, deleteItemPage
from apiHandlers import viewAnItem
from gloginHandlers import gAuthorize, gOAuth2CallbackHandler, gOAuth2RevokeHandler

import os

app = Flask(__name__)


# Login Related Links
@app.route('/login', methods=['GET'])
def login():
    return loginPage()

# For Google Authentication
@app.route('/gLogin')
def gLogin():
    return gAuthorize()


@app.route('/gOAuth2Callback')
def gOAuth2Callback():
    return gOAuth2CallbackHandler()


@app.route('/gRevoke')
def gRevoke():
    return gOAuth2RevokeHandler()





# Dashboard Page
@app.route('/', methods=['GET'])
def dashboard():
    return dashboardPage()


# Add a Category
@app.route('/category/add', methods=['GET', 'POST'])
def addCategory():
    return addCategoryPage()


# View Items in a Category
@app.route('/category/<categoryID>/items/view', methods=['GET'])
def viewItems(categoryID):
    return viewItemsPage(categoryID)


# Edit a Category
@app.route('/category/<categoryID>/edit', methods=['GET', 'POST'])
def editCategory(categoryID):
    return editCategoryPage(categoryID)


# Delete a Category
@app.route('/category/<categoryID>/delete', methods=['GET'])
def deleteCategory(categoryID):
    return deleteCategoryPage(categoryID)


# Add an Item
@app.route('/item/add', methods=['GET', 'POST'])
def addItem():
    return addItemPage()


# View an Item API
@app.route('/item/<itemID>/view', methods=['GET'])
def viewItem(itemID):
    return viewAnItem(itemID)


# Edit an Item
@app.route('/item/<itemID>/edit', methods=['GET', 'POST'])
def editItem(itemID):
    return editItemPage(itemID)


# Delete an Item
@app.route('/item/<itemID>/delete', methods=['GET'])
def deleteItem(itemID):
    return deleteItemPage(itemID)


if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
