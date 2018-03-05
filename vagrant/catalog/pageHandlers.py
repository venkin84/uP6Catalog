from flask import request, render_template, redirect, url_for
from database_setup import Category
from dbUtils import DBOperations

dbOperations = DBOperations()

def addCategoryPage():
    if request.method == 'POST':
        category_to_add = Category(name = request.form.get('categoryName'))
        dbOperations.createOperation(category_to_add)
        return redirect(url_for('dashboard'))
    else:
        return render_template('addCategory.html')
    
def dashboardPage():
    return render_template('dashboard.html')