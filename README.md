# WEATHER APPLICATION
#### Video Demo:  <https://youtu.be/RTYzpxZKVEE>
#### Description:
First let me introduce my final project:
After week 9 of cs50x2023 I was strongly inspired how to bulit a website using html css and flask. So I want to make a WEATHER APPLICATION of my own.

### Project using:
Python, HTML, CSS, Flask, Jinja and SQL

#### App function:
#### First
When access to the web-based application, it will require user to have an account, html code from login.html will be rendered and extented with code from layout.html.

If user don't have an account, they can create one by cliking register. app.py will automaticaly render register.html and show a form to ask username, password and confirmation. If any error, app.py will render error.html and error message.

After create an account, their information will be stored in data.db about username, hash_password and log the user in.

login.html will show a form to ask username and password before log user in. If any error, error.html will be rendered.

#### Second
When successfuly log the user in, Index.html will be rendered and show a form ask the user current location or user can type in any location that they want to look up weather informations.

When provide the city name, in app.py. The program will access to openweather and use some API that the web provide and store information in a dictionary name data.

If no city was found, error.html and message will be rendered.

After collecting all the weather data, weather.html will be rendered and show some informations about name of the city, current temperature in Celcius, general weather, temperature details, wind speed, humidity, visibility, sunset time and sunrise time.

weather.html also show 2 map collect from windy.com, one is wind map and one is cloud map from surrounding areas.

#### Last
app.py does the most job of the project. In charge of routing html files, collecting datas, computing some equations. By using flask and jinja, app.py can access to html code and built a functional web-base application.

In static folder, it contains style.css which decorate the asthetic of the web. But the project also use bootstrap framework that can boost the project's working time.

layout.html built the skeleton of the web so that keep the unification of the app.

data.db is the batabase that store information of user in a table users. It store the user's id, username. password and their address. The data of them will be use for loging them to the app and can be analysed that where the user care about weather most.
