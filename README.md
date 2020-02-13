## Backend API

# Python: 3.6.9 : Flask: 1.1.1

### Installation steps:
`sudo apt-get install python3-venv`  Install venv for python3

`python3 -m venv venv` Create venv dir

`source venv/bin/activate` Activate venv

`python --version`  Chk python version, it should show 3.6.9

`source venv/bin/activate` Activate venv

### `FLASK_ENV=development flask run`
Runs the app in the development mode.
Open http://localhost:5000/ to view it in the browser.

Use `pip freeze > requirements.txt` command each time when install any new package so that we can maintain the cross platform dependency 

