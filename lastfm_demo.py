from flask import Flask, request, redirect

import requests
import json

'''
    This basic demo shows querying an artist page using the audioscrobbler API.
    Loading root/<artist name> will generate a page that shows the description and image associated with the artist.
    
    For various reasons, the homepage demonstrates the API result for "Kanye West".
'''

KEY = '149dd5b09740a5d715f2831fe791c262'
SECRET = '326c2adac87600bdead990fd7e8ff4a8'

API_ROOT = 'http://ws.audioscrobbler.com/2.0/'

app = Flask(__name__)

@app.route('/')
def root_page():
    return redirect('http://127.0.0.1:8080/kanye%20west')

@app.route('/<artist>')
def artist_page(artist):
    payload = {
        'method' : 'artist.getinfo',
        'artist' : artist,
        'api_key' : KEY,
        'format' : 'json'
    }

    r = requests.get(API_ROOT, params=payload)
    artist_details = json.loads(r.text)

    summary =  artist_details['artist']['bio']['summary']
    image =  artist_details['artist']['image'][-1]['#text']

    page = '<html><head><link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet"></head>' + summary + '<hr><img src="' + image + '"></html'

    return page


if __name__ == '__main__':
    app.debug = True
    app.run(port=8080)
