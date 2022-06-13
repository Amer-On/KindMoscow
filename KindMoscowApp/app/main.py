from flask import Flask, request, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import *
from random import randrange
import requests as req
from config import api_server_ip, api_login, api_password

startTimeForSessions = datetime(year=2022, month=1, day=1)
app = Flask(__name__,
            static_folder='static',
            template_folder='templates'
            )
app.config["SECRET_KEY"] = "bo5akspa182xxd61o4v6i7sgrzt5wz"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main"
app.config["SQLALCHEMY_BINDS"] = {
    'users': 'sqlite:///users.db',
    'register': 'sqlite:///register.db',
    'recovery': 'sqlite:///recovery.db',
    'users_info': 'sqlite:///users_info.db',
    'events': 'sqlite:///events.db',
    'log': 'sqlite:///log.db',
    'searcher_info': 'sqlite:///searcher_info.db',
    'business_info': 'sqlite:///business_info.db',
    'business_log': 'sqlite:///business_log.db'
}
db = SQLAlchemy(app)


def generate_code():
    alphabet = "qwertyuiopasdfghjklzxcvbnm1234567890"
    code = ""
    for i in range(30):
        code += alphabet[randrange(len(alphabet))]
    return code


def getName(id):
    try:
        user = User.query.get(id)
        print(user.role)
        if user.role == "volunteer":
            try:
                return UserInfo.query.filter_by(email=user.email).first().name
            except:
                return "Волонтер"
        if user.role == "searcher":
            try:
                return SearcherInfo.query.filter_by(email=user.email).first().company
            except:
                return "Организатор"
        if user.role == "business":
            try:
                return BusinessInfo.query.filter_by(email=user.email).first().company
            except:
                return "Спонсор"
    except:
        return ""



class User(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


class Register(db.Model):
    __bind_key__ = 'register'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Register %r>' % self.id


class Recovery(db.Model):
    __bind_key__ = 'recovery'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Recovery %r>' % self.id


class Event(db.Model):
    __bind_key__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    metro = db.Column(db.String(100), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    count = db.Column(db.Integer, nullable=True)
    used = db.Column(db.Integer, default=0)
    ages = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Event %r>' % self.id


class Log(db.Model):
    __bind_key__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), nullable=False)
    event_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Log %r>' % self.id


class UserInfo(db.Model):
    __bind_key__ = 'users_info'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    patronymic = db.Column(db.String(50), nullable=True)
    birth = db.Column(db.DateTime, nullable=False)
    company = db.Column(db.String(100), nullable=False)
    education = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    volunteer = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<UserInfo %r>' % self.id


class SearcherInfo(db.Model):
    __bind_key__ = 'searcher_info'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)


class BusinessInfo(db.Model):
    __bind_key__ = 'business_info'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)


class BusinessLog(db.Model):
    __bind_key__ = 'business_log'
    id = db.Column(db.Integer, primary_key=True)
    business_email = db.Column(db.String(100), nullable=False)
    event_id = db.Column(db.Integer, nullable=False)


def email_is_busy(email: str) -> bool:
    state = User.query.filter_by(email=email).first()
    if state is None:
        return False
    else:
        return True


def need_to_redirect(basedRedirect: str):
    if 'need_to_redirect' in session and 'id' in session and 'time_to_redirect' in session:
        tmp = datetime.now() - startTimeForSessions
        nowTime = tmp.days * 86400 + tmp.seconds
        if nowTime - session['time_to_redirect'] >= 300:
            session['need_to_redirect'] = ''
            return basedRedirect
        elif ready(session['id']) and session['need_to_redirect'] != '':
            save = session['need_to_redirect']
            session['need_to_redirect'] = ''
            return save
    return basedRedirect


def check_user(email: str, password: str, id=0) -> bool:
    try:
        if id == 0:
            return User.query.filter_by(email=email, password=password) .first() is not None
        user = User.query.get(id)
        return (user.email == email) and (user.password == password)
    except:
        return False


def is_volunteer(id: int):
    try:
        return User.query.get(id).role == "volunteer"
    except:
        return False


def is_searcher(id: int):
    try:
        return User.query.get(id).role == "searcher"
    except:
        return False


def is_business(id: int):
    try:
        return User.query.get(id).role == "business"
    except:
        return False


def ready(id: int):
    try:
        user = User.query.get(id)
        if user.role == "volunteer":
            return UserInfo.query.filter_by(email=user.email).first() is not None
        if user.role == "searcher":
            return SearcherInfo.query.filter_by(email=user.email).first() is not None
        if user.role == "business":
            return BusinessInfo.query.filter_by(email=user.email).first() is not None
    except:
        return False


def get_age(birth):
    age = datetime.now().year - birth.year
    if datetime.now().month < birth.month:
        age -= 1
    elif datetime.now().month == birth.month:
        if datetime.now().day < birth.day:
            age -= 1
    return age


