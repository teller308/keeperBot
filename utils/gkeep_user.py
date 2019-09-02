from flask_sqlalchemy import SQLAlchemy

from bot import application

db = SQLAlchemy(application)


class GKeepUser(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    tg_user_id = db.Column(db.Integer, unique=True, nullable=False)
    tg_user_name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return 'User {}:{} - {}'.format(
            self.tg_user_id, self.tg_username, self.email)
