from flask import request, render_template, redirect, url_for
from database_setup import Category, Item
from dbUtils import DBOperations

dbOperations = DBOperations()


def dashboardPage():
    categories = dbOperations.fetchCategories()
    return render_template('dashboard.html', categories=categories)


def addCategoryPage():
    if request.method == 'POST':
        categoryToAdd = Category(name=request.form.get('categoryName'))
        dbOperations.addCategory(categoryToAdd)
        
        return redirect(url_for('dashboard'))
    
    else:
        return render_template('addCategory.html', operation = "Add", category = None)
    
def editCategoryPage(categoryIDToEdit):
    if request.method == 'POST':
        categoryID = request.form.get('categoryID')
        categoryInstance = Category(name = request.form.get('categoryName'))
        category = dbOperations.editCategory(categoryID, categoryInstance)
        
        return redirect(url_for('dashboard'))
    else:
        category = dbOperations.fetchCategory(categoryIDToEdit)
        return render_template('addCategory.html', operation = "Edit", category = category)


def addItemPage():
    if request.method == 'POST':
        categoryID = request.form.get('categoryID')
        itemName = request.form.get('itemName')
        itemDescription = request.form.get('itemDescription')
        
        itemToAdd = Item(name=itemName, description=itemDescription)
        dbOperations.addItem(categoryID, itemToAdd)
        
        return redirect(url_for('dashboard'))
    
    else:
        if(request.args.get('selectedCategory')):
            selectedCategory = request.args.get('selectedCategory')
            print "SELECTED CAT: " + selectedCategory
            categories = dbOperations.fetchCategories()
            return render_template('addItem.html', categories=categories, selectedCategory=selectedCategory, item=None)
        else:
            print "NO SELECTED CAT"
            categories = dbOperations.fetchCategories()
            return render_template('addItem.html', categories=categories, selectedCategory=None, item=None)

        
def viewItemsPage(categoryID):
    categories = dbOperations.fetchCategories()
    items = dbOperations.fetchItemsInCategory(categoryID)
    category = dbOperations.fetchCategory(categoryID)
    return render_template('itemsInCategory.html', categories=categories, items=items,
                           category=category)
