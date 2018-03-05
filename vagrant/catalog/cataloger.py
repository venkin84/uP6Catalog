from flask import Flask
from pageHandlers import dashboardPage, addCategoryPage

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def dashboard():
    return dashboardPage()

@app.route('/category/add', methods = ['GET', 'POST'])
def addCategory():
    return addCategoryPage()


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