@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():
    try:
        personal_user_id = session['id']
        personal_user_email = session['email']
        personal_user_password = session['password']
    except:
        personal_user_id = -1
        personal_user_email = ""
        personal_user_password = ""
    if check_user(personal_user_email, personal_user_password, personal_user_id):
        if request.method == "GET":
            if is_volunteer(personal_user_id):
                userInfo = UserInfo.query.filter_by(email=personal_user_email).first()
                if userInfo is not None:
                    surname = userInfo.surname
                    name = userInfo.name
                    patronymic = ""
                    if userInfo.patronymic is not None:
                        patronymic = userInfo.patronymic
                    day = userInfo.birth.day
                    month = userInfo.birth.month
                    year = userInfo.birth.year
                    birth = f"{year}-{month}-{day}"
                    education = userInfo.education
                    company = userInfo.company
                    location = userInfo.location
                    checked = []
                    print(userInfo.volunteer)
                    for i in range(9):
                        if userInfo.volunteer[i] == '0':
                            checked.append('')
                        else:
                            checked.append('checked')
                    return render_template("create_profile.html",
                                           personal_user_id=personal_user_id,
                                           name=name,
                                           surname=surname,
                                           patronymic=patronymic,
                                           birth=birth,
                                           education=education,
                                           company=company,
                                           location=location,
                                           checked0=checked[0],
                                           checked1=checked[1],
                                           checked2=checked[2],
                                           checked3=checked[3],
                                           checked4=checked[4],
                                           checked5=checked[5],
                                           checked6=checked[6],
                                           checked7=checked[7],
                                           checked8=checked[8])
                else:
                    return render_template("create_profile.html",
                                           name=getName(personal_user_id),
                                           personal_user_id=personal_user_id,)
            elif is_searcher(personal_user_id):
                searcherInfo = SearcherInfo.query.filter_by(email=personal_user_email).first()
                if searcherInfo is not None:
                    searcherInfo = SearcherInfo.query.filter_by(email=personal_user_email).first()
                    if searcherInfo is not None:
                        company = searcherInfo.company
                        description = searcherInfo.description
                        location = searcherInfo.location
                        contact = searcherInfo.contact
                        return render_template("create_searcher.html",
                                               name=getName(personal_user_id),
                                               personal_user_id=personal_user_id,
                                               company=company,
                                               description=description,
                                               location=location,
                                               contact=contact)
                return render_template("create_searcher.html",
                                       name=getName(personal_user_id),
                                        personal_user_id=personal_user_id)
            elif is_business(personal_user_id):
                businessInfo = BusinessInfo.query.filter_by(email=personal_user_email).first()
                if businessInfo is not None:
                    company = businessInfo.company
                    description = businessInfo.description
                    location = businessInfo.location
                    contact = businessInfo.contact
                    return render_template("create_business.html",
                                           name=getName(personal_user_id),
                                           personal_user_id=personal_user_id,
                                           company=company,
                                           description=description,
                                           location=location,
                                           contact=contact)
                return render_template("create_business.html",
                                       name=getName(personal_user_id),
                                       personal_user_id=personal_user_id)
        else:
            if is_volunteer(personal_user_id):
                surname = request.form.get('surnameForm')
                name = request.form.get('nameForm')
                patronymic = request.form.get('patronymicForm')
                print(request.form.get('birthForm'))
                tmp = list(map(int, request.form.get('birthForm').split('-')))
                birth = datetime(year=tmp[0], month=tmp[1], day=tmp[2])
                education = request.form.get("educationForm")
                company = request.form.get("companyForm")
                location = request.form.get("locationForm")
                volunteer = ""
                checked = []
                for i in range(9):
                    check = f"volunteer{i}Form"
                    if request.form.get(check) is None:
                        volunteer += '0'
                        checked.append('')
                    else:
                        volunteer += '1'
                        checked.append('checked')
                userInfo = UserInfo.query.filter_by(email=session['email']).first()
                state = False
                if userInfo is None:
                    state = True
                    userInfo = UserInfo()
                userInfo.email = personal_user_email
                userInfo.surname = surname
                userInfo.name = name
                userInfo.patronymic = patronymic
                userInfo.birth = birth
                userInfo.education = education
                userInfo.company = company
                userInfo.location = location
                userInfo.volunteer = volunteer
                if state:
                    db.session.add(userInfo)
                db.session.commit()
                try:
                    if state:
                        db.session.add(userInfo)
                    db.session.commit()
                    return redirect(need_to_redirect(f"/profile/{personal_user_id}"))
                except:
                    return render_template("create_profile.html",
                                           personal_user_id=personal_user_id,
                                           name=name,
                                           surname=surname,
                                           location=location,
                                           patronymic=patronymic,
                                           birth='-'.join([str(i) for i in tmp]),
                                           education=education,
                                           company=company,
                                           checked0=checked[0],
                                           checked1=checked[1],
                                           checked2=checked[2],
                                           checked3=checked[3],
                                           checked4=checked[4],
                                           checked5=checked[5],
                                           checked6=checked[6],
                                           checked7=checked[7],
                                           checked8=checked[8])
            elif is_searcher(personal_user_id):
                searcherInfo = SearcherInfo.query.filter_by(email=session['email']).first()
                state = False
                if searcherInfo is None:
                    state = True
                    searcherInfo = SearcherInfo()
                searcherInfo.email = personal_user_email
                searcherInfo.company = request.form.get('companyForm')
                searcherInfo.contact = request.form.get('contactForm')
                searcherInfo.description = request.form.get('descriptionForm')
                searcherInfo.location = request.form.get('locationForm')
                try:
                    if state:
                        db.session.add(searcherInfo)
                    db.session.commit()
                    return redirect(need_to_redirect(f"/profile/{personal_user_id}"))
                except:
                    return render_template("create_searcher.html",
                                           personal_user_id=personal_user_id,
                                           name=getName(personal_user_id),
                                           company=searcherInfo.company,
                                           contact=searcherInfo.contact,
                                           description=searcherInfo.description,
                                           location=searcherInfo.location
                                           )
            elif is_business(personal_user_id):
                businessInfo = BusinessInfo.query.filter_by(email=session['email']).first()
                state = False
                if businessInfo is None:
                    state = True
                    businessInfo = BusinessInfo()
                businessInfo.email = personal_user_email
                businessInfo.company = request.form.get('companyForm')
                businessInfo.contact = request.form.get('contactForm')
                businessInfo.description = request.form.get('descriptionForm')
                businessInfo.location = request.form.get('locationForm')
                try:
                    if state:
                        db.session.add(businessInfo)
                    db.session.commit()
                    return redirect(need_to_redirect(f"/profile/{personal_user_id}"))
                except:
                    return render_template("create_business.html",
                                           name=getName(personal_user_id),
                                           personal_user_id=personal_user_id,
                                           company=businessInfo.company,
                                           contact=businessInfo.contact,
                                           description=businessInfo.description,
                                           location=businessInfo.location)
    else:
        return redirect("/login")


