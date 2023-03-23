# import flask
# from application import db
# from werkzeug.security import generate_password_hash, check_password_hash


# class User(db.Document):
#     user_id = db.IntField(unique=True)
#     first_name = db.StringField(max_length=50)
#     last_name = db.StringField(max_length=50)
#     email = db.StringField(max_length=30, unique=True)
#     password = db.StringField(max_length=30)

#     def set_password(self, password):
#         self.password = generate_password_hash(password)

#     def get_password(self, password):
#         return check_password_hash(self.password, password)


# class Course(db.Document):
#     course_id = db.StringField(max_length=10, unique=True)
#     title = db.StringField(max_length=100)
#     description = db.StringField(max_length=255)
#     credits = db.IntField()
#     term = db.StringField(max_length=25)


# class Enrollment(db.Document):
#     user_id = db.IntField()
#     course_id = db.StringField(max_length=10)

import flask
from application import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


def set_password(password):
    password = generate_password_hash(password)


class User(db.Document, UserMixin):
    user_id = db.IntField(unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    email = db.StringField(max_length=30, unique=True)
    password = db.StringField()


def get_password(email, password):
    user = User.objects(email=email).first()
    # if user.password == password:
    #     return 1
    return check_password_hash(set_password(password), user.password)


class Course(db.Document):
    courseID = db.StringField(max_length=10, unique=True)
    title = db.StringField(max_length=100)
    description = db.StringField(max_length=255)
    credits = db.IntField()
    term = db.StringField(max_length=25)


class Enrollment(db.Document):
    user_id = db.IntField()
    courseID = db.StringField(max_length=10)
