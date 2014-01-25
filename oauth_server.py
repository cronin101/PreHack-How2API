from flask import Flask, request, redirect
from rauth import OAuth2Service
import urlparse
import json

LOCALHOST_ENDPOINT = 'http://127.0.0.1:8080/oauth'

app = Flask(__name__)
HOME_LINK = '<a href="http://127.0.0.1:8080">Go Home</a>'

@app.route('/')
def root_page():
    return '''
        <html>
        <head>
            <link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
                <h1> OAuth token request app </h1>
                <b>
                    Following one of these links will create a .token file in the directory that the server is running in.
                </b>
                <hr>
                <ul>
                    <li>
                        <a href='/github'>GitHub OAuth Token Flow</a>
                    </li>
                    <li>
                        <a href='/facebook'>Facebook OAuth Token Flow</a>
                    </li>
                    <li>
                        <a href='/reddit'>Reddit OAuth Token Flow</a>
                    </li>
               </ul>
        </body>
        </html>
    '''


'''
    OAuth flow code for GitHub

    API Docs: http://developer.github.com/v3/oauth/
'''
GITHUB_BASE_URL = 'https://github.com/login/oauth'
github_creds = {
    'client_id' : '47f975d65cb2cc6fba2f',
    'client_secret' : '94df88d7d222c689725d7717a3387d956f24769a',
}
github = OAuth2Service(
    client_id=github_creds['client_id'],
    client_secret=github_creds['client_secret'],
    authorize_url=(GITHUB_BASE_URL + '/authorize'),
    access_token_url=(GITHUB_BASE_URL + '/access_token'),
)

@app.route('/github')
def github_redirect():
    return redirect(
        github.get_authorize_url(redirect_uri=(LOCALHOST_ENDPOINT + '/github')),
        code=302
    )

@app.route('/oauth/github')
def receive_github_code():
    token = urlparse.parse_qs(github.get_raw_access_token(data={
        'code' : request.args.get('code'),
        'redirect_uri' : LOCALHOST_ENDPOINT + '/github'
    }).text)

    github_creds['access_token'] = token['access_token'][0]
    with open('github_oauth.token', 'w') as f:
        f.write(json.dumps(github_creds))
    return "GitHub OAuth token flow complete " + HOME_LINK


'''
    OAuth flow code for Facebook
    API Docs: https://developers.facebook.com/docs/reference/dialogs/oauth/
'''
FACEBOOK_BASE_URL = 'https://www.facebook.com'
facebook_creds = {
    'client_id' : '256137844547669',
    'client_secret' : '9387d2da526147fdd8af8c0811b14dfd'
}
facebook = OAuth2Service(
    client_id=facebook_creds['client_id'],
    client_secret=facebook_creds['client_secret'],
    authorize_url=(FACEBOOK_BASE_URL + '/dialog/oauth'),
    access_token_url='https://graph.facebook.com/oauth/access_token',
)

@app.route('/facebook')
def facebook_redirect():
    return redirect(
        facebook.get_authorize_url(
            redirect_uri=(LOCALHOST_ENDPOINT + '/facebook'),
            scope='publish_actions'
        ),
        code=302
    )

@app.route('/oauth/facebook')
def receive_facebook_code():
    token = urlparse.parse_qs(facebook.get_raw_access_token(data={
        'code' : request.args.get('code'),
        'redirect_uri' : LOCALHOST_ENDPOINT + '/facebook'
    }).text)

    facebook_creds['access_token'] = token['access_token'][0]
    with open('facebook_oauth.token', 'w') as f:
        f.write(json.dumps(facebook_creds))
    return "Facebook OAuth token flow complete " + HOME_LINK


'''
    OAuth flow code for Reddit
    API Docs: https://github.com/reddit/reddit/wiki/OAuth2
'''
REDDIT_BASE_URL = 'https://ssl.reddit.com/api/v1'
reddit_creds = {
    'client_id' : 'RQmPBWVnLdMpAw',
    'client_secret' : 'GfF_lklead8-yVRHWiUN3MhYK1k'
}
reddit = OAuth2Service(
    client_id=reddit_creds['client_id'],
    client_secret=reddit_creds['client_secret'],
    authorize_url=(REDDIT_BASE_URL + '/authorize'),
    access_token_url=(REDDIT_BASE_URL + '/access_token')
)

@app.route('/reddit')
def reddit_redirect():
    params = {
        'scope' : 'identity',
        'state' : 'derp',
        'response_type': 'code',
        'redirect_uri': LOCALHOST_ENDPOINT + '/reddit',
    }
    return redirect(
        reddit.get_authorize_url(**params),
        code=302
    )

@app.route('/oauth/reddit')
def receive_reddit_code():
    data = {
        'code' : request.args.get('code'),
        'redirect_uri' : LOCALHOST_ENDPOINT + '/reddit',
        'grant_type' : 'authorization_code'
    }

    token = json.loads(reddit.get_raw_access_token(
        data=data,
        auth=(reddit_creds['client_id'], reddit_creds['client_secret'])
    ).text)

    reddit_creds['access_token'] = token['access_token']
    with open('reddit_oauth.token', 'w') as f:
        f.write(json.dumps(reddit_creds))
    return 'Reddit OAuth token flow complete ' + HOME_LINK





if __name__ == '__main__':
    app.debug = True
    app.run(port=8080)