@app.route("/", methods=["POST", "GET"])
def main():
    try:
        personal_user_id = session['id']
        personal_user_email = session['email']
        personal_user_password = session['password']
    except:
        personal_user_id = -1
        personal_user_email = ""
        personal_user_password = ""
    if request.method == "POST":
        filterMetro = request.form.get("metroForm")
        filterNumber = request.form.get("activity")
        filterDate = request.form.get("dateForm")
        requestFormat = []
        if filterMetro != "":
            requestFormat.append(f"filterMetro={filterMetro}")
        if filterNumber != "-1":
            requestFormat.append(f"filterNumber={filterNumber}")
        print(filterDate)
        if filterDate != "":
            requestFormat.append(f"filterDate={filterDate}")
        return redirect(f"/events?{'&'.join(requestFormat)}")

    isAuth = "display: none"
    noAuth = "display: none"
    if check_user(personal_user_email, personal_user_password, personal_user_id):
        isAuth = ""
    else:
        noAuth = ""
    return render_template("index.html", personal_user_id=personal_user_id,
                           isAuth=isAuth, noAuth=noAuth, name=getName(personal_user_id))


@app.route("/profile/-1")
@app.route("/profile/-1/events")
def not_auth():
    return redirect("/login")


@app.route("/quit")
def quit():
    session['email'] = ''
    session['password'] = ''
    session['id'] = -1
    session['need_to_redirect'] = ''
    return redirect("/login")


@app.route("/profile/<id>")
def profile(id: int):
    try:
        personal_user_id = session['id']
        personal_user_email = session['email']
        personal_user_password = session['password']
    except:
        personal_user_id = -1
        personal_user_email = ""
        personal_user_password = ""
    hidden = "hidden"
    print(personal_user_id, id)
    if int(id) == int(personal_user_id):
        if not ready(personal_user_id):
            return redirect("/edit-profile")
        hidden = ""
    session['need_to_redirect'] = ''
    if not ready(id):
        return redirect("/404")
    try:
        role = User.query.get(id).role
        email = User.query.get(id).email
        if role == "volunteer":
            userInfo = UserInfo.query.filter_by(email=email).first()
            name = userInfo.name
            surname = userInfo.surname
            patronymic = userInfo.patronymic
            if patronymic is None:
                patronymic = ""
            birth = userInfo.birth.strftime("%d.%m.%Y")
            age = get_age(userInfo.birth)
            if 11 <= age % 100 <= 20:
                age = str(age) + " лет"
            elif (age % 10) == 1:
                age = str(age) + " год"
            elif (age % 10) <= 4:
                age = str(age) + " года"
            else:
                age = str(age) + " лет"
            education = userInfo.education
            company = userInfo.company
            location = userInfo.location
            isAuth = "display: none"
            noAuth = "display: none"
            if check_user(personal_user_email, personal_user_password, personal_user_id):
                isAuth = ""
            else:
                noAuth = ""
            return render_template("profile_volunteer.html",
                                   isAuth=isAuth,
                                   noAuth=noAuth,
                                   personal_user_id=personal_user_id,
                                   role=role,
                                   name=name,
                                   surname=surname,
                                   patronymic=patronymic,
                                   birth=birth,
                                   age=age,
                                   education=education,
                                   company=company,
                                   location=location,
                                   id=id)
        elif role == "searcher":
            searcherInfo = SearcherInfo.query.filter_by(email=email).first()
            company = searcherInfo.company
            description = searcherInfo.description
            location = searcherInfo.location
            contact = searcherInfo.contact
            isAuth = "display: none"
            noAuth = "display: none"
            if check_user(personal_user_email, personal_user_password, personal_user_id):
                isAuth = ""
            else:
                noAuth = ""
            return render_template("profile_searcher.html",
                                   name=getName(personal_user_id),
                                   isAuth=isAuth,
                                   noAuth=noAuth,
                                   company=company,
                                   description=description,
                                   location=location,
                                   contact=contact,
                                   id=id,
                                   personal_user_id=personal_user_id)
        elif role == "business":
            businessInfo = BusinessInfo.query.filter_by(email=email).first()
            company = businessInfo.company
            description = businessInfo.description
            location = businessInfo.location
            contact = businessInfo.contact
            isAuth = "display: none"
            noAuth = "display: none"
            if check_user(personal_user_email, personal_user_password, personal_user_id):
                isAuth = ""
            else:
                noAuth = ""
            return render_template("profile_business.html",
                                   name=getName(personal_user_id),
                                   isAuth=isAuth,
                                   noAuth=noAuth,
                                   company=company,
                                   description=description,
                                   location=location,
                                   contact=contact,
                                   id=id,
                                   personal_user_id=personal_user_id)
    except:
        return redirect("/404")


