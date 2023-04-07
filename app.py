import os

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text, text, delete, insert
from sqlalchemy.sql.expression import update, select

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure Application
app = Flask(__name__)

# Ensure templates are auto reloded
app.config["TEMPLATES_AUTO_RELOD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Making connection to the database
engine = create_engine("sqlite:///data.db", echo = False, connect_args={"check_same_thread": False})
conn = engine.connect()

# Make Tables:
meta = MetaData()
users = Table(
    'users', meta,
    Column('id', Integer, primary_key = True),
    Column('username', Text),
    Column('hash', Text),
    Column('exclusive', Integer),   # 0 for normal patients and other numbers for different staffs(future scope), now only 1 for official staffs 
)

inventory = Table(
    'inventory', meta,
    Column('m_id', Integer, primary_key = True),
    Column('m_name', Text),
    Column('m_quantity', Integer),
)

p_history = Table(
    "p_history", meta,
    Column('p_id', Integer),
    Column('d_id', Integer),
    Column('problem', Text),
    Column('med', Text),
)

meta.create_all(engine)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# HOME PAGE ----------------------------------------
@app.route("/")
def home():
    # s = users.select().where(users.c.id == session['user_id'])
    # result = conn.execute(s)
    # for row in result:
    #     req = row[3]
    #     if req == None:
    #         req = 0
    return render_template('landing-page.html')
#---------------------------------------------------

# LOGIN and REGISTER ----------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("register.html")
    username = request.form.get('username')
    password = request.form.get('password')
    confirmation = request.form.get('confirmation')

    user = text('SELECT username, id FROM users')
    result = conn.execute(user)
    u_l = []
    id = 0
    for row in result:
        u_l.append(row[0])
        id = row[1]
    if username == '' or username in u_l:
        return apology('input is blank or the username already exists.')
    u_l = []
    if password == '' or password != confirmation:
        return apology('Password input is blank or the passwords do not match.')

    # id = db.execute('INSERT INTO users(username, hash) VALUES(?, ?)', username, generate_password_hash(password))
    ins = users.insert().values(username = username, hash = generate_password_hash(password), exclusive = 0)
    conn.execute(ins)

    session['user_id'] = id

    return render_template("after-login.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        
        # Query database for username
        #Can make better
        user = text('SELECT username, hash, id FROM users')
        result = conn.execute(user)
        for row in result:
            if row[0] == request.form.get("username"):
                if check_password_hash(row[1], request.form.get("password")):
                    session['user_id'] = row[2]
                    return render_template("after-login.html")
        
        return apology('Sorry We cannot find you right now')
    
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
# --------------------------------------------------------------
