import os
from localesexample import app
from flask import render_template, flash, redirect, session, request
from localesexample.locales_en import en
from localesexample.locales_zh import zh

current_path = ""

language={
    'en': en,
    'zh': zh
}

@app.route("/")
@app.route("/home")
def home_page():

    session['current_path'] = request.path
    print(current_path)
    return render_template("index.html", language=language[render_languages()])


@app.route("/about")
def about_page():
    session['current_path'] = request.path
    print(current_path)
    return render_template("about.html", language=language[render_languages()])

@app.route('/changelang')
def change_language():
    if session['lang'] == 'en':
        session['lang'] = 'zh'
        return redirect(session['current_path']);
    else:
        session['lang'] = 'en'
        return redirect(session['current_path'])

def render_languages():
    if not 'lang' in session:
        session['lang'] = 'en'
    return session['lang']