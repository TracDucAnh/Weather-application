import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import datetime as dt
import requests
import math

db = SQL("sqlite:///data.db")

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        if not request.form.get("city"):
            return render_template("/error.html", error_message = "City not found")
        BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
        API_KEY = "c9de69a3b0b5117399bfe1a64b3b88f1"
        CITY = request.form.get("city")
        url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
        data = requests.get(url).json()
        cod = data["cod"]
        if cod == '404':
            return render_template("/error.html", error_message = "City not found")
        temp_C = round(data["main"]["temp"] - 273.15,2)
        temp_F = round(temp_C * (9/5) + 32,2)

        temp_C_feel = round(data["main"]["feels_like"] - 273.15,2)
        temp_F_feel = round(temp_C_feel * (9/5) + 32, 2)

        sunrise_time = dt.datetime.utcfromtimestamp(data["sys"]["sunrise"] + data["timezone"])
        sunset_time = dt.datetime.utcfromtimestamp(data["sys"]["sunset"] + data["timezone"])

        wind_map = "https://embed.windy.com/embed2.html?lat=" + str(data["coord"]["lat"]) + "&lon=" +str(data["coord"]["lon"]) +"&detailLat=" + str(data["coord"]["lat"]) +"&detailLon=" + str(data["coord"]["lon"]) + "&width=650&height=450&zoom=5&level=surface&overlay=wind&product=ecmwf&menu=&message=&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"

        cloud_map = "https://embed.windy.com/embed2.html?lat="+ str(data["coord"]["lat"]) +"&lon="+ str(data["coord"]["lon"]) +"&detailLat="+ str(data["coord"]["lat"]) +"&detailLon="+ str(data["coord"]["lon"]) +"&width=650&height=450&zoom=5&level=surface&overlay=clouds&product=ecmwf&menu=&message=&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"

        UV = "https://embed.windy.com/embed2.html?lat="+ str(data["coord"]["lat"]) +"&lon="+ str(data["coord"]["lon"]) +"&detailLat="+ str(data["coord"]["lat"]) +"&detailLon="+ str(data["coord"]["lon"]) +"&width=650&height=450&zoom=5&level=surface&overlay=wind&product=ecmwf&menu=&message=&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"
        return render_template("/weather.html", data = data, temp_F = temp_F, temp_C = temp_C, temp_F_feel = temp_F_feel, temp_C_feel = temp_C_feel, sunset = sunset_time, sunrise = sunrise_time, wind_map = wind_map, cloud_map = cloud_map, UV = UV)
    else:
        return render_template("/index.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        usernames = db.execute("SELECT username FROM users;")
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        hash = generate_password_hash(password, method="pbkdf2", salt_length=16)
        for username in usernames:
            if name == username["username"]:
                error = "Username alredy exists"
                return render_template("/error.html", error_message = error)

        if password != confirmation:
            error = "Password and confirmation don't match"
            return render_template("/error.html", error_message = error)

        elif not request.form.get("username"):
            error = "Must provide username"
            return render_template("/error.html", error_message = error)

        elif not request.form.get("password"):
            error = "Must provide password"
            return render_template("/error.html", error_message = error)

        elif not request.form.get("confirmation"):
            error = "must provide confirmation"
            return render_template("/error.html", error_message = error)

        create_account = True
        try:
            insert_account = (
                "INSERT INTO users (username, hash_password) VALUES ("
                + "'"
                + name
                + "'"
                + ", "
                + "'"
                + hash
                + "');"
            )
            db.execute(insert_account)
        except:
            create_account = False
        # Redirect user to home page

        if create_account == True:
            id = db.execute("SELECT id FROM users WHERE username = ?;", name)
            session["user_id"] = id[0]["id"]
            return redirect("/")
        else:
            return render_template("/register.html")
    else:
       return render_template("/register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            error = "must provide username"
            return render_template("/error.html", error_message = error)
        elif not request.form.get("password"):
            return render_template("/error.html", error_message = "Must provide password")
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash_password"], request.form.get("password")
        ):
            return render_template("/error.html", error_message = "invalid username and/or password")
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")
