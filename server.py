


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

import random
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
    exam_no = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    school = db.Column(db.String(255))
    prefcourse = db.Column(db.String(255))
    userFile_science = db.relationship('userFile_science', backref='users', lazy=True)

    
    
    def create(self, firstname='',  exam_no='', lastname='', username = '', password = '',school='', prefcourse = ''):
            self.firstname	 = firstname
            self.lastname 	 = lastname
            self.exam_no = exam_no
            self.username = username
            self.password =  password
            self.school = school
            self.prefcourse = prefcourse
           
            
            
            
       
  


    def save(self):
        db.session.add(self)
        db.session.commit()

    def commit(self):
        db.session.commit()

class userFile_science(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    course_one =  db.Column(db.String(255))
    course_two =  db.Column(db.String(255))
    course_three = db.Column(db.String(255))
    course_four =  db.Column(db.String(255))
    course_five =  db.Column(db.String(255))
    course_six =  db.Column(db.String(255))
    school_one = db.Column(db.String(255))
    school_two =  db.Column(db.String(255))
    school_three =  db.Column(db.String(255))
    preferred_school = db.Column(db.String(255))
    preferred_course = db.Column(db.String(255))
    personality_test1 = db.Column(db.String(255))
    personality_test2 = db.Column(db.String(255))
    user = db.Column(db.Integer, db.ForeignKey(Users.id))

    
    def create(self, course_one='',  course_two='', course_three='', course_four = '', course_five = '', course_six = '', school_one = '', school_two = '', school_three = '', preferred_school = '', preferred_course ='', personality_test1='', personality_test2=''):
            self.course_one	 = course_one
            self.course_two	 = course_two
            self.course_three	 = course_three
            self.course_four	 = course_four
            self.course_five	 = course_five
            self.course_six	 = course_six
            self.school_one = school_one
            self.school_two = school_two
            self.school_three = school_three
            self.preferred_course = preferred_course
            self.preferred_school = preferred_school
            self.presonality_test1 = personality_test1
            self.presonality_test2 = personality_test2
       
  


    def save(self):
        db.session.add(self)
        db.session.commit()

    def commit(self):
        db.session.commit()
        
# class userFile_others(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key = True)
#     course_one =  db.Column(db.String(255))
#     course_two =  db.Column(db.String(255))
#     course_three = db.Column(db.String(255))
#     course_four =  db.Column(db.String(255))
#     course_five =  db.Column(db.String(255))
  
#     school_one = db.Column(db.String(255))
#     school_two =  db.Column(db.String(255))
#     school_three =  db.Column(db.String(255))
#     preferred_school = db.Column(db.String(255))
#     preferred_course = db.Column(db.String(255))
#     presonality_test1 = db.Column(db.String(255))
#     presonality_test2 = db.Column(db.String(255))
    
#     def create(self, course_one='',  course_two='', course_three='', course_four = '', course_five = '', school_one = '', school_two = '', school_three = '', preferred_school = '', preferred_course ='', personality_test1='', personality_test2=''):
#             self.course_one	 = course_one
#             self.course_two	 = course_two
#             self.course_three	 = course_three
#             self.course_four	 = course_four
#             self.course_five	 = course_five
            
#             self.school_one = school_one
#             self.school_two = school_two
#             self.school_three = school_three
#             self.preferred_course = preferred_course
#             self.preferred_school = preferred_school
#             self.presonality_test1 = personality_test1
#             self.presonality_test2 = personality_test2
       
  


#     def save(self):
#         db.session.add(self)
#         db.session.commit()

#     def commit(self):
#         db.session.commit()
      

class Secure(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    

admin = Admin(app, name='administration', template_mode='bootstrap3')
admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(userFile_science, db.session))
# admin.add_view(ModelView(userFile_others, db.session))



login_manager = LoginManager()
login_manager.login_view = "signin"
login_manager.init_app(app)
@login_manager.user_loader
def user_loader(homepage_id):
    return Users.query.get(homepage_id)


@app.route('/login',methods=['GET','POST'])
def login():
    user = Users()
    if request.method == 'POST':
        username = request.form['usernames']
        password = request.form['passwords']
        user = Users.query.filter_by(username=username,is_admin=True).first()
       
        if user:
            if user.password == password:
                login_user(user)
                return redirect('admin')

                
                
            


    return render_template('login.html')
@app.route('/process',methods=['GET','POST'])

def process():
    auths = Users()
    if request.method == "POST":
        username = request.form['uname']
        password = request.form['pass']
        email = request.form['email']
        auths = Users(username=username,
             password=password,email=email,is_admin=True)
        db.session.add(auths)
        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template('register.html')
  

  
@app.route('/',methods=['GET','POST'])

def signup():
    auths = Users()
    if request.method == "POST":
        firstname = request.form['fname']
        lastname = request.form['lname']
        exam_no = request.form['exam_no']
        
        auths = Users(firstname=firstname, lastname = lastname
             ,exam_no=exam_no)
        db.session.add(auths)
        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template('index.html')

@app.route('/signin',methods=['GET','POST'])
def signin():
    user = Users()
    if request.method == 'POST':
        exam_no = request.form['exam_no']
       
        user = Users.query.filter_by(exam_no=exam_no).first()
       
        login_user(user)
        return redirect(url_for("dashboard"))

                
                
            


    return render_template('signin.html')

@app.route('/science',methods=['GET','POST'])
@login_required
def science():
    auth = userFile_science()
    
    if request.method == 'POST':
        course_one = request.form['course_one']
        course_two = request.form['course_two']
        course_three = request.form['course_three']
        course_four = request.form['course_four']
        course_five = request.form['course_five']
        course_six = request.form['course_six']
        school_one = request.form['school_one']
        school_two = request.form['school_two']
        school_three = request.form['school_three']
        # preferred_school = request.form ['prefferred_school']
        preferred_course = request.form['preferred_course']
        personality_test1 = request.form['question1']
        personality_test2 = request.form['question2']
        
        
        auth = userFile_science(course_one = course_one, course_two = course_two, course_three = course_three, course_four = course_four, course_five = course_five, course_six = course_six,school_one= school_one, school_two = school_two, school_three = school_three, preferred_course = preferred_course,  personality_test1 = personality_test1, personality_test2 = personality_test2)
        db.session.add(auth)
        db.session.commit()
        return "go to view result screen"
        
            
    return render_template('science.html')

# @app.route("/others")
# @login_required
# def others():
#     auth = userFile_others()
#     total =  userFile_science
#     if request.method == 'POST':
#         course_one = request.form['course_one']
#         course_two = request.form['course_two']
#         course_three = request.form['course_three']
#         course_four = request.form['course_four']
#         course_five = request.form['course_five']
       
#         school_one = request.form['school_one']
#         school_two = request.form['school_two']
#         school_three = request.form['school_three']
#         preferred_school = request.form ['prefferred_school']
#         preferred_course = request.form['prefferred_course']
#         personality_test1 = request.form['question1']
#         personality_test2 = request.form['question2']
        
#         # if total == course_one + course_two + course_three + course_four + course_five + course_five + course_six:
#         #     print(total)
#         auth = userFile_science(course_one = course_one, course_two = course_two, course_three = course_three, course_four = course_four, course_five = course_five, school_one= school_one, school_two = school_two, school_three = school_three, preferred_course = preferred_course, preferred_school = preferred_school, personality_test1 = personality_test1, personality_test2 = personality_test2)
#         db.session.add(auth)
#         db.session.commit()
#         return "go to view result screen"
        
   
#     return render_template('others.html')

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')



@app.route('/result')
@login_required
def result():
    return render_template('result.html')

# @app.route('/entry')
# @login_required
# def entry():
#     siteSettings = userFile_science.query.all()
#     return render_template('entry.html',
#                             siteSettings=siteSettings
#                            )

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
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
