import click
import pandas as pd
import sqlite3 as sq
from flask import current_app, g

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

@click.command("init-db")
def init_db_command():
    db = get_db()

    # Initalize schools DB
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))

    # Initialize Dell Key DB
    df = pd.read_csv('reportautomator/static/Dell_Key.csv')
    df.columns = df.columns.str.strip()
    df.to_sql('dellkey', db, if_exists='replace', index=False)

    click.echo("You successfully initialized the database!")

def get_db():
    if 'db' not in g:
        g.db = sq.connect(
            current_app.config['DATABASE'],
            detect_types=sq.PARSE_DECLTYPES,
        )
        g.db.row_factory = sq.Row
    
    return g.db