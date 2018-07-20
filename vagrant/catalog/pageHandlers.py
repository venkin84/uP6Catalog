from flask import request, render_template, redirect, url_for, make_response
from dbHandlers.database_setup import Category, Item
from dbHandlers.dbUtils import DBOperations

dbOperations = DBOperations()


# Login Page
def loginPage():
    print request.cookies.get('aToken')
    return render_template('loginpage.html')


# DashBoard
def dashboardPage(user):
    categories = dbOperations.fetchCategories()
    items = dbOperations.fetchLatestItems()
    response = make_response(render_template('dashboard.html',
                                             user=user,
                                             categories=categories,
                                             items=items))
    return response


# Create a Category
def addCategoryPage(user):
    if user:
        if request.method == 'POST':
            categoryToAdd = Category(name=request.form.get('categoryName'),
                                     user_id=user.email_address)
            dbOperations.addCategory(categoryToAdd)

            return redirect(url_for('dashboard'))

        else:
            return render_template('addEditCategory.html',
                                   user=user,
                                   operation="Add",
                                   category=None)
    else:
        return redirect(url_for('dashboard'))


# Update a Category
def editCategoryPage(user, categoryIDToEdit):
    category = dbOperations.fetchCategory(categoryIDToEdit)
    if (user.email_address == category.user_id) or (user.role == 2):
        if request.method == 'POST':
            categoryID = request.form.get('categoryID')
            categoryInstance = Category(name=request.form.get('categoryName'))
            dbOperations.editCategory(categoryID, categoryInstance)
            return redirect(url_for('dashboard'))
        else:
            return render_template('addEditCategory.html',
                                   operation="Edit",
                                   category=category,
                                   user=user)
    else:
        return redirect(url_for('dashboard'))


# Delete a Category
def deleteCategoryPage(user, categoryID):
    category = dbOperations.fetchCategory(categoryID)
    if (user.email_address == category.user_id) or (user.role == 2):
        if (dbOperations.deleteCategory(categoryID)):
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('dashboard'))


# Add an Item
def addItemPage(user):
    if user:
        if request.method == 'POST':
            categoryID = request.form.get('categoryID')
            itemName = request.form.get('itemName')
            itemDescription = request.form.get('itemDescription')
            itemToAdd = Item(name=itemName, description=itemDescription,
                             user_id=user.email_address)
            dbOperations.addItem(categoryID, itemToAdd)
            return redirect(url_for('viewItems', categoryID=categoryID))

        else:
            if (request.args.get('selectedCategory')):
                selectedCategory = request.args.get('selectedCategory')
                categories = dbOperations.fetchCategories()
                return render_template('addEditItem.html',
                                       categories=categories,
                                       selectedCategory=selectedCategory,
                                       item=None,
                                       operation="Add",
                                       user=user)
            else:
                categories = dbOperations.fetchCategories()
                return render_template('addEditItem.html',
                                       categories=categories,
                                       selectedCategory=None,
                                       item=None,
                                       operation="Add",
                                       user=user)
    else:
        return redirect(url_for('dashboard'))


# Read Items in a Category   
def viewItemsPage(user, categoryID):
    categories = dbOperations.fetchCategories()
    items = dbOperations.fetchItemsInCategory(categoryID)
    category = dbOperations.fetchCategory(categoryID)
    return render_template('itemsInCategory.html',
                           categories=categories,
                           items=items,
                           category=category,
                           user=user)


# Update an Item
def editItemPage(user, itemIDToEdit):
    item = dbOperations.fetchItem(itemIDToEdit)
    if (item.user_id == user.email_address) or (user.role == 2):
        if request.method == 'POST':
            categoryID = request.form.get('categoryID')
            itemID = request.form.get('itemID')
            itemInstance = Item(name=request.form.get('itemName'),
                                description=request.form.get(
                                    'itemDescription'),
                                category_id=categoryID,
                                user_id=user.email_address)
            dbOperations.editItem(itemID, itemInstance)
            return redirect(url_for('viewItems', categoryID=categoryID))
        else:
            categories = dbOperations.fetchCategories()
            return render_template('addEditItem.html',
                                   operation="Edit",
                                   item=item,
                                   categories=categories,
                                   selectedCategory=item.category_id,
                                   user=user)
    else:
        return redirect(url_for('dashboard'))


# Delete an Item
def deleteItemPage(user, itemID):
    item = dbOperations.fetchItem(itemID)
    if (user.role == 2 or user.email_address == item.user_id):
        item = dbOperations.fetchItem(itemID)
        categoryID = item.category_id
        if (dbOperations.deleteItem(itemID)):
            return redirect(url_for('viewItems', categoryID=categoryID))
        else:
            return redirect(url_for('viewItems', categoryID=item.category_id))
    else:
        return redirect(url_for('dashboard'))
