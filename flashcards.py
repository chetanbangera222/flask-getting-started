from flask import Flask, render_template, abort, jsonify, request,redirect,url_for
from model import db,save_db

app = Flask(__name__)
counter = 0


@app.route("/")
def welcome():
    return render_template('welcome.html', message='This is passed from app', cards=db)


@app.route("/views")
def check_counter():
    global counter
    counter += 1
    return "This page is called " + str(counter) + " times"


@app.route("/card/<int:index>")
def card_view(index):
    try:
        card = db[index]
        return render_template('card.html', card=card, index=index, max_index=len(db) - 1)
    except IndexError:
        abort(404)


@app.route("/add_card", methods=['GET', 'POST'])
def add_card():
    try:
        if request.method == 'POST':
            card = {"question" : request.form['question'],"answer" : request.form['answer']}
            db.append(card)
            return redirect(url_for('card_view', index=len(db)-1))
        else:
            return render_template('add_card.html')
    except IndexError:
        abort(404)

@app.route("/remove_card/<int:index>", methods=['GET', 'POST'])
def remove_card(index):
    try:
        if request.method == 'POST':
            del(db[index])
            save_db()
            return redirect(url_for('welcome'))
        else:
            return render_template('remove_card.html',card=db[index])
    except IndexError:
        abort(404)

@app.route("/api/card/<int:index>")
def card_view_list(index):
    try:
        return db[index]
    except IndexError:
        abort(404)


@app.route("/api/card/")
def card_view_list_all():
    try:
        # print("=============")
        # print(db)
        # print("=============")
        # print(jsonify(db))
        # print("=============")
        return jsonify(db)
    except IndexError:
        abort(404)
