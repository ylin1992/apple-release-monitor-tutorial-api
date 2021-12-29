from flask import Flask, jsonify, abort
from flask_cors import CORS
from database.models import setup_db
import requests
import ast
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    setup_db(app)
    return app

app = create_app()

@app.route('/test')
def test():
    return jsonify({
        'test': 'done'
    })

@app.route('/callback', methods=['GET'])
def app_response_code():
    return '''  <script type="text/javascript">
                var token = window.location.href.split("code=")[1]; 
                window.location = "/callback_token/" + token;
            </script> '''

@app.route('/callback_token/<token>/', methods=['GET'])
def app_response_token(token):
    print(token)
    bearer_token = post_token_request(token)
    if 'access_token' in bearer_token:
        return jsonify({
            'access_token': bearer_token['access_token']
        })
    else:
        return jsonify({
            'access_token': None
        })


def post_token_request(id_token):
    print({
        'client_id': os.getenv('CLIENT_ID', ''),
        'client_secret': os.getenv('CLIENT_SECRET', ''),
        'code': id_token
    })
    url = 'https://dev-artpgixt.us.auth0.com/oauth/token'
    obj = {
        'grant_type': 'authorization_code',
        'client_id': os.getenv('CLIENT_ID', ''),
        'client_secret': os.getenv('CLIENT_SECRET', ''),
        'code': id_token,
        'redirect_uri': os.getenv('REDIRECT_URI', '')
    }
    header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post(url, data=obj, headers=header)
    r = r.content.decode("UTF-8")
    r = ast.literal_eval(r)
    print(r)
    return jsonify({
        'token': r
    })

if __name__ == '__main__':
    app.run(debug=True)