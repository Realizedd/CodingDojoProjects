from system.core.model import Model
import datetime

class Registration(Model):
    def __init__(self):
        super(Registration, self).__init__()

    def get_users(self, id):
        query = 'SELECT * FROM users WHERE id!=:id'
        values = {
            'id': id
        }

        return self.db.query_db(query, values)

    def get_user(self, id):
        query = 'SELECT * FROM users WHERE id=:id'
        values = {
            'id': id
        }

        return self.db.get_one(query, values)

    # NOTE TO SELF: Requests are already validated from Controller
    def find_user(self, request):
        query = 'SELECT * FROM users WHERE email=:email'
        values = {
            'email': request.form['email']
        }

        user = self.db.get_one(query, values)

        # Result is empty, no user found.
        if not user:
            return False

        if not self.bcrypt.check_password_hash(user['pw_hash'], request.form['pw']):
            return False

        # Return id to store in session
        return user['id']

    def add_user(self, request):
        query = 'INSERT INTO users (name, alias, email, pw_hash, date_of_birth, created_at) VALUES (:name, :alias, :email, :pw_hash, :date_of_birth, NOW())'
        values = {
            'name': request.form['name'],
            'alias': request.form['alias'],
            'email': request.form['email'],
            'date_of_birth': datetime.datetime(int(request.form['year']), int(request.form['month']), int(request.form['day']), 0, 0),
            'pw_hash': self.bcrypt.generate_password_hash(request.form['pw'])
        }

        return self.db.query_db(query, values)

