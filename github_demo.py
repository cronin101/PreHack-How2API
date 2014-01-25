import json
from rauth import OAuth2Session

API_BASE = 'https://api.github.com'

if __name__ == '__main__':
    with open('./github_oauth.token', 'r') as f:
        creds = json.loads(f.read())

    session = OAuth2Session(
      client_id=creds['client_id'],
      client_secret=creds['client_secret'],
      access_token=creds['access_token'],
    )

    user_details = session.get(API_BASE + '/user').json()

    print(
        "Hello there " + user_details['login'] + ", or should I call you " + user_details['name'] + "?\n"
        "You have " + str(user_details['public_repos']) + " public repos on GitHub, "
        "and " + str(user_details['public_gists']) + " public gists."
    )


