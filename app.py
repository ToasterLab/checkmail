import os
from flask import Flask, jsonify
from flask_cors import CORS
from Email import Email

app = Flask(__name__)
CORS(app)


@app.route('/')
def readme():
    return ("<p>GET /[string: email_address]</p><p>GET /overall[string: email_address]</p><p>GET /syntax[string: email_address]</p><p>GET /dns[string: email_address]</p><p>GET /smtp[string: email_address]</p>")


@app.route('/<string:address>')
def check_email(address):
    email = Email(address)
    return jsonify(vars(email))


@app.route('/overall/<string:address>')
def check_email_overall(address):
    email = Email(address)
    return str(email.valid['overall']).upper()


@app.route('/syntax/<string:address>')
def check_email_syntax(address):
    email = Email(address)
    return str(email.valid['syntax']['result']).upper()


@app.route('/dns/<string:address>')
def check_email_dns(address):
    email = Email(address)
    return str(email.valid['dns']['result']).upper()


@app.route('/smtp/<string:address>')
def check_email_smtp(address):
    email = Email(address)
    return str(email.valid['smtp']['result']).upper()


if(__name__ == '__main__'):
    app.run(
        host=os.environ.get('host', '0.0.0.0'),
        port=os.environ.get('port', 8000),
        debug=os.environ.get('debug', True)
    )
