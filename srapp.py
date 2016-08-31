import os
import sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, flash


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'database.db'),
    SECRET_KEY='development key'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('SELECT * FROM entries ORDER BY id DESC')
    entries = cur.fetchall()
    return render_template('list.html', entries=entries)


@app.route('/story', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        db = get_db()
        db.execute('insert into entries (title, story, criteria, value, estimation, status) values (?, ?, ?, ?, ?, ?)',
                   [request.form['title'], request.form['story'], request.form['criteria'],
                    request.form['value'], request.form['estimation'], request.form['status']])
        db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'))
    else:
        return render_template('form.html', title='new')


@app.route('/story/<story_id>', methods=['GET'])
def show_story(story_id):
    ID = story_id
    global ID #fucking flask url encoding!
    db = get_db()
    cur = db.execute('SELECT * FROM entries WHERE id = {}'.format(story_id))
    entries = cur.fetchall()
    return render_template('form.html', title='edit', entries=entries)


@app.route('/story/<story_id>', methods=['POST'])
def edit_story(story_id):
    db = get_db()
    db.execute("UPDATE entries SET title=?, story=?, criteria=?, value=?, estimation=?, status=? WHERE id=?",
               (request.form['title'], request.form['story'], request.form['criteria'],
                request.form['value'], request.form['estimation'], request.form['status'], ID))
    db.commit()
    flash('Entry was successfully updated!')
    return redirect(url_for('show_entries'))


@app.route('/delete', methods=['POST'])
def delete_row():
    db = get_db()
    db.execute("DELETE FROM entries WHERE id=?", (request.form['bin']))
    db.commit()
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    init_db()
    app.run()