@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        personal_user_id = session['id']
        personal_user_email = session['email']
        personal_user_password = session['password']
    except:
        personal_user_id = -1
        personal_user_email = ""
        personal_user_password = ""
    if check_user(personal_user_email, personal_user_password, personal_user_id):
        return redirect(f"/profile/{personal_user_id}")
    if request.method == "GET":
        return render_template("login.html", error="", saveEmail="", personal_user_id=personal_user_id)
    else:
        email = request.form.get("emailForm")
        password = request.form.get("passwordForm")
        if check_user(email, password):
            session['email'] = email
            session['password'] = password
            print(User.query.filter_by(email=email, password=password).first())
            print(User.query.all()[0].email, User.query.all()[0].password)
            session['id'] = User.query.filter_by(email=email, password=password).first().id
            if ready(session['id']):
                return redirect(need_to_redirect(f"/profile/{session['id']}"))
            else:
                return redirect(f"/profile/{session['id']}")
        else:
            return render_template("login.html", personal_user_id=personal_user_id, error="Неверно указана почта или пароль!", saveEmail=email)


def delete_trash(email: str):
    registers = Register.query.filter_by(email=email).all()
    recovery = Recovery.query.filter_by(email=email).all()
    for i in registers:
        try:
            db.session.delete(i)
        except:
            pass
    for i in recovery:
        try:
            db.session.delete(i)
        except:
            pass
    db.session.commit()


@app.route("/register", methods=["GET", "POST"])
def register():
    try:
        personal_user_id = session['id']
        personal_user_email = session['email']
        personal_user_password = session['password']
    except:
        personal_user_id = -1
        personal_user_email = ""
        personal_user_password = ""
    if check_user(personal_user_email, personal_user_password, personal_user_id):
        return redirect(f"/profile/{personal_user_id}")
    if request.method == "GET":
        return render_template("register.html", personal_user_id=personal_user_id, error="", saveEmail="")
    else:
        email = request.form.get("emailForm")
        password = request.form.get("passwordForm")
        passwordSubmit = request.form.get("passwordSubmitForm")
        role = request.form.get("roleForm")
        if password != passwordSubmit:
            return render_template("register.html", personal_user_id=personal_user_id, error="Пароли не совпадают!", saveEmail=email)
        if email_is_busy(email=email):
            return render_template("register.html", personal_user_id=personal_user_id, error="Данная почта уже зарегистрирована!", saveEmail="")

        code = generate_code()
        while Register.query.filter_by(code=code).first() is not None:
            code = generate_code()
        register = Register(email=email, code=code, password=password, role=role)
        try:
            resp = req.get(f"http://{api_server_ip}/send_email/{email}/confirm/{code}", auth=(api_login, api_password))
            if resp.text != '"OK"':
                raise exception
            db.session.add(register)
            db.session.commit()
            return render_template("submit.html", personal_user_id=personal_user_id)
        except:
            return render_template("register.html", personal_user_id=personal_user_id, error="Что-то пошло не так! Попробуйте еще раз!", saveEmail=email)


@app.route("/confirm/<code>")
def confirm(code: str):
    try:
        personal_user_id = session['id']
        personal_user_email = session['email']
        personal_user_password = session['password']
    except:
        personal_user_id = -1
        personal_user_email = ""
        personal_user_password = ""
    if check_user(personal_user_email, personal_user_password, personal_user_id):
        return redirect(f"/profile/{personal_user_id}")
    state = Register.query.filter_by(code=code).first()
    if state is None:
        return render_template("confirm_error.html", personal_user_id=personal_user_id)
    if (datetime.now() - state.date).seconds > 900 or (datetime.now() - state.date).days > 0:
        return render_template("confirm_error.html", personal_user_id=personal_user_id)
    user = User(email=state.email, password=state.password, role=state.role)
    try:
        db.session.add(user)
        db.session.delete(state)
        db.session.commit()
        return render_template("confirm.html", personal_user_id=personal_user_id)
    except:
        return render_template("confirm_error_save.html", personal_user_id=personal_user_id)


@app.route("/recovery", methods=["GET", "POST"])
def recovery():
    try:
        personal_user_id = session['id']
        personal_user_email = session['email']
        personal_user_password = session['password']
    except:
        personal_user_id = -1
        personal_user_email = ""
        personal_user_password = ""
    if check_user(personal_user_email, personal_user_password, personal_user_id):
        return redirect(f"/profile/{personal_user_id}")
    if request.method == "GET":
        return render_template("recovery.html", error="", saveEmail="", personal_user_id=personal_user_id)
    else:
        email = request.form.get("emailForm")
        if not email_is_busy(email=email):
            return render_template("recovery.html", error="Данная почта не зарегистрирована в системе!", saveEmail="", personal_user_id=personal_user_id)
        code = generate_code()
        while Recovery.query.filter_by(code=code).first() is not None:
            code = generate_code()
        recovery = Recovery(email=email, code=code)
        try:
            resp = req.get(f"http://{api_server_ip}/send_email/{email}/confirm/{code}", auth=(api_login, api_password))
            if resp.text != '"OK"':
                raise exception
            db.session.add(recovery)
            db.session.commit()
            return render_template("recovery_send_message.html", personal_user_id=personal_user_id)
        except:
            return render_template("recovery.html", personal_user_id=personal_user_id, error="Что-то пошло не так! Попробуйте еще раз!", saveEmail=email)


