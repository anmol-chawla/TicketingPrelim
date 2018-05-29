from flask import Flask, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from model import insert_data, check_user
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://anmol:pass@localhost/aadb'
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


class User(db.Model):
    __tablename__ = 'auth'

    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)

    def verify_password(self, password):
        return check_user(self.username, password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/users', methods=['POST'])
def new_user():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if username == '' or password == '':
            exit(400)  # missing arguments
        # if User.query.filter_by(username=username).first() != '':
        #     exit(400)  # existing user
        user = User(username=username, password=password)
        if not user.verify_password(password):
            exit(400)
        db.session.add(user)
        db.session.commit()
        return jsonify({'status': "Success"})


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app.route("/sale/record", methods=["POST"])
def do_sale():
    if request.method == "POST":
        try:
            id = request.form.get('id')
            name = request.form.get('name')
            reg_no = request.form.get('reg_no')
            mail_id = request.form.get('mail_id')
            phone = request.form.get('phone')
            college = request.form.get('college')
            pay_mode = request.form.get('pay_mode')
            type = request.form.get('type')
            pch = request.form.get('pch')
            insert_data(id, name, reg_no, mail_id, phone, college, pay_mode, type, pch)
            return "Success"
        except Exception as e:
            return jsonify({
                'error': str(e)
            })


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


if __name__ == '__main__':
    app.run(debug=True)
