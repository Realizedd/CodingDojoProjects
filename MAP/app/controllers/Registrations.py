from system.core.controller import *
import re
import json
import os

KEY = os.environ['ACCESS_SECRET']
TOKEN = os.environ['ACCESS_TOKEN']
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class Registrations(Controller):
    def __init__(self, action):
        super(Registrations, self).__init__(action)
        self.load_model('Registration')

    def index(self):
        if 'id' in session:
            return redirect('/books')

        return self.load_view('index.html')

    def login(self):
        # 'not in request.form' handles the case of html modification (?)
        if 'email' not in request.form or len(request.form['email']) == 0:
            flash('Please type a valid email.', 'login_email')
            return redirect('/')

        if 'pw' not in request.form or len(request.form['pw']) == 0:
            flash('Please type a valid password.', 'login_pw')
            return redirect('/')

        result = self.models['Registration'].get_user(request)

        if not result:
            flash('Login failed! Are you sure your credenticals are correct?', 'global')
            return redirect('/')

        session['id'] = result
        return redirect('/books')

    def register(self):
        if 'name' not in request.form or len(request.form['name']) == 0:
            flash('Please type a valid name.', 'name')
            return redirect('/')

        name = request.form['name']

        if not name.replace(" ", "").isalpha():
            flash('Name must be alphabetic.', 'name')
            return redirect('/')

        if len(name) < 2:
            flash('Name must be longer than 1 character.', 'name')
            return redirect('/')

        if 'alias' not in request.form or len(request.form['alias']) == 0:
            flash('Please type a valid alias', 'alias')
            return redirect('/')

        alias = request.form['alias']

        if not alias.isalpha():
            flash('Alias must be alphabetic.', 'alias')
            return redirect('/')

        if len(alias) < 2:
            flash('Alias must be longer than 1 character.', 'alias')
            return redirect('/')

        if 'email' not in request.form:
            flash('Please type a valid email.', 'register_email')
            return redirect('/')

        email = request.form['email']

        if not EMAIL_REGEX.match(email):
            flash('Please type a valid email.', 'register_email')
            return redirect('/')

        if 'pw' not in request.form:
            flash('Please type a valid password.', 'register_pw')
            return redirect('/')

        password = request.form['pw']

        if len(password) < 8:
            flash('Passwords must be longer than 8 characters.', 'register_pw')
            return redirect('/')

        if 'pw_conf' not in request.form:
            flash('Please type a valid password.', 'register_pw_conf')
            return redirect('/')

        password_confirm = request.form['pw_conf']

        if not password == password_confirm:
            flash('Password and Password Confirmation must match.', 'register_pw_conf')
            return redirect('/')

        result = self.models['Registration'].add_user(request)
        session['id'] = result
        return redirect('/books')

    def logout(self):
        session.clear()
        return redirect('/')

    def books(self):
        if 'id' not in session:
            return redirect('/login')

        return self.load_view('books.html')

    def testroute(self):
        print request.form['accessToken']
        url = 'https://graph.facebook.com/debug_token?input_token=' + request.form['accessToken'] + '&access_token=' + TOKEN
        response = json.loads(requests.get(url).content)
        print response['data']['is_valid']
        return redirect('/')
