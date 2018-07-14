# ###############################
# # Decorating a decorator test #
# ###############################
#
# from functools import wraps
# from random import Random
#
# r = Random()
#
# def superDecorator(dec):
#     def wrapper(func):
#         print "SuperDecorator"
#         a = r.random()
#         return dec(func, a)
#     return wrapper
#
# @superDecorator
# def decorator(func, a):
#     @wraps(func)
#     def wrapper(var):
#         print "Decorator"
#         b = r.randint(310,440)
#         return func(var, a, b)
#     return wrapper
#
# @decorator
# def main1(var, a, b):
#     print "Test:",var, a, b
#     return None
#
# if __name__ == "__main__":
#     main1("00")
#     main1("01")


# ###########################################################################
# # Decorator chaining with parameter passing from one to another decorator #
# ###########################################################################
#
# from functools import wraps
# from random import Random
#
# r = Random()
#
# def decFunc1(func, decFuncs, *args, **kwargs):
#     print "AddOnDecorator1"
#     b = r.randint(310, 440)
#     if (decFuncs is None):
#         return func(b, *args, **kwargs)
#     else:
#         decFunc = decFuncs[0]
#         if (len(decFuncs) > 1):
#             del decFuncs[0]
#             print decFuncs[0]
#             return decFunc(func, decFuncs, b, *args, **kwargs)
#         else:
#             return decFunc(func, None, b, *args, **kwargs)
#
# def decFunc2(func, decFuncs, *args, **kwargs):
#     print "AddOnDecorator2"
#     c = r.random()
#     if (decFuncs is None):
#         return func(c, *args, **kwargs)
#     else:
#         decFunc = decFuncs[0]
#         if (len(decFuncs) > 1):
#             del decFuncs[0]
#             print decFuncs[0]
#             return decFunc(func, decFuncs, c, *args, **kwargs)
#         else:
#             return decFunc(func, None, c, *args, **kwargs)
#
# addOns = [decFunc1, decFunc2]
#
# def decorator(decFuncs):
#     def dec(func):
#         def wrapper(var):
#             print "Decorator"
#             a = r.random()
#             if (decFuncs is None):
#                 return func(a, var)
#             else:
#                 decFuncsCopy = list(decFuncs)
#                 decFunc = decFuncsCopy[0]
#                 print decFunc
#                 if(len(decFuncsCopy) > 1):
#                     del decFuncsCopy[0]
#                     print decFuncsCopy[0]
#                     return decFunc(func, decFuncsCopy, a, var)
#                 else:
#                     return decFunc(func, None, a, var)
#         return wrapper
#     return dec
#
# @decorator(addOns)
# def main1(*args):
#     print "Test:", args
#     return None
#
# if __name__ == "__main__":
#     main1("00")
#     main1("01")


# #############
# # Enum Test #
# #############
#
# import enum
#
# class authProvider (enum.Enum):
#     google = 1
#     facebook = 2
#
#
# def main():
#     e = authProvider.google
#
#     if (e == 1):
#         print "It is Google"
#     else:
#         print "It is Facebook"
#
# if __name__ == "__main__":
#     main()



# ##################################
# # Inserting an user in the table #
# ##################################
#
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
# from dbHandlers.dbUtils import DBOperations
#
# from dbHandlers.database_setup import User, IdentityServer, UserRole
#
# Base = declarative_base()
# engine = create_engine('postgresql://vagrant:root@localhost:5432/vagrant')
# Base.metadata.create_all(engine)
#
# DBSession = sessionmaker(bind=engine)
# session = DBSession()
#
# # identityServer = IdentityServer.google
# # role = UserRole.admin
# #
# # user = User(name = "Venky",
# #             email_address = "xyz@gmail.com",
# #             identity_server = identityServer,
# #             role = role)
# #
# # def addUser(userInfo):
# #     session.add(userInfo)
# #     session.commit()
# #     userUpdated = session.query(User).filter(User.role == role).one()
# #     print "Added User:", userUpdated.name
#
# dbOperation = DBOperations()
#
# if __name__ == "__main__":
#     # addUser(user)
#     items = dbOperation.fetchItems()
#     for item in items:
#         print item.name


# ###############################
# # Adding decorators to routes #
# ###############################
#
# from flask import Flask, redirect, url_for, make_response, request
# from functools import wraps
# import os
#
# app = Flask(__name__)
#
# def decorator(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         b = 1
#         return fn(b, *args, **kwargs)
#     return wrapper
#
# @app.route('/', methods=['GET'])
# @decorator
# def func(b):
#     print b
#     return redirect(url_for('func2', a=10, c="Error"))
#
# @app.route('/<int:a>', methods=['GET'])
# @decorator
# def func2(b, a):
#     err = ""
#     if( request.args.has_key('c')):
#         err = request.args.get('c')
#     print b, a, err
#     return str(b + a) + err
#
#
# if __name__ == '__main__':
#     os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
#     app.secret_key = 'super_secret_key'
#     app.debug = True
#     app.run(host='0.0.0.0', port=5000)

