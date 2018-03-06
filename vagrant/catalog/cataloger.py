from flask import Flask
from pageHandlers import dashboardPage, addCategoryPage, addItemPage, viewItemsPage, editCategoryPage

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def dashboard():
    return dashboardPage()

@app.route('/category/add', methods = ['GET', 'POST'])
def addCategory():
    return addCategoryPage()

@app.route('/category/<categoryID>/edit', methods = ['GET', 'POST'])
def editCategory(categoryID):
    return editCategoryPage(categoryID)

@app.route('/category/<categoryID>/delete', methods = ['GET'])
def deleteCategory(categoryID):
    return addCategoryPage()

@app.route('/item/add', methods = ['GET', 'POST'])
def addItem():
    return addItemPage()

@app.route('/category/<categoryID>/items/view', methods = ['GET'])
def viewItems(categoryID):
    return viewItemsPage(categoryID)

@app.route('/item/<itemID>/view', methods = ['GET', 'POST'])
def viewItem(itemID):
    return viewItemsPage(itemID)

@app.route('/item/<itemID>/edit', methods = ['GET', 'POST'])
def editItem(itemID):
    return viewItemsPage(itemID)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
