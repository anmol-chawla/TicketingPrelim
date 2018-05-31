import re
from flask import Flask, request, jsonify, g, url_for, render_template, redirect, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from model import insert_data, check_user
from uuid_create import dict_to_uuid
from qr_create import create_qrcode
from email_send import send_email
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://anmol:golmol@localhost/aadb'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin, db.Model):
    __tablename__ = 'auth'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password_hash = db.Column(db.String)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/api/addusers', methods=['POST'])
def new_user():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username is None or password is None:
            return jsonify({'status': "Empty form"})  # missing arguments
        if User.query.filter_by(username=username).first() is not None:
            return jsonify({'status': 'exists'})  # existing user
        user = User(username=username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'status': "Success"})


@app.route("/api/login", methods=['POST'])
def authorize():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username is None or password is None:
            return jsonify({'status': "Empty form"})  # missing arguments
        if User.query.filter_by(username=username).first() is not None:
            user = User.query.filter_by(username=username).first()
            if user.verify_password(password):
                g.user = user
                login_user(user)
                return redirect(url_for('do_sale'), code=307)


@app.route("/sale/record", methods=["POST"])
@login_required
def do_sale():
    return render_template("form_sale.html")


@app.route("/api/enter", methods=["POST"])
@login_required
def enter_data():
    if request.method == "POST":
        try:
            user_info = {}
            name = request.form.get('name')
            reg_no = request.form.get('reg_no')
            mail_id = request.form.get('mail_id')
            phone = request.form.get('phone')
            college = request.form.get('college')
            pay_mode = request.form.get('pay_mode')
            event_type = request.form.get('type')
            location = request.form.get('location')
            pch = request.form.get('pch')
            user_info['name'] = name
            user_info['reg_no'] = reg_no
            user_info['mail_id'] = mail_id
            user_info['phone'] = phone
            user_info['college'] = college
            user_info['pay_mode'] = pay_mode
            user_info['event_type'] = event_type
            user_info['location'] = location
            user_info['pch'] = pch
            id = dict_to_uuid(user_info)
            if insert_data(id, name, reg_no, mail_id, phone, college, pay_mode, location, event_type, pch):
                create_qrcode(id)
                if not re.match(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", mail_id):
                    return "Incorrect Email"
                send_email(mail_id, ('QRCodes/' + id + '.png'))
                return 'Mail Sent'
            return "Success"
        except Exception as e:
            return jsonify({
                'error': str(e)
            })


if __name__ == '__main__':
    app.run(debug=True)