@app.route("/create_event", methods=["GET", "POST"])
def create_event():
    try:
        personal_user_id = session['id']
        personal_user_email = session['email']
        personal_user_password = session['password']
    except:
        personal_user_id = -1
        personal_user_email = ""
        personal_user_password = ""
    if check_user(personal_user_email, personal_user_password, personal_user_id):
        if not ready(personal_user_id):
            session['need_to_redirect'] = f"/create_event"
            tmp = datetime.now() - startTimeForSessions
            session['time_to_redirect'] = tmp.days * 86400 + tmp.seconds
            return redirect("/edit-profile")
        typeEdit = "Создание мероприятия"
        if is_searcher(personal_user_id):
            if request.method == "GET":
                return render_template("create_event.html", typeEdit=typeEdit, personal_user_id=personal_user_id, name=getName(personal_user_id))
            else:
                title = request.form.get("titleForm")
                description = request.form.get("descriptionForm")
                number = int(request.form.get("numberForm"))
                metro = request.form.get("metroForm")
                tempData = list(map(int, request.form.get("dateForm").split("-")))
                data = datetime(year=tempData[0], month=tempData[1], day=tempData[2])
                count = request.form.get("countForm")
                if count is None or len(str(count)) == 0:
                    count = -1
                else:
                    count = int(count)
                ages = int(request.form.get("agesForm"))
                event = Event(title=title,
                              description=description,
                              number=number,
                              email=personal_user_email,
                              metro=metro,
                              data=data,
                              count=count,
                              ages=ages)

                try:
                    db.session.add(event)
                    db.session.commit()
                    id = Event.query.filter_by(email=session['email']).all()[-1].id
                    return redirect(f"/event/{id}")
                except:
                    return "ERROR"
        else:
            return render_template("/events", personal_user_id=personal_user_id)
    else:
        return redirect("/login")


