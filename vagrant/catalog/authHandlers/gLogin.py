from flask import request, redirect, url_for, make_response, jsonify
from flask import session
import requests
from dbHandlers.dbUtils import DBOperations
import time
from datetime import datetime
import calendar
import json
from dbHandlers.database_setup import IdentityServer, User, UserRole

import google_auth_oauthlib.flow


class GLogin:
    dbOperations = DBOperations()

    CLIENT_SECRETS_FILE = "authHandlers/gSecret.json"
    SCOPES = ['https://www.googleapis.com/auth/userinfo.email',
              'https://www.googleapis.com/auth/userinfo.profile']

    @staticmethod
    def authorize():
        if ('rToken' in request.cookies):
            accessToken, expires_in = GLogin.oauth2RefreshToken()
            response = make_response(redirect(url_for('dashboard')))
            if (accessToken is not None):
                print accessToken + "  " + str(expires_in)
                response.set_cookie('aToken', value=accessToken,
                                    max_age=int(expires_in))
                response.set_cookie('idServer',
                                    value=str(IdentityServer.google))
            return response
        else:
            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                GLogin.CLIENT_SECRETS_FILE, scopes=GLogin.SCOPES)

            flow.redirect_uri = url_for('gOAuth2Callback', _external=True)

            # Without prompt='consent' (apart from access_type='offline')
            # refresh token is not returned
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent')

            session['state'] = state
            return redirect(authorization_url)

    @staticmethod
    def oauth2CallbackHandler():
        state = session['state']
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            GLogin.CLIENT_SECRETS_FILE,
            scopes=GLogin.SCOPES,
            state=state)
        flow.redirect_uri = url_for('gOAuth2Callback', _external=True)

        # Use the authorization server's response to fetch the OAuth 2.0
        # tokens.
        authorization_response = request.url
        flow.fetch_token(code=request.args["code"])
        credentials = flow.credentials

        response = make_response(redirect(url_for('dashboard')))

        # Validating the ID Token
        payload = {'access_token': credentials.token}
        valResponse = requests.get(
            'https://www.googleapis.com/oauth2/v3/tokeninfo', params=payload)

        if (valResponse.status_code == 200):
            valToken = valResponse.json()

            response.set_cookie('aToken', value=credentials.token,
                                max_age=int(valToken['expires_in']))
            response.set_cookie('rToken',
                                value=credentials.refresh_token,
                                expires=time.mktime(
                                    GLogin.utc_afterMonths(6).timetuple()))
            response.set_cookie('idServer',
                                value=str(IdentityServer.google),
                                expires=time.mktime(
                                    GLogin.utc_afterMonths(6).timetuple()))

        userProfile = requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo', params=payload)
        profile = userProfile.json()
        user = User(name=profile["name"],
                    email_address=profile["email"],
                    identity_server=IdentityServer.google,
                    role=UserRole.user)
        if not GLogin.dbOperations.fetchUser(user.email_address):
            GLogin.dbOperations.addUser(user)
        return response

    @staticmethod
    def oauth2RefreshToken():
        credentials = None
        with open(GLogin.CLIENT_SECRETS_FILE) as cred:
            credentials = json.load(cred)
        print credentials['web']['client_id']
        payload = (
            ('refresh_token', request.cookies['rToken']),
            ('client_id', credentials['web']['client_id']),
            ('client_secret', credentials['web']['client_secret']),
            ('grant_type', 'refresh_token'))
        resp = requests.post('https://www.googleapis.com/oauth2/v4/token',
                             data=payload)
        if (resp.status_code == 200):
            r = resp.json()
            print r
            return r['access_token'], r['expires_in']
        else:
            print "Response: " + resp.status_code
            return None, None

    @staticmethod
    def oauth2RevokeHandler():
        response = make_response(redirect(url_for('dashboard')))

        if ('aToken' in request.cookies):
            revokeResp = requests.post(
                'https://accounts.google.com/o/oauth2/revoke',
                params={'token': request.cookies['aToken']})
        elif ('rToken' in request.cookies):
            revokeResp = requests.post(
                'https://accounts.google.com/o/oauth2/revoke',
                params={'token': request.cookies['rToken']})
        else:
            return response

        if revokeResp.status_code == 200:
            response.set_cookie('aToken', value='', expires=0)
            response.set_cookie('rToken', value='', expires=0)
            response.set_cookie('idServer', value='', expires=0)
            return response
        elif revokeResp.status_code == 400:
            return response
        else:
            return response

    @staticmethod
    def utc_afterMonths(months):
        currentDateTime = datetime.utcnow()
        month = currentDateTime.month - 1 + months
        year = currentDateTime.year + month // 12
        month = month % 12 + 1
        day = min(currentDateTime.day, calendar.monthrange(year, month)[1])
        newDateTime = currentDateTime.replace(year=year, month=month, day=day)
        return newDateTime

    @staticmethod
    def validateGToken(access_token):
        payload = {'access_token': access_token}
        response = requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo', params=payload)
        if (response.status_code == 200):
            respData = response.json()
            return respData['email']
        else:
            return None
