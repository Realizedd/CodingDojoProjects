from system.core.model import Model

class Author(Model):
    def __init__(self):
        super(Author, self).__init__()

    def get_authors(self):
        query = 'SELECT * FROM authors'
        return self.db.query_db(query)

    def add_author(self, name):
        query = 'INSERT INTO authors (name) VALUES (:name)'
        values = {
            'name': name
        }

        return self.db.query_db(query, values)