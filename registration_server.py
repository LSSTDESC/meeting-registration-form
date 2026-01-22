import os
import argparse
from flask import Flask, render_template, request, redirect, url_for, Response, make_response
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql.sqltypes import Boolean
#  from sqlalchemy import and_

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db').replace("s://", "sql://", 1)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '')
db = SQLAlchemy(app)


# Defines the registration entry
class Participant(db.Model):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    affiliation = db.Column(db.String(200))

    # For statistics.  Also sometimes used to determine reg. fee
    early_career = db.Column(db.String(5))

    # All of the following are visible only for in-person
    # Some should perhaps be restricted just to U of I, not satellites
    in_person = db.Column(db.String(5))
    site = db.Column(db.String(20))    # One of "U of I", "Paris", ...
    lname = db.Column(db.String(100))
    sname = db.Column(db.String(100))
    pronoun = db.Column(db.String(100))
    sprint = db.Column(db.String(5))
    poster = db.Column(db.String(5))
    de_school = db.Column(db.String(5))               # UI only
    # dinner = db.Column(db.String(5))                 # UI only
    # dinner_plus_one = db.Column(db.String(5))        # UI only
    # Tshirt_size = db.Column(db.String(5))            # UI only
    # dietary = db.Column(db.String(500))

    contact = db.Column(db.String(5))
    volunteer = db.Column(db.String(5))

    CL = db.Column(db.String(5))
    CO = db.Column(db.String(5))
    CSS = db.Column(db.String(5))
    DKM = db.Column(db.String(5))
    MCP = db.Column(db.String(5))
    PLC = db.Column(db.String(5))
    PO = db.Column(db.String(5))
    PZ = db.Column(db.String(5))
    SA = db.Column(db.String(5))
    SC = db.Column(db.String(5))
    SRV = db.Column(db.String(5))
    TD = db.Column(db.String(5))
    WLSS = db.Column(db.String(5))
    Social = db.Column(db.String(5))

    recording = db.Column(db.String(5))
    code_of_conduct = db.Column(db.String(5))

    speedchat = db.Column(db.String(5))

    def __repr__(self):
        return '<Participant: %r %r %r %r %r %r %r %r %r [%r]>' % (self.first_name, self.last_name, self.CL, self.CO, self.CSS, self.DKM, self.MCP, self.PLC, self.email)


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
        return ("Email already registered",
                {'Access-Control-Allow-Origin': '*'})


@app.route('/register', methods=['POST'])
@requires_auth
def register():
    # Extract fields from form data and create participant
    kwargs = {k: request.form[k] for k in request.form}

    # Remove secret field
    del kwargs['secret']

    # Special for July 2025 Collaboration Meeting
    if 'in_person' not in kwargs:
        kwargs['site'] = 'Remote'
    elif kwargs['in_person'] != 'on':
        kwargs['site'] = 'Remote'

    participant = Participant(**kwargs)

    db.session.add(participant)
    db.session.commit()
    if participant.in_person == 'on':
        if participant.site == 'UI':
            payment_link = 'https://appserv7.admin.uillinois.edu/FormBuilderSurvey/Survey/ncsa/aspo/desc/Survey'
            r = make_response(render_template('payment_UI.html',
                                              data=participant,
                                              payment_link=payment_link))
        else:
            r = make_response(render_template('success.html', data=participant))
    else:
        r = make_response(render_template('success.html', data=participant))

    r.headers.set('Access-Control-Allow-Origin', "*")
    return r


@app.route('/', methods=['GET'])
def registered():
    """Returns the list of registered participants
    """
    # Get list of participants
    participants = Participant.query.order_by(Participant.last_name, Participant.first_name).with_entities(Participant.first_name, Participant.last_name, Participant.affiliation, Participant.in_person, Participant.site).all()
    in_persons = [p for p in participants if p.in_person == "on"]
    n_in_person = len(in_persons)
    n_remote = len(participants) - n_in_person
    return render_template('participants.html', data=participants,
                           n_in_person=n_in_person, n_remote=n_remote)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--create", action='store_true')
    parser.add_argument("--dump", action='store_true')
    parser.add_argument("--drop", action='store_true')
    args = parser.parse_args()

    if args.create:
        print("Creating database table if it doesn't exist")
        with app.app_context():
            db.create_all()
    elif args.drop:
        print("Dropping database table if it exists")
        with app.app_context():
            db.drop_all()

    if args.dump:
        print("Printing content of database.")
        with app.app_context():
            for p in Participant.query.all():
                print(p)