@app.route("/event/<id>", methods=["GET", "POST"])
def showEvent(id: int):
    try:
        personal_user_id = session['id']
        personal_user_email = session['email']
        personal_user_password = session['password']
    except:
        personal_user_id = -1
        personal_user_email = ""
        personal_user_password = ""
    if request.method == "POST":
        print("OK")
        print(request.form.get('state'))
        if not check_user(personal_user_email, personal_user_password, personal_user_id):
            session['need_to_redirect'] = f"/event/{id}"
            tmp = datetime.now() - startTimeForSessions
            session['time_to_redirect'] = tmp.days * 86400 + tmp.seconds
            return redirect("/login")
        if not ready(personal_user_id):
            session['need_to_redirect'] = f"/event/{id}"
            tmp = datetime.now() - startTimeForSessions
            session['time_to_redirect'] = tmp.days * 86400 + tmp.seconds
            return redirect("/edit-profile")
        try:
            event = Event.query.get(id)
        except:
            return redirect("/404")
        if event is None:
            return redirect("/404")
        if request.form.get('state') == "join":
            if event.data < datetime.now():
                return redirect(f"/event/{id}")
            if is_volunteer(personal_user_id):
                if event.count == event.used:
                    return redirect(f"/event/{id}")
                user = UserInfo.query.filter_by(email=personal_user_email).first()
                age = get_age(user.birth)
                log = Log(user_email=personal_user_email, event_id=id)
                if Event.query.get(id).ages > age:
                    return redirect(f"/event/{id}")
                Event.query.get(id).used += 1
                try:
                    db.session.add(log)
                    db.session.commit()
                    return redirect("/event/" + str(id))
                except:
                    return "ERROR"
            elif is_business(personal_user_id):
                businessLog = BusinessLog(business_email=personal_user_email, event_id=id)
                try:
                    db.session.add(businessLog)
                    db.session.commit()
                    return redirect("/event/" + str(id))
                except:
                    return "ERROR"
        if request.form.get('state') == "leave":
            if event.data < datetime.now():
                return redirect(f"/event/{id}")
            if is_volunteer(personal_user_id):
                log = Log.query.filter_by(user_email=personal_user_email, event_id=id).first()
                if log is not None:
                    Event.query.get(id).used -= 1
                    try:
                        db.session.delete(log)
                        db.session.commit()
                    except:
                        return "ERROR"
                return redirect("/event/" + str(id))
            elif is_business(personal_user_id):
                businessLog = BusinessLog.query.filter_by(business_email=personal_user_email, event_id=id).first()
                if businessLog is not None:
                    try:
                        db.session.delete(businessLog)
                        db.session.commit()
                    except:
                        return "ERROR"
                return redirect("/event/" + str(id))
    event = Event.query.get(id)
    if event is None:
        return redirect("/404")
    title = event.title
    description = event.description
    metro = event.metro
    volunteerTypes = ["Патриотическое", "Социальное",
                      "Спортивное", "Событийное",
                      "Культурное", "Добровольцы МЧС",
                      "Эко", "Медицинское",
                      "Туристическое"]
    volunteerType = volunteerTypes[int(event.number)]
    data = event.data.strftime("%d.%m.%Y")
    available = "disabled"
    if event.count == -1 or event.count > event.used:
        available = ""
    if event.count == -1:
        count = "Неограниченно"
    else:
        count = event.count - event.used
    age = event.ages
    users = []
    sponsors = []
    for i in Log.query.filter_by(event_id=id).all():
        user = UserInfo.query.filter_by(email=i.user_email).first()
        users.append({"name": user.name, "surname": user.surname, "id": User.query.filter_by(email=i.user_email).first().id})
    for i in BusinessLog.query.filter_by(event_id=id).all():
        sponsor = BusinessInfo.query.filter_by(email=i.business_email).first()
        sponsors.append({"company": sponsor.company, "id": User.query.filter_by(email=i.business_email).first().id})
    if event.data <= datetime.now():
        isAuth = "display: none"
        noAuth = "display: none"
        if check_user(personal_user_email, personal_user_password, personal_user_id):
            isAuth = ""
        else:
            noAuth = ""
        # fajk;;
        return render_template("aboutEventNoButton.html",
                               isAuth=isAuth,
                               noAuth=noAuth,
                               title=title,
                               metro=metro,
                               age=age,
                               count=count,
                               data=data,
                               description=description,
                               volunteerType=volunteerType,
                               users=users,
                               sponsors=sponsors,
                               name=getName(personal_user_id))
    elif event.email == personal_user_email:
        isAuth = "display: none"
        noAuth = "display: none"
        if check_user(personal_user_email, personal_user_password, personal_user_id):
            isAuth = ""
        else:
            noAuth = ""
        return render_template("aboutEvent_admin.html",
                               isAuth=isAuth,
                               noAuth=noAuth,
                               title=title,
                               metro=metro,
                               age=age,
                               count=count,
                               data=data,
                               description=description,
                               volunteerType=volunteerType,
                               users=users,
                               sponsors=sponsors,
                               name=getName(personal_user_id),
                               id=id)
    elif is_business(personal_user_id):
        if BusinessLog.query.filter_by(business_email=session['email'], event_id=id).first() is None:
            isAuth = "display: none"
            noAuth = "display: none"
            if check_user(personal_user_email, personal_user_password, personal_user_id):
                isAuth = ""
            else:
                noAuth = ""
            return render_template("AboutEvent.html",
                                   isAuth=isAuth,
                                   noAuth=noAuth,
                                   title=title,
                                   metro=metro,
                                   age=age,
                                   count=count,
                                   data=data,
                                   description=description,
                                   volunteerType=volunteerType,
                                   users=users,
                                   sponsors=sponsors,
                                   name=getName(personal_user_id),
                                   state="join",
                                   buttonName="Спонсировать")
        else:
            isAuth = "display: none"
            noAuth = "display: none"
            if check_user(personal_user_email, personal_user_password, personal_user_id):
                isAuth = ""
            else:
                noAuth = ""
            return render_template("AboutEvent.html",
                                   isAuth=isAuth,
                                   noAuth=noAuth,
                                   title=title,
                                   metro=metro,
                                   age=age,
                                   count=count,
                                   data=data,
                                   description=description,
                                   volunteerType=volunteerType,
                                   users=users,
                                   sponsors=sponsors,
                                   name=getName(personal_user_id),
                                   state="leave",
                                   buttonName="Отказаться от спонсирования")
    else:
        if Log.query.filter_by(user_email=personal_user_email, event_id=id).first() is None:
            isAuth = "display: none"
            noAuth = "display: none"
            if check_user(personal_user_email, personal_user_password, personal_user_id):
                isAuth = ""
            else:
                noAuth = ""
            buttonName = "Участвовать"
            if is_volunteer(personal_user_id):
                if get_age(UserInfo.query.filter_by(email=personal_user_email).first().birth) < age:
                    available = "disabled"
            if available == "disabled":
                buttonName = "Вы не можете участвовать"
            return render_template("AboutEvent.html",
                                   isAuth=isAuth,
                                   noAuth=noAuth,
                                   title=title,
                                   metro=metro,
                                   age=age,
                                   count=count,
                                   data=data,
                                   description=description,
                                   volunteerType=volunteerType,
                                   users=users,
                                   sponsors=sponsors,
                                   name=getName(personal_user_id),
                                   available=available,
                                   state="join",
                                   buttonName=buttonName)
        else:
            isAuth = "display: none"
            noAuth = "display: none"
            if check_user(personal_user_email, personal_user_password, personal_user_id):
                isAuth = ""
            else:
                noAuth = ""
            available = ""
            buttonName = "Отказаться от участия"
            if is_volunteer(personal_user_id):
                if get_age(UserInfo.query.filter_by(email=personal_user_email).first().birth) < age:
                    available = "disabled"
            if available == "disabled":
                buttonName = "Вы не можете участвовать"
            return render_template("AboutEvent.html",
                                   isAuth=isAuth,
                                   noAuth=noAuth,
                                   title=title,
                                   metro=metro,
                                   age=age,
                                   count=count,
                                   data=data,
                                   description=description,
                                   volunteerType=volunteerType,
                                   users=users,
                                   sponsors=sponsors,
                                   name=getName(personal_user_id),
                                   available=available,
                                   state="leave",
                                   buttonName=buttonName)


