import os
import argparse
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.sqltypes import Boolean

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db')
db = SQLAlchemy(app)

# Defines the registration entry
class Participant(db.Model):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name  = db.Column(db.String(100))
    email = db.Column(db.String(100))
    affiliation = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    sname = db.Column(db.String(100))
    pronoun = db.Column(db.String(100))

    attend_mon = db.Column(db.String(5))
    attend_tue = db.Column(db.String(5))
    attend_wed = db.Column(db.String(5))
    attend_thu = db.Column(db.String(5))
    attend_fri = db.Column(db.String(5))

    code_of_conduct = db.Column(db.String(5))

    def __init__(self, form):
        kwargs = {}
        for k in form:
            kwargs[k] = form[k]
        super(Participant, self).__init__(**kwargs)

    def __repr__(self):
        return '<Participant: %r %r [%r]>' % (self.first_name, self.last_name, self.email)

@app.route('/check_email', methods=['POST'])
def check_email():
    email = request.form['email']
    # Check for already registered email
    if Participant.query.filter(Participant.email == email).count() == 0:
        return ("Ok", {'Access-Control-Allow-Origin':'*'})
    else:
        return ("Email already registered", {'Access-Control-Allow-Origin':'*'})

@app.route('/register', methods=['POST'])
def register():
    participant = Participant(request.form)
    db.session.add(participant)
    db.session.commit()
    return "Registered ok"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--create", action='store_true')
    parser.add_argument("--dump", action='store_true')
    args = parser.parse_args()

    if args.create:
        print("Creating database table if doesn't exist")
        db.create_all()

    if args.dump:
        print("Printing content of database.")
        for p in Participant.query.all():
            print(p)
