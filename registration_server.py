import os
import argparse
import requests
from flask import Flask, render_template, request, redirect, url_for, Response, make_response
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy import and_

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:////tmp/flask_app.db').replace("s://", "sql://", 1)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '')
db = SQLAlchemy(app)

# Defines the registration entry


class Participant(db.Model):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), index=True, unique=True)
    affiliation = db.Column(db.String(100))
    descmember = db.Column(db.String(5))
    in_person = db.Column(db.String(5))
    lname = db.Column(db.String(100))
    sname = db.Column(db.String(100))
    pronoun = db.Column(db.String(100))

    #covid_vaccine = db.Column(db.String(5))
    covid_rules = db.Column(db.String(5))

    monday = db.Column(db.String(5))
    tuesday = db.Column(db.String(5))
    wednesday = db.Column(db.String(5))
    thursday = db.Column(db.String(5))
    friday = db.Column(db.String(5))
    dietary = db.Column(db.String(200))
    access = db.Column(db.String(10))
    contact = db.Column(db.String(5))


    newbie = db.Column(db.String(5))
    first_sprint = db.Column(db.String(5))

    recording = db.Column(db.String(5))
    code_of_conduct = db.Column(db.String(5))

    def __repr__(self):
        return '<Participant: %r %r [%r]>' % (self.first_name, self.last_name, self.email)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.form['secret']
        if not (auth == app.config['SECRET_KEY']):
            return Response('Could not verify your access level for that URL.', 401,
                            {'WWW-Authenticate': 'Include valid "secret" in form data.'})
        return f(*args, **kwargs)
    return decorated


@app.route('/check_email', methods=['POST'])
@requires_auth
def check_email():
    email = request.form['email']
    # Check for already registered email
    if Participant.query.filter(Participant.email == email).count() == 0:
        return ("Ok", {'Access-Control-Allow-Origin': '*'})
    else:
        return ("Email already registered", {'Access-Control-Allow-Origin': '*'})


@app.route('/register', methods=['POST'])
@requires_auth
def register():
    # Extract fields from form data and create participant
    kwargs = {k: request.form[k] for k in request.form}
    # Remove secret field
    del kwargs['secret']
    participant = Participant(**kwargs)
    db.session.add(participant)
    db.session.commit()

    r = make_response(render_template(
        'success.html', data=participant))

    r.headers.set('Access-Control-Allow-Origin', "*")
    return r


@app.route('/', methods=['GET'])
def registered():
    """Returns the list of registered participants
    """
    # Get list of participants
    participants = Participant.query.order_by(Participant.last_name, Participant.first_name).with_entities(
        Participant.first_name, Participant.last_name, Participant.affiliation, Participant.in_person).all()
    in_person = 0
    remote = 0
    for p in participants:
        if p.in_person == "on":
            in_person += 1
        else:
            remote += 1
    return render_template('participants.html', data=participants, in_person_cnt=in_person,
                           remote_cnt=remote)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--create", action='store_true')
    parser.add_argument("--dump", action='store_true')
    args = parser.parse_args()

    if args.create:
        print("Creating database table if doesn't exist")
        with app.app_context():
            db.create_all()

    if args.dump:
        print("Printing content of database.")
        for p in Participant.query.all():
            print(p)
