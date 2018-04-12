from system.core.model import Model

class Review(Model):
    def __init__(self):
        super(Review, self).__init__()

    def add_review(self, id, request):
        query = 'INSERT INTO reviews (rating, message, book_id, user_id, created_at) VALUES (:rating, :message, :book_id, :user_id, NOW())'
        values = {
            'book_id': request.form['id'],
            'user_id': id,
            'message': request.form['message'],
            'rating': int(request.form['rating'])
        }

        return self.db.query_db(query, values)

    def add_review_by_values(self, values):
        query = 'INSERT INTO reviews (rating, message, book_id, user_id, created_at) VALUES (:rating, :message, :book_id, :user_id, NOW())'
        values = {
            'book_id': values['book_id'],
            'user_id': values['user_id'],
            'message': values['message'],
            'rating': int(values['rating'])
        }

        return self.db.query_db(query, values)

    def get_reviews(self, id):
        query = 'SELECT reviews.rating, reviews.message, reviews.created_at, reviews.user_id, users.alias as reviewer FROM reviews LEFT JOIN users ON users.id = reviews.user_id WHERE book_id=:id ORDER BY created_at DESC'
        values = {
            'id': id
        }

        return self.db.query_db(query, values)

    def get_reviews_by_id(self, id):
        query = 'SELECT books.title, books.id FROM reviews JOIN books ON reviews.book_id = books.id WHERE reviews.user_id=:id'
        values = {
            'id': id
        }

        return self.db.query_db(query, values)

    def get_recent_reviews(self):
        query = 'SELECT reviews.book_id, reviews.rating, reviews.message, books.title, users.alias as reviewer, users.id, reviews.created_at FROM reviews JOIN books ON books.id = book_id JOIN users ON users.id = user_id ORDER BY reviews.created_at DESC LIMIT 3'
        return self.db.query_db(query)