# -*- coding: utf-8 -*

import json
import random
import string

from flask import Flask, session, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'JIOH7injbn*jnbjbn'
app_url = ''
mxj_url = 'http://127.0.0.1:5000'
users_db = {'mxj': 'haslo'}
urls_db = {}
chars = string.ascii_letters + string.digits
pwdSize = 6


@app.route(app_url + '/')
def index():
    if 'username' not in session:
        username = 'Nieznajomy'
        logged = False
    else:
        username = session['username']
        logged = True
    return render_template('start.html', logged=logged, username=username, shortener=url_for('shortener'), listoflinks=url_for('listoflinks'), logout=url_for('logout'), login=url_for('login'), register=url_for('register'))



@app.route(app_url + '/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login_form.html', message='', home=url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users_db and password == users_db[username]:
            session['username'] = username
            logged = True
            return render_template('start.html', logged=logged, username=username, shortener=url_for('shortener'), listoflinks=url_for('listoflinks'), logout=url_for('logout'), login=url_for('login'), register=url_for('register'))
        else:
            message = u'Niepoprawny login i/lub hasło'
            return render_template('login_form.html', message=message, home=url_for('index'))


@app.route(app_url + '/logout')
def logout():
    session.pop('username', None)
    return redirect(mxj_url + app_url)


@app.route(app_url + '/shortener', methods=['GET', 'POST'])
def shortener():
    if request.method == 'GET':
        return render_template('url_shortener.html', url='', short_url='', home=url_for('index'))
    if request.method == 'POST':
        if request.form.get('url')!= '':
            url = request.form.get('url')
            generated_url = mxj_url + app_url + '/' + ''.join((random.choice(chars)) for x in range(pwdSize))
            urls_db[generated_url] = url
            return render_template('url_shortener.html', url=url, short_url=generated_url, home=url_for('index'))
        else:
            return render_template('url_shortener.html', url='', short_url='', home=url_for('index'))


@app.route(app_url + '/<url_code>')
def redirecting(url_code):
    generated_url = mxj_url + app_url + '/' + url_code
    if generated_url in urls_db:
        if 'http://' not in urls_db[generated_url]:
            url = 'http://' + urls_db[generated_url]
        else:
            url = urls_db[generated_url]
        return redirect(url, 302)
    else:
        return render_template('error.html', home=url_for('index'))


@app.route(app_url + '/listoflinks')
def listoflinks():
    if 'username' not in session:
        message = u'Dostęp tylko dla zalogowanych!'
        return render_template('login_form.html', message=message, home=url_for('index'))
    else:
        return render_template('list.html', urls_db=urls_db, home=url_for('index'), database=url_for('database'))


@app.route(app_url + '/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', message='', home=url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username not in users_db:
            users_db[username] = password
            message = 'Zarejestrowano pomyślnie'
        else:
            message = 'Podana nazwa użytkownika jest już zajęta, wybierz inną'
        return render_template('register.html', message=message, home=url_for('index'))


@app.route(app_url + '/database')
def database():
    if 'username' not in session:
        message = u'Dostęp tylko dla zalogowanych!'
        return render_template('login_form.html', message=message, home=url_for('index'))
    else:
        return render_template('database_options.html', message='', save=url_for('save'), read=url_for('read'), home=url_for('index'))


@app.route(app_url + '/database/read')
def read():
    if 'username' not in session:
        message = u'Dostęp tylko dla zalogowanych!'
        return render_template('login_form.html', message=message, home=url_for('index'))
    else:
        text_file = open('/database.txt', 'r')
        database = json.loads(text_file.read())
        urls_db.update(database)
        text_file.close()
        message = u'Wczytano bazę danych'
        return render_template('database_options.html', message=message, save=url_for('save'), read=url_for('read'), home=url_for('index'))


@app.route(app_url + '/database/save')
def save():
    if 'username' not in session:
        message = u'Dostęp tylko dla zalogowanych!'
        return render_template('login_form.html', message=message, home=url_for('index'))
    else:
        text_file = open('/database.txt', 'w')
        text_file.write('%s' % json.dumps(urls_db))
        text_file.close()
        message = u'Zapisano bazę do pliku'
        return render_template('database_options.html', message=message, save=url_for('save'), read=url_for('read'), home=url_for('index'))


if __name__ == '__main__':
    app.run()
