from system.core.controller import *
import re
import json
import os

KEY = os.environ['ACCESS_SECRET']
TOKEN = os.environ['ACCESS_TOKEN']
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class Searches(Controller):
    def __init__(self, action):
        super(Searches, self).__init__(action)
        self.load_model('Search')

    def index(self):
        # if 'id' in session:
        #     return redirect('/')
        session['user_id'] = 2
        return self.load_view('search.html')

    def add_favourite(self):
        print 'Searches_add_favourite'
        print 'data received - ', request.form, '\n'
        new_fav_id=self.models['Search'].add_favourite(request.form)
        print 'New fav ID - ', new_fav_id
        # newfile = jsonify({'new_fav_id': new_fav_id})
        # return newfile
        return redirect('/search/get_favs_table_partial')

    def favs_partial_html(self):
        user_favs = self.models['Search'].get_favourites_by_user_id(session)
        print 'Searches_favs_partial_html - ', user_favs, '\n'
        return self.load_view('partials/favs_table_partial.html', user_favs=user_favs)
