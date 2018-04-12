from system.core.model import Model

class Search(Model):
    def __init__(self):
        super(Search, self).__init__()

    # Appended by_id due to method naming conflicts
    def get_favourites_by_user_id(self, session):
        print 'Session is - ', session,'\n'
        data_all_fav = {
            'id': session['id']
        }
        query_all_fav = 'SELECT * FROM favorites WHERE user_id = :id'

        return self.db.query_db(query_all_fav, data_all_fav)

    def add_favourite(self, form):
        print "Search_add_favourite",'\n'
        query_new_fav = 'INSERT INTO favorites (name, description, url, created_at, user_id) VALUES (:name, :description, :url, NOW(), :id);'
        print "Form data is ", form, '\n'

        new_fav_data = {
            'fav_name': form['fav_name'],
            'fav_description': form['fav_description'],
            'current_url_search': form['current_url_search']
        }

        return self.db.query_db(query_new_fav, new_fav_data)

    def get_fav_by_user(self, user_id, fav_id):
        print 'Search_get_fav_by_user'
        data_fav_by_user = {
            'user_id': user_id,
            'fav_id': fav_id
        }
        query_fav_by_user = 'SELECT url FROM favorites WHERE user_id=:user_id AND id=:fav_id'
        search_url = self.db.query_db(query_fav_by_user, data_fav_by_user)
        print 'Search URL is ', search_url,'\n'
        return search_url[0]['search_url']