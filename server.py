
import re
from flask import Flask, render_template, request, redirect, url_for,jsonify
#from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from werkzeug.security  import generate_password_hash, check_password_hash
from  flask_login import UserMixin, LoginManager, login_required, login_user, logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os
#from flask_migrate import Migrate, MigrateCommand
#from flask_script import Manager
#from sys import argv


from random import randint
from datetime import datetime
#from flask_marshmallow import Marshmallow



app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname((__file__)))
database = "app.db"
con = sqlite3.connect(os.path.join(basedir,database))

app.config['SECRET_KEY'] = "jhkxhiuydu"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,database)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

db = SQLAlchemy(app)





class Users(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(500))
    course_one =  db.Column(db.String(255))
    course_two =  db.Column(db.String(255))
    course_three = db.Column(db.String(255))
    course_four =  db.Column(db.String(255))
    school_one =  db.Column(db.String(255))
    school_two =  db.Column(db.String(255))
    school_three=  db.Column(db.String(255))
    school_four =  db.Column(db.String(255))
    exam_no = db.Column(db.Integer)
    referID = db.Column(db.String(500))



    def check_password(self, password):
            return check_password_hash(self.password, password)
    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')


    def create(self, firstname='',  email='', lastname='', password='',referID=''):
        self.firstname	 = firstname
        self.email	 = email
        self.lastname 	 = lastname
        self.referID = referID
        self.password= generate_password_hash(password, method='sha256')


    def save(self):
        db.session.add(self)
        db.session.commit()

    def commit(self):
        db.session.commit()

class school(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(255))
    school_location = db.Column(db.String(255))
    school_rate = db.Column(db.String(255))
    

class Settings(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), unique=True)
    lastname = db.Column(db.String(255), unique=True)

class Secure(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    

admin = Admin(app, name='administration', template_mode='bootstrap3')
admin.add_view(Secure(Users, db.session))
admin.add_view(Secure(Settings, db.session))

login_manager = LoginManager()
login_manager.login_view = "signin"
login_manager.init_app(app)
@login_manager.user_loader
def user_loader(homepage_id):
    return Users.query.get(homepage_id)


@app.route("/signin",methods=['GET','POST'])
def signin():
    users = Users()
    if request.method == "POST":
        data = request.json
        userByemail = users.query.filter_by(email=data['email']).first()
        mainUser = None
        if userByemail:
            mainUser = userByemail
        if mainUser:
            if mainUser.check_password(data['password']):
                login_user(mainUser,remember=True,fresh=True)
                return jsonify({'status':200,'msg':'user authenticated'})
            return jsonify({"status":404,"msg":"Invalid password provided!!!"})
        return jsonify({"status":404,"msg":"invalid email or username"})

    return render_template("signin.html")


@app.route("/signup",methods=['GET','POST'])
def signup():
    users = Users()
    if request.method == 'POST':
        data = request.json
        email = data['email']
        firstname = data['firstname']
        lastname = data['lastname']
        password = data['password']
        if users.query.filter_by(email=email).first():
            return jsonify({"status":404,"msg":"email already exist!!!"})
        users.create(email=email,
                            firstname = firstname,
                            lastname = lastname,
                            password = password
                            )
        users.save()

        login_user(users)
        # return redirect(url_for("dashboard"))
        return jsonify({'status':200,"msg":"registration compelete!!!"})

    return render_template("signup.html")
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/service.html')
def service():
    return render_template('service.html')
@app.route('/about.html')
def about():
    return render_template('about.html')
@app.route("/dashboard")
@login_required
def dashboard():
    siteSettings = Settings.query.all()
  
    return render_template('dashboard.html',
                                siteSettings=siteSettings,
                                )

# @app.route('/login.html')
# def login():
#     return render_template('login.html')
@app.route('/school.html')
def schools():
    return render_template('school.html')
@app.route('/email.html')
def email():
    return render_template('email.html')








@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("signin"))




@app.route("/db")
def database():
    db.drop_all()
    db.create_all()
    return "Hello done!!!"


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
