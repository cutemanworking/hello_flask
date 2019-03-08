from flask import Flask, render_template, session, redirect, url_for, flash
from flask import request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['MAIL_SUPPRESS_SEND'] = os.environ.get('MAIL_SUPPRESS_SEND')
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
app.config['MAIL_SENDER'] = os.environ.get('MAIL_SENDER')

mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)


class Role(db.Model):
   __tablename__='roles'
   id = db.Column(db.Integer,primary_key=True)
   name = db.Column(db.String(64),unique=True)
   users = db.relationship('User', backref='role')
   def __repr__(self):
      return '<Role %r>' % self.name

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username

class NameForm(FlaskForm):
   name = StringField('What is your name?',validators=[DataRequired()])
   submit = SubmitField('Submit')

bootstrap = Bootstrap(app)
moment = Moment(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(505)
def internal_server_error(e):
    return render_template('500.html'), 500  


@app.route('/', methods=['GET', 'POST'])
def index():
#   name = None
   form = NameForm()
   if form.validate_on_submit():
#      name = form.name.data
#      old_name = session.get('name')
      user = User.query.filter_by(username=form.name.data).first()
      if user is None:
         user = User(username=form.name.data)
         db.session.add(user)
         db.session.commit()
         session['known'] = False
         #if app.config['FLASKY_ADMIN']:
         #   send_email(app.config['FLASKY_ADMIN'],'Newuser', 'mail/new_user', user=user)
         #else:
         session['known'] = True
#      if old_name is not None and old_name != form.name.data:
#         flash('Looks like you have changed your name!')
      session['name'] = form.name.data
      return redirect(url_for('index'))
#      form.name.data = ''
#   return render_template('index.html', form=form,name=session.get('name'),current_time=datetime.utcnow())
   return render_template('index.html', form=form,name=session.get('name'),known=session.get('known', False),current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
   return render_template('user.html', name=name)


@app.shell_context_processor
def make_shell_context():
   return dict(db=db, User=User, Role=Role)


def send_email(template, **kwargs):
   msg = Message(sender=app.config['MAIL_SENDER'])
   msg.body = render_template(template+'.txt', **kwargs)
   msg.html = render_template(template+'.html', **kwargs)
   msg.subject = 'Testing from Flask Email Program'
   msg.recipients = ["gandalfwong@gmail.com"]
   mail.send(msg)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
    