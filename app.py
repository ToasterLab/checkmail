import os
from flask import Flask, jsonify
from flask_cors import CORS
from Email import Email

app = Flask(__name__)
CORS(app)


@app.route('/')
def readme():
    return 'GET /[string: email_address]'


@app.route('/<string:address>')
def check_email(address):
    email = Email(address)
    return jsonify(vars(email))


if(__name__ == '__main__'):
    app.run(
        host=os.environ.get('host', '0.0.0.0'),
        port=os.environ.get('port', 8000),
        debug=os.environ.get('debug', True)
    )
