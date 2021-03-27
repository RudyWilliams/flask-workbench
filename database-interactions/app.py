from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_name = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(35), unique=True, nullable=False)
    f_name = db.Column(db.String(25), nullable=False)
    l_name = db.Column(db.String(25), nullable=True)
    budget = db.relationship("Budget", backref="user", lazy="dynamic")


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    super_category = db.Column(db.String(15), nullable=True)
    category = db.Column(db.String(15), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    __table_args__ = (
        db.UniqueConstraint(
            "user_id", "category", name="user_category_uniq_constraint"
        ),
    )


# only run once to initialize the db
# db.create_all()
