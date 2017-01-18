from flask import render_template, url_for, jsonify

from app import app


@app.route('/endpoint/<swag>')
def endpoint(swag):
    return jsonify(str(swag)[::-1])


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return 'About you!'
