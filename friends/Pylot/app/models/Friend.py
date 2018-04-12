from system.core.model import Model
import datetime

class Friend(Model):
    def __init__(self):
        super(Friend, self).__init__()

    def get_friends(self, id):
        query = 'SELECT users.id as friend_id, users.alias as friend, owners.id as owner_id, owners.alias as creator FROM friends LEFT JOIN users ON friends.user_id=users.id LEFT JOIN users as owners ON friends.owner_id=owners.id WHERE user_id=:id OR owner_id=:id'
        values = {
            'id': id
        }

        return self.db.query_db(query, values)

    def remove_friend(self, id, request):
        query = 'DELETE FROM friends WHERE (user_id=:id or owner_id=:id) and (user_id=:friend_id or owner_id=:friend_id)'
        values = {
            'id': id,
            'friend_id': request.form['id']
        }

        return self.db.query_db(query, values)

    def add_friend(self, id, request):
        query = 'INSERT INTO friends (created_at, user_id, owner_id) VALUES (NOW(), :id, :friend_id)'
        values = {
            'id': id,
            'friend_id': request.form['id']
        }

        return self.db.query_db(query, values)

