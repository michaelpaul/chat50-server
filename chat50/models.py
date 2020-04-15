from datetime import datetime

import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('messages', lazy=True))
    channel = db.Column(db.String(64), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def to_json(self):
        return {
            'channel': self.channel,
            'author': self.user.nickname,
            'avatar': self.user.picture,
            'body': self.body,
            'datetime': self.created_at.isoformat() + 'Z'
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub = db.Column(db.String(64), unique=True, nullable=False)
    nickname = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    picture = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db.drop_all()
    db.create_all()
    click.echo('Initialized the database.')
