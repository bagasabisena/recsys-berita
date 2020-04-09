import sqlite3
import random

from flask import Flask, render_template, abort, redirect, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    random_id = random.randint(0, 28393)
    return redirect(url_for('news', id=random_id))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/news/<id>')
def news(id):
    db = sqlite3.connect('db.sqlite3')
    qry = 'SELECT * FROM news WHERE id=?'
    c = db.cursor()
    c.execute(qry, (id,))
    data = c.fetchone()
    if not data:
        abort(404)
    
    id_, title, body, rel_raw = data
    data = {
        'id': id_,
        'title': title,
        'body': body.split('\n')
    }

    # now getting the relations
    related_ids = rel_raw.split(',')
    qry = 'SELECT * FROM news WHERE id IN ({})'.format(
        ','.join('?'*len(related_ids))
    )
    c.execute(qry, related_ids)
    related_rows = c.fetchall()
    related_data = [
        {'id': row[0], 'title': row[1], 'body': row[2].split('.')[0] + '.'}
        for row in related_rows
    ]
    return render_template('content.html', main=data, related=related_data)
