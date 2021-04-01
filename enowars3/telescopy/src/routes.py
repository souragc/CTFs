from app import db
import cryptography.fernet as f
import subprocess as planet
import base64
from planet import Planet
from user import User
from flask import request, jsonify, render_template, Blueprint, session, render_template_string, redirect, url_for
import hashlib
from functools import wraps
from passlib.hash import sha256_crypt
import json
from redis import Redis

routes = Blueprint("routes", __name__)
redis = Redis(host='redis', port=6379)


# Check login state
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('routes.login'))

    return wrap


@routes.route('/')
@is_logged_in
def index():
    planets = Planet.query.all()
    # planets = [p.to_dict() for p in planets]
    # planets = json.dumps(planets)
    # session['planets'] = planets

    if request.method == 'POST':
        planets = Planet.query.all()
        return render_template('index.html', planets=planets)
    return render_template("index.html", planets=planets)


@routes.route('/getPlanet')
@is_logged_in
def get_planet():
    idd = request.args.get('id')
    t = request.args.get('ticket')

    if t is None or not represent_int(t) or idd is None:
        return "provide a valid ticket and id!"

    s = check_ticket_validity(t)
    if s != 2:
        return "Invalid ticket! Try again :)"

    print("REDIS ticket t: {0} and get is: {1}", t, bool(redis.get(t)), flush=True)
    if bool(redis.get(t)):
        return "Ticket was used already!"

    redis.set(t, bytes(True))
    if idd is not None:
        ra = Planet.query.filter(Planet.planetId == idd).first()
        if ra is not None:
            return jsonify(Planet.query.filter(Planet.planetId == idd).first().to_dict())
        else:
            return "Planet not found!"


@routes.route('/addPlanet', methods=['GET', 'POST'])
@is_logged_in
def add_planet():
    try:
        name = request.args.get('name')
        dec = request.args.get('declination')
        ri = request.args.get('rightAscension')
        flag = request.args.get('flag')
    except:
        return "wrong arguments provided"

    if name is None or name == "" or dec is None or dec == "" or ri is None or ri == "" or flag is None or flag == "":
        return "Please provide all planet information!"

    if len(name) > 30 or len(ri) > 15 or len(dec) > 15 or len(flag) > 200:
        return "value too long!"

    if Planet.query.filter_by(name=name).first():
        return "A planet with that name already exists!"

    p = Planet(name, dec, ri, flag)
    iding(p)
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict())


@routes.route('/planet_details')
@is_logged_in
def get_planet_details():
    name = request.args.get('name')
    planeta = None
    if name:
        planets = Planet.query.all()
        # Session vulnerability here.
        # TODO check if too difficult o too easy.
        # session['planets'] = planets
        for p in planets:
            if p.name in name:
                planeta = p.to_dict()
                break
    template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Telescopy</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
          integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
</head>
<body>

<div class="container">
    <div class="card mt-4">
        <div class="card-body">
            <div class="row">
                <div class="col-md-4 mb-3">
                    <label><strong>Name: </strong></label>
                </div>
                <div class="col-md-8 mb-3 ml-0">
                    <label>%s</label>
                </div>
            </div>
            <div class="row">
                <div class="col-md-4 mb-2">
                    <label><strong>Declination: </strong></label>
                </div>
                <div class="col-md-4 mb-3 ml-0">
                    <label>{{ planet.declination }}</label>
                </div>
            </div>
            <div class="row">
                <div class="col-md-4 mb-2">
                    <label><strong>Right Ascension: </strong></label>
                </div>
                <div class="col-md-5 mb-2 ml-0">
                    <label>{{ planet.rightAscension }}</label>
                </div>
            </div>
            <div class="row">
                <div class="col-md-4 mb-2">
                    <label><strong>Location: </strong></label>
                </div>
                <div class="col-md-5 mb-2 ml-0">
                    <label>{{ planet.location }}</label>
                </div>
            </div>
        </div>
    </div>
    <div class="ml-5 pl-5 mt-5">
        <a class="btn btn-secondary" href="/" role="button">Return to Index</a>
    </div>
</div>

<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
        integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
        crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
        integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
        crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
        integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
        crossorigin="anonymous"></script>
</body>
</html>''' % name
    return render_template_string(template, planet=planeta)


@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        try:
            username = request.form['username']
            password_candidate = request.form['password']
        except KeyError:
            username = request.args.get("username")
            password_candidate = request.args.get("password")

        user = User.query.filter_by(username=username).first()

        if not user:
            return "User not found"

        if user.password is not None:
            # Get stored hash
            password = user.password

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session.permanent = True

                session['logged_in'] = True
                session['user'] = user.username

                return redirect(url_for('routes.index'))
            else:
                return "Incorrect password"
        else:
            return "User not found"

    return render_template('login.html')


@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
        except KeyError:
            username = request.args.get("username")
            password = request.args.get("password")

        if username is None or username == "" or password is None or password == "" or len(password) > 15 or len(
                username) > 15:
            return "Invalid username or password"

        user = User.query.filter_by(username=username).first()

        if user:
            return "Username already taken!"

        password = sha256_crypt.encrypt(password)

        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('routes.login'))

    return render_template('register.html')


# Logout
@routes.route('/logout')
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for('routes.login'))


def iding(i):
    e = i.name.encode('utf-8')
    d = i.declination.encode('utf-8')
    r = i.rightAscension.encode('utf-8')
    h = hashlib.sha256(e + d + r)
    i.planetId = h.hexdigest()


def check_ticket_validity(ticket):
    return planet.call("./ticketChecker " + ticket, shell=True)


def calculate_location(bh, angle):
    data = base64.b64encode(str.encode(bh.bhId))
    k = f.Fernet(data)
    bh.location = k.encrypt(str.encode(angle))


def represent_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
