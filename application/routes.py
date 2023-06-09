from application import app, db
from flask import render_template, request, json, Response, flash, redirect, url_for
from application.models import User, get_password, set_password, Course, Enrollment
from application.forms import LoginForm, RegisterForm
from werkzeug.security import check_password_hash

courseData = [{"courseID": "1111", "title": "PHP 101", "description": "Intro to PHP", "credits": 3, "term": "Fall, Spring"}, {"courseID": "2222", "title": "Java 1", "description": "Intro to Java Programming", "credits": 4, "term": "Spring"}, {"courseID": "3333", "title": "Adv PHP 201",
                                                                                                                                                                                                                                                   "description": "Advanced PHP Programming", "credits": 3, "term": "Fall"}, {"courseID": "4444", "title": "Angular 1", "description": "Intro to Angular", "credits": 3, "term": "Fall, Spring"}, {"courseID": "5555", "title": "Java 2", "description": "Advanced Java Programming", "credits": 4, "term": "Fall"}]


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", index=True)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        # if user and get_password(email, password):
        user = User.objects(email=email).first()
        if password == user.password:
            flash("You are successfully logged in!", "success")
            return redirect("/index")
        else:
            flash("Sorry,something went wrong", "danger")
    return render_template("login.html", title="Login", form=form, login=True)


@app.route("/Courses/")
@app.route("/Courses/<term>")
def Courses(term="2019"):
    if term is None:
        term = "Spring 2019"
    classes = Course.objects.order_by("-courseID")
    return render_template("Courses.html", courseData=classes, courses=True, term=term)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(user_id=user_id, email=email,
                    first_name=first_name, last_name=last_name)
        set_password(password)
        user.save()
        flash('You are successfully registered!', 'success')
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", form=form, register=True)


@app.route("/enrollment", methods=["POST", "GET"])
def enrollment():
    courseID = request.form.get('courseID')
    courseTitle = request.form.get('title')
    user_id = 1
    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(
                f"Oops! You already registered to this course {courseTitle}!", "danger")
            return redirect(url_for("Courses"))
        else:
            Enrollment(user_id=user_id, courseID=courseID)
            flash(f"You are enrolled in {courseTitle}!", "success")

    classes = None
    term = request.form.get('term')
    return render_template("enrollment.html", enrollment=True, title="Enrollment", classes=classes)


@app.route("/api")
@app.route("/api/<idx>")
def api(idx=None):
    if (idx == None):
        jdata = courseData
    else:
        jdata = courseData[int(idx)]

    return Response(json.dumps(jdata), mimetype="application/json")


class User(db.Document):
    user_id = db.IntField(unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    email = db.StringField(max_length=30)
    password = db.StringField(max_length=30)


@app.route("/user")
def user():
    # User(user_id=1, first_name="Christian", last_name="Hur",
    #      email="christian@uta.com", password='abc1234').save()
    # User(user_id=2, first_name="Mary", last_name="Jane",
    #      email="maryjane@uta.com", password='password123').save()
    users = User.objects.all()
    return render_template('user.html', users=users)
