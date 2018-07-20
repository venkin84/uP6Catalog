from flask import Flask, redirect, url_for, request

from pageHandlers import dashboardPage, addCategoryPage, editCategoryPage, \
    deleteCategoryPage, loginPage
from pageHandlers import addItemPage, viewItemsPage, editItemPage, \
    deleteItemPage
from apiHandlers import viewAnItem
from authHandlers.gLogin import GLogin, IdentityServer
from authHandlers.authValidator import validateUser

import os

app = Flask(__name__)


# Login Related Links
@app.route('/login', methods=['GET'])
def login():
    return loginPage()


@app.route('/logout', methods=['GET'])
def logout():
    if ('idServer' in request.cookies):
        if (request.cookies['idServer'] == str(IdentityServer.google)):
            return redirect(url_for('gRevoke'))
        else:
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('dashboard'))


# For Google Authentication
@app.route('/gLogin')
def gLogin():
    return GLogin.authorize()


@app.route('/gOAuth2Callback')
def gOAuth2Callback():
    return GLogin.oauth2CallbackHandler()


@app.route('/gRevoke')
def gRevoke():
    return GLogin.oauth2RevokeHandler()


# Dashboard Page
@app.route('/', methods=['GET'])
@validateUser
def dashboard(user):
    return dashboardPage(user)


# Add a Category
@app.route('/category/add', methods=['GET', 'POST'])
@validateUser
def addCategory(user):
    return addCategoryPage(user)


# View Items in a Category
@app.route('/category/<categoryID>/items/view', methods=['GET'])
@validateUser
def viewItems(user, categoryID):
    return viewItemsPage(user, categoryID)


# Edit a Category
@app.route('/category/<categoryID>/edit', methods=['GET', 'POST'])
@validateUser
def editCategory(user, categoryID):
    return editCategoryPage(user, categoryID)


# Delete a Category
@app.route('/category/<categoryID>/delete', methods=['GET'])
@validateUser
def deleteCategory(user, categoryID):
    return deleteCategoryPage(user, categoryID)


# Add an Item
@app.route('/item/add', methods=['GET', 'POST'])
@validateUser
def addItem(user):
    return addItemPage(user)


# View an Item API
@app.route('/item/<itemID>/view', methods=['GET'])
def viewItem(itemID):
    return viewAnItem(itemID)


# Edit an Item
@app.route('/item/<itemID>/edit', methods=['GET', 'POST'])
@validateUser
def editItem(user, itemID):
    return editItemPage(user, itemID)


# Delete an Item
@app.route('/item/<itemID>/delete', methods=['GET'])
@validateUser
def deleteItem(user, itemID):
    return deleteItemPage(user, itemID)


if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
