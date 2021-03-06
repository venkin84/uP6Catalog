from flask import jsonify

from dbHandlers.dbUtils import DBOperations

dbOperations = DBOperations()


# View an Item
def viewAnItem(itemID):
    item = dbOperations.fetchItem(itemID)
    return jsonify(item.serialize)