@app.route("/event/<id>/edit", methods=["GET", "POST"])
def edit_event(id):
    try:
        personal_user_id = session['id']
        personal_user_email = session['email']
        personal_user_password = session['password']
    except:
        personal_user_id = -1
        personal_user_email = ""
        personal_user_password = ""
    if check_user(personal_user_email, personal_user_password, personal_user_id):
        event = Event.query.get(id)
        if event is None:
            return redirect("/404")
        if event.email == personal_user_email:
            if event.data < datetime.now():
                return redirect(f"/event/{id}")
            if request.method == "GET":
                typeEdit = "Редактирование мероприятия"
                title = event.title
                description = event.description
                metro = event.metro
                selected = ["" for i in range(9)]
                selected[int(event.number)] = "selected"
                data = event.data.strftime("%Y-%m-%d")
                if event.count == -1:
                    count = ""
                else:
                    count = str(event.count)
                age = event.ages
                return render_template("edit_event.html",
                                       metro=metro,
                                       personal_user_id=personal_user_id,
                                       typeEdit=typeEdit,
                                       title=title,
                                       description=description,
                                       volunteer0=selected[0],
                                       volunteer1=selected[1],
                                       volunteer2=selected[2],
                                       volunteer3=selected[3],
                                       volunteer4=selected[4],
                                       volunteer5=selected[5],
                                       volunteer6=selected[6],
                                       volunteer7=selected[7],
                                       volunteer8=selected[8],
                                       data=data,
                                       count=count,
                                       ages=age)
            else:
                title = request.form.get("titleForm")
                description = request.form.get("descriptionForm")
                number = int(request.form.get("numberForm"))
                metro = request.form.get("metroForm")
                tempData = list(map(int, request.form.get("dateForm").split("-")))
                data = datetime(year=tempData[0], month=tempData[1], day=tempData[2])
                count = request.form.get("countForm")
                if count is None or len(str(count)) == 0:
                    count = -1
                else:
                    count = int(count)
                ages = int(request.form.get("agesForm"))
                event.title=title
                event.description=description
                event.number=number
                event.metro=metro
                event.data=data
                event.count=count
                try:
                    db.session.commit()
                    return redirect(f"/event/{id}")
                except:
                    return "ERROR"
        else:
            isAuth = "hidden"
            if personal_user_id != -1:
                isAuth = ""
            return render_template("permission_denied.html", personal_user_id=personal_user_id, isAuth=isAuth)
    else:
        return redirect("/login")


@app.route("/confirm-recovery/<code>", methods=["GET", "POST"])
def confirm_recovery(code: str):
    try:
        personal_user_id = session['id']
        personal_user_email = session['email']
        personal_user_password = session['password']
    except:
        personal_user_id = -1
        personal_user_email = ""
        personal_user_password = ""
    if check_user(personal_user_email, personal_user_password, personal_user_id):
        return redirect(f"/profile/{personal_user_id}")
    state = Recovery.query.filter_by(code=code).first()
    if state is None:
        return render_template("confirm_error.html", personal_user_id=personal_user_id)
    if (datetime.now() - state.date).seconds > 900 or (datetime.now() - state.date).days > 0:
        return render_template("confirm_error.html", personal_user_id=personal_user_id)
    if request.method == "GET":
        return render_template("recovery_new_password.html", error="", personal_user_id=personal_user_id)
    else:
        password = request.form.get("passwordForm")
        passwordSubmit = request.form.get("passwordSubmitForm")
        if password != passwordSubmit:
            return render_template("recovery_new_password.html", error="Пароли не совпадают!", personal_user_id=personal_user_id)
        user = User.query.filter_by(email=state.email).first()
        user.password = password
        try:
            db.session.delete(state)
            db.session.commit()
            return render_template("recovery_success.html", personal_user_id=personal_user_id)
        except:
            return render_template("recovery_new_password.html", error="Что-то пошло не так! Попробуйте еще раз!", personal_user_id=personal_user_id)


