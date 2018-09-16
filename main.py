from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from random import randint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tableusersdef import *
from tablehistorydef import *


app = Flask(__name__)
app.secret_key = 'veryverysecretkey1'


@app.route('/')
def index():
	# index
	# -------------------------------------

	if not session.get('logged_in'):
		return redirect(url_for('login'))
	else:
		return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
	# shows login form and handles login and registration
	# --------------------------------------

	if request.method == 'POST':
		USERNAME = str(request.form['username'])

		# search for username in database
		Session = sessionmaker(bind=users_engine)
		s = Session()
		query = s.query(User).filter(User.username.in_([USERNAME]))
		result = query.first()
		if result:
			# successful login
			session['logged_in'] = True
			session['username'] = USERNAME

			return redirect(url_for('index'))
		else:
			# register new user
			user = User(USERNAME)
			s.add(user)
			s.commit()

			session['logged_in'] = True
			session['username'] = USERNAME

			return redirect(url_for('index'))
			
	else:
		return render_template('login.html')




@app.route('/logout')
def logout():
	# ends session and deletes username
	# ------------------------------------

	session['logged_in'] = False
	session.pop('username', None)
	return redirect(url_for('index'))


@app.route('/random')
def random():
	# generates random number and adds to the history
	# -----------------------------------------------

	if not session.get('logged_in'):
		return redirect(url_for('login'))
	else:
		number = randint(1, 10**9)

		Session = sessionmaker(bind=history_engine)
		s = Session()

		username = session['username']
		entry = Entry(username, number)

		s.add(entry)
		s.commit()

		return render_template('random.html', number=number)

@app.route('/history')
def history():
	# pulls out history for current user
	# ---------------------------------------

	if not session.get('logged_in'):
		return redirect(url_for('login'))
	else:
		# search for all entries with given username
		Session = sessionmaker(bind=history_engine)
		s = Session()
		username = session['username']
		query = s.query(Entry).filter(Entry.username.in_([username]))
		# create list
		hist = [x.number for x in query.all()]
		# reverse so last numbers are on top
		hist.reverse()


		return render_template('history.html', hist=hist)
