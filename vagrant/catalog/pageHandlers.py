import random, string

from flask import request, render_template, redirect, url_for
from flask import session as login_session
from database_setup import Category, Item
from dbUtils import DBOperations

dbOperations = DBOperations()

clientID = "433420290668-lohrcharee0mud3j66f8j0eful3nb3f2.apps.googleusercontent.com"

# Login Page
def loginPage():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('loginpage.html', clientID = clientID, STATE = state)


# DashBoard
def dashboardPage():
    categories = dbOperations.fetchCategories()
    return render_template('dashboard.html', categories=categories)


# Create a Category
def addCategoryPage():
    if request.method == 'POST':
        categoryToAdd = Category(name=request.form.get('categoryName'))
        dbOperations.addCategory(categoryToAdd)
        
        return redirect(url_for('dashboard'))
    
    else:
        return render_template('addEditCategory.html', operation = "Add", category = None)

# Update a Category
def editCategoryPage(categoryIDToEdit):
    if request.method == 'POST':
        categoryID = request.form.get('categoryID')
        categoryInstance = Category(name = request.form.get('categoryName'))
        category = dbOperations.editCategory(categoryID, categoryInstance)
        
        return redirect(url_for('dashboard'))
    else:
        category = dbOperations.fetchCategory(categoryIDToEdit)
        return render_template('addEditCategory.html', operation = "Edit", category = category)

# Delete a Category
def deleteCategoryPage(categoryID):
    if(dbOperations.deleteCategory(categoryID)):
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('dashboard'))
    
    
# Add an Item
def addItemPage():
    if request.method == 'POST':
        categoryID = request.form.get('categoryID')
        itemName = request.form.get('itemName')
        itemDescription = request.form.get('itemDescription')
        
        itemToAdd = Item(name=itemName, description=itemDescription)
        dbOperations.addItem(categoryID, itemToAdd)
        
        return redirect(url_for('viewItems', categoryID = categoryID))
    
    else:
        if(request.args.get('selectedCategory')):
            selectedCategory = request.args.get('selectedCategory')
            categories = dbOperations.fetchCategories()
            return render_template('addEditItem.html', categories=categories, selectedCategory=selectedCategory, 
                                   item=None, operation="Add")
        else:
            categories = dbOperations.fetchCategories()
            return render_template('addEditItem.html', categories=categories, selectedCategory=None, item=None,
                                   operation="Add")


# Read Items in a Category   
def viewItemsPage(categoryID):
    categories = dbOperations.fetchCategories()
    items = dbOperations.fetchItemsInCategory(categoryID)
    category = dbOperations.fetchCategory(categoryID)
    return render_template('itemsInCategory.html', categories=categories, items=items,
                           category=category)

# Update an Item
def editItemPage(itemIDToEdit):
    if request.method == 'POST':
        categoryID = request.form.get('categoryID')
        itemID = request.form.get('itemID')
        itemInstance = Item(name = request.form.get('itemName'),
                            description = request.form.get('itemDescription'),
                            category_id = categoryID)
        dbOperations.editItem(itemID, itemInstance)
        
        return redirect(url_for('viewItems', categoryID = categoryID))
    else:
        item = dbOperations.fetchItem(itemIDToEdit)
        categories = dbOperations.fetchCategories()
        return render_template('addEditItem.html', operation = "Edit", item = item, 
                               categories=categories, selectedCategory = item.category_id)

# Delete an Item
def deleteItemPage(itemID):
    item = dbOperations.fetchItem(itemID)
    categoryID = item.category_id
    if(dbOperations.deleteItem(itemID)):
        return redirect(url_for('viewItems', categoryID = categoryID))
    else:
        return redirect(url_for('viewItems', categoryID = item.category_id))
