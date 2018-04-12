from system.core.model import Model

class Book(Model):
    def __init__(self):
        super(Book, self).__init__()

    def add_book(self, author_id, request):
        query = 'INSERT INTO books (title, author_id, created_at) VALUES (:title, :author_id, NOW())'
        values = {
            'title': request.form['title'],
            'author_id': author_id
        }

        return self.db.query_db(query, values)
    
    def get_book(self, id):
        query = 'SELECT books.id, books.title, authors.name FROM books JOIN authors ON authors.id=books.author_id WHERE books.id=:id'
        values = {
            'id': id
        }
        return self.db.get_one(query, values)

    def get_books_with_reviews(self):
        query = 'SELECT COUNT(*), book_id, books.title FROM reviews LEFT JOIN books ON books.id = reviews.book_id GROUP BY books.title HAVING COUNT(*) > 0 ORDER BY COUNT(*) DESC'
        return self.db.query_db(query)