@app.route("/events", methods=["GET", "POST"])
def events():
    session['need_to_redirect'] = ''
    try:
        personal_user_id = session['id']
        personal_user_email = session['email']
        personal_user_password = session['password']
    except:
        personal_user_id = -1
        personal_user_email = ""
        personal_user_password = ""
    if request.method == "POST":
        if request.form.get("eventType") == "off":
            return redirect("/events")
        filterMetro = request.form.get("filterMetro")
        filterNumber = request.form.get("filterNumber")
        filterDate = request.form.get("filterDate")
        requestFormat = []
        if filterMetro != "":
            requestFormat.append(f"filterMetro={filterMetro}")
        if filterNumber != "-1":
            requestFormat.append(f"filterNumber={filterNumber}")
        print(filterDate)
        if filterDate != "":
            requestFormat.append(f"filterDate={filterDate}")
        return redirect(f"/events?{'&'.join(requestFormat)}")
    events = Event.query.order_by(Event.data).all()
    filterMetro = request.args.get("filterMetro")
    if filterMetro is None:
        filterMetro = ""
    filterNumber = request.args.get("filterNumber")
    checked = ["" for i in range(10)]
    if filterNumber is None:
        checked[9] = "selected"
        filterNumber = ""
    else:
        checked[int(filterNumber)] = "selected"
    filterDate = request.args.get("filterDate")
    StartWorkDate = None
    FinishWorkDate = None
    if filterDate is not None:
        tmp = list(map(int, filterDate.split("-")))
        StartWorkDate = datetime(year=tmp[0], month=tmp[1], day=tmp[2])
        FinishWorkDate = StartWorkDate + timedelta(days=1)
    l = 0
    r = len(events)
    nowTime = datetime.now()
    while l + 1 < r:
        m = (l + r) // 2
        if events[m].data < nowTime:
            l = m
        else:
            r = m
    if r == 1 and events[0].data > nowTime:
        r = 0
    activeEvents = []
    volunteerTypes = ["Патриотическое", "Социальное",
                      "Спортивное", "Событийное",
                      "Культурное", "Добровольцы МЧС",
                      "Эко", "Медицинское",
                      "Туристическое"]
    for i in range(r, len(events)):
        filterOk = True
        if filterMetro != "":
            filterOk = min(filterOk, events[i].metro == filterMetro)
        if filterNumber != "":
            filterOk = min(filterOk, int(events[i].number) == int(filterNumber))
        if filterDate is not None:
            if not (StartWorkDate <= events[i].data < FinishWorkDate):
                break
        if not filterOk:
            continue
        activeEvents.append({})
        activeEvents[-1]['title'] = events[i].title
        activeEvents[-1]['description'] = events[i].description
        activeEvents[-1]['metro'] = events[i].metro
        activeEvents[-1]['volunteer'] = volunteerTypes[int(events[i].number)]
        if events[i].count == -1:
            activeEvents[-1]['count'] = "Неограниченно"
        else:
            activeEvents[-1]['count'] = events[i].count - events[i].used
        activeEvents[-1]['data'] = events[i].data.strftime("%d.%m.%Y")
        activeEvents[-1]['ages'] = events[i].ages
        activeEvents[-1]['isActive'] = "Активно"
        activeEvents[-1]['id'] = events[i].id
    isSearcher = "hidden"
    if is_searcher(personal_user_id):
        isSearcher = ""
    isAuth = "display: none"
    noAuth = "display: none"
    if check_user(personal_user_email, personal_user_password, personal_user_id):
        isAuth = ""
    else:
        noAuth = ""
    return render_template("events.html",
                           events=activeEvents,
                           personal_user_id=personal_user_id,
                           isSearcher=isSearcher,
                           isAuth=isAuth,
                           noAuth=noAuth,
                           filterMetro=filterMetro,
                           filterDate=filterDate,
                           volunteerNone=checked[9],
                           volunteer0=checked[0],
                           volunteer1=checked[1],
                           volunteer2=checked[2],
                           volunteer3=checked[3],
                           volunteer4=checked[4],
                           volunteer5=checked[5],
                           volunteer6=checked[6],
                           volunteer7=checked[7],
                           volunteer8=checked[8])


@app.route("/profile/<id>/events", methods=["GET", "POST"])
def events_profile(id: int):
    session['need_to_redirect'] = ''
    try:
        personal_user_id = session['id']
        personal_user_email = session['email']
        personal_user_password = session['password']
    except:
        personal_user_id = -1
        personal_user_email = ""
        personal_user_password = ""
    hiddenFilter = "hidden"
    if personal_user_id == id:
        if not check_user(personal_user_email, personal_user_password, personal_user_id):
            return redirect("/login")
    if not ready(id):
        return redirect("/404")
    if request.method == "POST":
        try:
            return redirect("/event/" + request.form.get('openEvent'))
        except:
            return
    user = User.query.get(id)
    events = []
    if user.role == "volunteer":
        for i in Log.query.filter_by(user_email=user.email).all():
            events.append(Event.query.get(i.event_id))
    elif user.role == "searcher":
        events = Event.query.filter_by(email=user.email).all()
    elif user.role == "business":
        for i in BusinessLog.query.filter_by(business_email=user.email).all():
            events.append(Event.query.get(i.event_id))
    events.sort(key=lambda x: x.data)
    events.reverse()
    activeEvents = []
    for i in range(len(events)):
        activeEvents.append({})
        activeEvents[-1]['title'] = events[i].title
        activeEvents[-1]['description'] = events[i].description
        activeEvents[-1]['metro'] = events[i].metro
        if events[i].count == -1:
            activeEvents[-1]['count'] = "Неограниченно"
        else:
            activeEvents[-1]['count'] = events[i].count - events[i].used
        activeEvents[-1]['data'] = events[i].data.strftime("%d.%m.%Y")
        activeEvents[-1]['ages'] = events[i].ages
        activeEvents[-1]['isActive'] = "Активно"
        if events[i].data < datetime.now():
            activeEvents[-1]['isActive'] = "Завершено"
        activeEvents[-1]['id'] = events[i].id
    isSearcher = "hidden"
    if is_searcher(personal_user_id):
        isSearcher = ""
    isAuth = "hidden"
    if personal_user_id != -1:
        isAuth = ""
    return render_template("events.html", hiddenFilter=hiddenFilter, events=activeEvents, personal_user_id=personal_user_id, isSearcher=isSearcher, isAuth=isAuth)


@app.errorhandler(404)
def page_not_found(e):
    try:
        personal_user_id = session['id']
    except:
        personal_user_id = -1
    return render_template('404.html', personal_user_id=personal_user_id), 404


if __name__ == "__main__":
    app.run(debug=True)
