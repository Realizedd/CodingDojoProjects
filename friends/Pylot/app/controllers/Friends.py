from system.core.controller import *

class Friends(Controller):
    def __init__(self, action):
        super(Friends, self).__init__(action)
        self.load_model('Friend')
        self.load_model('Registration')

    def show(self):
        if 'id' not in session:
            return redirect('/main')

        current_user = self.models['Registration'].get_user(session['id'])
        friends = self.models['Friend'].get_friends(session['id'])
        users = self.models['Registration'].get_users(session['id'])

        for user in users[:]:
            for friend in friends:
                if friend['owner_id'] == user['id'] or friend['friend_id'] == user['id']:
                    users.remove(user)
                    break

        return self.load_view('/friends/index.html', user=current_user, users=users, friends=friends)

    def profile(self, id):
        user = self.models['Registration'].get_user(id)
        return self.load_view('/friends/profile.html', user=user)

    def remove_friend(self):
        if 'id' not in request.form:
            return redirect('/friends')

        self.models['Friend'].remove_friend(session['id'], request)
        return redirect('/friends')

    def add_friend(self):
        if 'id' not in request.form:
            return redirect('/friends')

        self.models['Friend'].add_friend(session['id'], request)
        return redirect('/friends')

