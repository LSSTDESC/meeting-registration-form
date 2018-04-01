import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.sqltypes import Boolean

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db')
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
        return '<User %r>' % self.first_name

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
    db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
