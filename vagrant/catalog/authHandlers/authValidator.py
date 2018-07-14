from flask import request, url_for, redirect
from functools import wraps
from gLogin import GLogin, IdentityServer
from dbHandlers.dbUtils import DBOperations

dbOperation = DBOperations()

def validateUser(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if ('idServer' in request.cookies):
            if (request.cookies['idServer'] == str(IdentityServer.google)):
                if ('aToken' in request.cookies):
                    accessToken = request.cookies['aToken']
                    userEmail = GLogin.validateGToken(accessToken)
                    print userEmail
                    if userEmail:
                        user = dbOperation.fetchUser(userEmail)
                        return fn(user, *args, **kwargs)
                    else:
                        # Invalid access token Error need to retry Logging In
                        return fn(user=None, *args, **kwargs)
                else:
                    # Check if rToken is there
                    if ('rToken' in request.cookies):
                        return redirect(url_for('gLogin'))

                    # User not Logged In Error
                    return fn(user=None, *args, **kwargs)
            else:
                # Temporary placeholder to add other auth services
                return redirect(url_for('dashboard'))
        else:
            # User not Logged In Error
            return fn(user=None, *args, **kwargs)
    return wrapper



