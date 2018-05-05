from flask import request, render_template, redirect, url_for
from flask import session as login_session
import requests
from database_setup import User
from dbUtils import DBOperations

import google.oauth2.credentials
import google_auth_oauthlib.flow

dbOperations = DBOperations()

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['profile', 'email']

SECRET_KEY = "super_secret_key"

def authPage():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)
    
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    
    login_session['state'] = state
    return redirect(authorization_url)


def oauth2callback():
    state = login_session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    login_session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('dashboard'))


def authRevoke():
    if 'credentials' not in login_session:
        return ('You need to <a href="/authorize">authorize</a> before ' + 'testing the code to revoke credentials.')

    credentials = google.oauth2.credentials.Credentials(**login_session['credentials'])

    revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
                           params={'token': credentials.token},
                           eaders={'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        del login_session['credentials']
        return ('Credentials successfully revoked...')
    else:
        return('An error occurred...')
    

    

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}