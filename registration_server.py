import os
import argparse
from flask import Flask, render_template, request, redirect, url_for, Response, make_response
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy import and_

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db').replace("s://", "sql://", 1)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '')
db = SQLAlchemy(app)

# Defines the registration entry
class Participant(db.Model):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200))
    last_name  = db.Column(db.String(200))
    email = db.Column(db.String(200))
    affiliation = db.Column(db.String(200))
    early_career = db.Column(db.String(5))
    in_person = db.Column(db.String(5))
    lname = db.Column(db.String(100))
    sname = db.Column(db.String(100))
    pronoun = db.Column(db.String(100))
    deschool = db.Column(db.String(5))
    sprint = db.Column(db.String(5))
    poster = db.Column(db.String(5))
    dinner = db.Column(db.String(5))
    dinner_plus_one = db.Column(db.String(5))
    dietary = db.Column(db.String(200))
    contact = db.Column(db.String(5))
    volunteer = db.Column(db.String(5))

    covid_rules = db.Column(db.String(5))

    CL = db.Column(db.String(5))
    LSS = db.Column(db.String(5))
    TD = db.Column(db.String(5))
    WL = db.Column(db.String(5))
    BL = db.Column(db.String(5))
    CO = db.Column(db.String(5))
    SRV = db.Column(db.String(5))
    CSS = db.Column(db.String(5))
    DKM = db.Column(db.String(5))
    ES = db.Column(db.String(5))
    OS = db.Column(db.String(5))
    PC = db.Column(db.String(5))
    PSF = db.Column(db.String(5))
    PZ = db.Column(db.String(5))
    SA = db.Column(db.String(5))
    MCP = db.Column(db.String(5))
    COM = db.Column(db.String(5))
    DESChool = db.Column(db.String(5))
    Social = db.Column(db.String(5))

    recording = db.Column(db.String(5))
    code_of_conduct = db.Column(db.String(5))

    speedchat = db.Column(db.String(5))


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
        return ("Ok", {'Access-Control-Allow-Origin':'*'})
    else:
        return ("Email already registered", {'Access-Control-Allow-Origin':'*'})

@app.route('/register', methods=['POST'])
@requires_auth
def register():
    # Extract fields from form data and create participant
    kwargs = {k:request.form[k] for k in request.form}
    # Remove secret field
    del kwargs['secret'];
    participant = Participant(**kwargs)
    db.session.add(participant)
    db.session.commit()
    if participant.in_person == 'on':
        # Set the registration fee.
        if participant.early_career == 'on':
            reg_fee = "100"
            reg_fee_link = "https://buy.stripe.com/aEUg28aDb5eFfpCcMS"
        else:
            reg_fee = "225"
            reg_fee_link = "https://buy.stripe.com/bIY7vCeTr7mNcdq28f"
        # Collaboration dinner tickets
        if participant.dinner == 'on':
            if participant.dinner_plus_one == 'on':
                dinner_cost = "100"
                dinner_payment_link = "https://buy.stripe.com/7sI3es5ta9ki1fa8wJ"
            else:
                dinner_cost = "50"
                dinner_payment_link = "https://buy.stripe.com/dR63es7Bi8geaPKaES"
            r = make_response(render_template('payment_stripe.html', data=participant,
                                              reg_fee=reg_fee, reg_fee_link=reg_fee_link,
                                              dinner_cost=dinner_cost,
                                              dinner_payment_link=dinner_payment_link))
        else:
            r = make_response(render_template('payment_stripe_no_dinner.html', data=participant,
                                              reg_fee=reg_fee, reg_fee_link=reg_fee_link))
    else:
        r = make_response(render_template('success.html', data=participant))
    r.headers.set('Access-Control-Allow-Origin',"*")
    return r

@app.route('/', methods=['GET'])
def registered():
    """Returns the list of registered participants
    """
    # Get list of participants
    participants = Participant.query.order_by(Participant.last_name, Participant.first_name).with_entities(Participant.first_name, Participant.last_name, Participant.affiliation).all()
    return render_template('participants.html', data=participants)

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
