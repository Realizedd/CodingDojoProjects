from system.core.controller import *

class Books(Controller):
    def __init__(self, action):
        super(Books, self).__init__(action)
        self.load_model('Review')
        self.load_model('Book')
        self.load_model('Registration')
        self.load_model('Author')

    def index(self):
    	# if 'id' not in session:
    	# 	return redirect('/')

    	user = self.models['Registration'].get_user_by_id(session['id'])
    	recent_reviews = self.models['Review'].get_recent_reviews()
    	books_with_reviews = self.models['Book'].get_books_with_reviews()
        return self.load_view('books/index.html', user=user, recent_reviews=recent_reviews, books_with_reviews=books_with_reviews)

    def show(self, id):
        if 'id' not in session:
            return redirect('/')

        book = self.models['Book'].get_book(id)
        reviews = self.models['Review'].get_reviews(id)
        return self.load_view('books/show.html', book=book, reviews=reviews)

    def post_review(self):
        if not 'id' in request.form or not 'message' in request.form or not 'rating' in request.form:
            return redirect('/') 

        self.models['Review'].add_review(session['id'], request)
        return redirect('/books/' + request.form['id'])

    def add_book(self):
        if 'id' not in session:
            return redirect('/')

        authors = self.models['Author'].get_authors()
        return self.load_view('/books/add.html', authors=authors)

    def submit_book(self):
        if not 'title' in request.form or not 'selected_author' in request.form or not 'author' in request.form or not 'message' in request.form or not 'rating' in request.form:
            return redirect('/')

        author = request.form['author']

        if len(author) == 0:
            author = request.form['selected_author']

        author_id = self.models['Author'].add_author(author)
        book_id = self.models['Book'].add_book(author_id, request)

        values = {
            'message': request.form['message'],
            'book_id': book_id,
            'rating': request.form['rating'],
            'user_id': session['id']
        }

        self.models['Review'].add_review_by_values(values)
        return redirect('/books')