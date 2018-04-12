from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('Registration')
        self.load_model('Review')

    def show(self, id):
    	user = self.models['Registration'].get_user_by_id(id)
    	reviews = self.models['Review'].get_reviews_by_id(id)
        return self.load_view('users/show.html', user=user, reviews=reviews)

