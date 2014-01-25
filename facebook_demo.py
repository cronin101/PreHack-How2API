import json
import webbrowser
from rauth import OAuth2Session

API_BASE = 'https://graph.facebook.com'

if __name__ == '__main__':
    with open('./facebook_oauth.token', 'r') as f:
        creds = json.loads(f.read())

    session = OAuth2Session(
      client_id=creds['client_id'],
      client_secret=creds['client_secret'],
      access_token=creds['access_token'],
    )

    user_details = session.get(API_BASE + '/me').json()

    print("Hello " + user_details['name'] + "!")

    session.post(API_BASE + '/' + user_details['id'] + '/feed',
            data={
                'message' : 'Pre-Hack is awesome.',
                'place' : '282348111785010'
            }
    )

    webbrowser.open(user_details['link'])
