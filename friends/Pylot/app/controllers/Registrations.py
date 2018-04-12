from system.core.controller import *
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class Registrations(Controller):
    def __init__(self, action):
        super(Registrations, self).__init__(action)
        self.load_model('Registration')

    def index(self):
        return redirect('/main')

    def main(self):
        return self.load_view('index.html')

    def login(self):
        # 'not in request.form' handles the case of html modification (?)
        if 'email' not in request.form or len(request.form['email']) == 0:
            flash('Please type a valid email.', 'login_email')
            return redirect('/main')

        if 'pw' not in request.form or len(request.form['pw']) == 0:
            flash('Please type a valid password.', 'login_pw')
            return redirect('/main')

        result = self.models['Registration'].find_user(request)

        if not result:
            flash('Login failed! Are you sure your credenticals are correct?', 'global')
            return redirect('/main')

        session['id'] = result
        return redirect('/friends')

    def register(self):
        if 'name' not in request.form or len(request.form['name']) == 0:
            flash('Please type a valid name.', 'name')
            return redirect('/main')

        name = request.form['name']

        if not name.replace(" ", "").isalpha():
            flash('Name must be alphabetic.', 'name')
            return redirect('/main')

        if len(name) < 2:
            flash('Name must be longer than 1 character.', 'name')
            return redirect('/main')

        if 'alias' not in request.form or len(request.form['alias']) == 0:
            flash('Please type a valid alias', 'alias')
            return redirect('/main')

        alias = request.form['alias']

        if not alias.isalpha():
            flash('Alias must be alphabetic.', 'alias')
            return redirect('/main')

        if len(alias) < 2:
            flash('Alias must be longer than 1 character.', 'alias')
            return redirect('/main')

        if 'email' not in request.form:
            flash('Please type a valid email.', 'register_email')
            return redirect('/main')

        email = request.form['email']

        if not EMAIL_REGEX.match(email):
            flash('Please type a valid email.', 'register_email')
            return redirect('/main')

        if 'pw' not in request.form:
            flash('Please type a valid password.', 'register_pw')
            return redirect('/main')

        password = request.form['pw']

        if len(password) < 8:
            flash('Passwords must be longer than 8 characters.', 'register_pw')
            return redirect('/main')

        if 'pw_conf' not in request.form:
            flash('Please type a valid password.', 'register_pw_conf')
            return redirect('/main')

        password_confirm = request.form['pw_conf']

        if not password == password_confirm:
            flash('Password and Password Confirmation must match.', 'register_pw_conf')
            return redirect('/main')

        result = self.models['Registration'].add_user(request)

        if 'year' not in request.form or 'month' not in request.form or 'day' not in request.form:
            return redirect('/main')

        session['id'] = result
        return redirect('/friends')

    def logout(self):
        session.clear()
        return redirect('/main')

