"""Praxisprojekt: Book Reviewer - Lutz Celina"""

import unittest
import json
from main import app, generate_testdata


class TestBookReviewAPI(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        generate_testdata()

    def login(self, username, password):
        return self.client.post(
            '/login', json={'username': username, 'password': password}
        )

    def test_login(self):
        # Logge den Benutzer ein und speichere die Antwort in response
        response = self.login('user1', 'pass')
        # Prüfe ob Statuscode gleich 200 ist
        assert response.status_code == 200
        # Prüfe ob in der Response success True ist
        if json.loads(response.data)['success']:
            assert True

    def test_get_all_books(self):
        # Logge den Benutzer mit den Daten {username: 'user1', password: 'pass'}
        self.login('user1', 'pass')
        # Hole alle Bücher und speichere die Antwort in response
        response = self.client.get('/books')
        # Prüfe ob der Statuscode gleich 200 ist
        assert response.status_code == 200
        # Prüfe ob der Typ der Daten in response list ist
        assert type(json.loads(response.data)) is list

    def test_admin_add_book(self):
        # Logge den Benutzer mit den Daten {username: 'user1', password: 'pass'}
        self.login('user1', 'pass')
        # Füge ein neues Buch hinzu und speichere die Antwort in response
        response = self.client.post(
            '/books',
            json={'title': 'Test Book', 'author': 'Test Author', 'release_date': '11.11.2020', 'average_rating': 1,
                  'price': 10.00}
        )
        # Prüfe ob der Statuscode gleich 201 ist
        assert response.status_code == 201
        # Prüfe ob in der response message gleich 'Book added' ist
        assert json.loads(response.data)['message'] == 'Book added'

    def test_user_add_book(self):
        # Logge den Benutzer mit den Daten {username: 'user1', password: 'pass'}
        self.login('user2', 'pass')
        # Füge ein neues Buch hinzu und speichere die Antwort in response
        response = self.client.post(
            '/books',
            json={'title': 'Test Book', 'author': 'Test Author', 'release_date': '11.11.2020', 'average_rating': 1,
                  'price': 10.00}
        )
        # Prüfe ob der Statuscode gleich 403 ist
        assert response.status_code == 403
        # Prüfe ob in der response message gleich 'User does not have corresponding access' ist
        assert json.loads(response.data)['message'] == 'User does not have corresponding access'

    def test_admin_update_book(self):
        # Logge den Benutzer mit den Daten {username: 'user1', password: 'pass'}
        self.login('user1', 'pass')
        # Hole alle Bücher und speicher die Antwort in response
        response = self.client.get('/books')
        # Prüfe ob der Statuscode gleich 200 ist
        assert response.status_code == 200
        # Speichere die Daten aus response in books
        books = json.loads(response.data)
        # Überprüfe, ob die Book-Liste nicht leer ist
        assert len(books) > 0
        # Speichere das erste Buch aus der Liste books in first_book_id
        first_book_id = books[0]['book_id']
        # Aktualisiere das erste Buch der books-Liste mit neuen Daten und speichere die Antwort in response
        response = self.client.put(
            f'/books/{first_book_id}',
            json={'title': 'Updated Test Book', 'author': 'Updated Test Author', 'release_date': '22.11.2020',
                  'average_rating': 5, 'price': 10.00},
        )
        # Prüfe ob der Statuscode gleich 200 ist
        assert response.status_code == 200
        # Überprüfe ob die message aus response gleich 'Book updated' ist
        assert json.loads(response.data)['message'] == 'Book updated'

    def test_user_update_book(self):
        # Logge den Benutzer mit den Daten {username: 'user1', password: 'pass'}
        self.login('user2', 'pass')
        # Hole alle Bücher und speicher die Antwort in response
        response = self.client.get('/books')
        # Prüfe ob der Statuscode gleich 200 ist
        assert response.status_code == 200
        # Speichere die Daten aus response in books
        books = json.loads(response.data)
        # Überprüfe, ob die Book-Liste nicht leer ist
        assert len(books) > 0
        # Speichere das erste Buch aus der Liste books in first_book_id
        first_book_id = books[0]['book_id']
        # Aktualisiere das erste Buch der books-Liste mit neuen Daten und speichere die Antwort in response
        response = self.client.put(
            f'/books/{first_book_id}',
            json={'title': 'Updated Test Book', 'author': 'Updated Test Author', 'release_date': '22.11.2020',
                  'average_rating': 5, 'price': 10.00},
        )
        # Prüfe ob der Statuscode gleich 403 ist
        assert response.status_code == 403
        # Überprüfe ob die message aus response gleich 'User does not have corresponding access' ist
        assert json.loads(response.data)['message'] == 'User does not have corresponding access'

    def test_admin_delete_book(self):
        # Logge den Benutzer mit den Daten {username: 'user1', password: 'pass'}
        self.login('user1', 'pass')
        # Hole alle Bücher und speichere die Antwort in response
        response = self.client.get('/books')
        # Überprüfe, ob der Statuscode gleich 200 ist
        assert response.status_code == 200
        # Speichere die Daten aus Response in books
        books = json.loads(response.data)
        # Überprüfe, ob die books-Liste nicht leer ist
        assert len(books) > 0
        # Hole die ID des ersten Elements in der Liste books
        first_book_id = books[0]['book_id']
        # Lösche das erste books-Element und speichere die Antwort in response
        response = self.client.delete(f'/books/{first_book_id}')
        # Überprüfe, ob der Statuscode gleich 200 ist
        assert response.status_code == 200
        # Überprüfe, ob message aus response gleich 'Book deleted' ist
        assert json.loads(response.data)['message'] == 'Book deleted'

    def test_user_delete_book(self):
        # Logge den Benutzer mit den Daten {username: 'user1', password: 'pass'}
        self.login('user2', 'pass')
        # Hole alle Bücher und speichere die Antwort in response
        response = self.client.get('/books')
        # Überprüfe, ob der Statuscode gleich 200 ist
        assert response.status_code == 200
        # Speichere die Daten aus Response in books
        books = json.loads(response.data)
        # Überprüfe, ob die books-Liste nicht leer ist
        assert len(books) > 0
        # Hole die ID des ersten Elements in der Liste books
        first_book_id = books[0]['book_id']
        # Lösche das erste books-Element und speichere die Antwort in response
        response = self.client.delete(f'/books/{first_book_id}')
        # Überprüfe, ob der Statuscode gleich 403 ist
        assert response.status_code == 403
        # Überprüfe, ob message aus response gleich 'User does not have corresponding access' ist
        assert json.loads(response.data)['message'] == 'User does not have corresponding access'

    def test_get_all_reviews(self):
        # Logge den Benutzer mit den Daten {username: 'user1', password: 'pass'}
        self.login('user1', 'pass')
        # Speichere die Antwort in response
        response = self.client.get('/books/1/reviews')
        # Überprüfe, ob Statuscode 200 ist
        assert response.status_code == 200
        # Überprüfe, ob response typ:list ist
        assert type(json.loads(response.data)) is list

    def test_add_review(self):
        # Logge den Benutzer mit den Daten {username: 'user1', password: 'pass'}
        self.login('user1', 'pass')
        # Füge ein neues Buch hinzu
        self.client.post(
            '/books',
            json={'title': 'Test Book', 'author': 'Test Author', 'release_date': '11.11.2020', 'average_rating': 0,
                  'price': 10.00}
        )
        # Hole alle Bücher und speichere sie in books_response
        books_response = self.client.get('/books')
        # Speichere die Daten aus books_response in books
        books = json.loads(books_response.data)
        # Speichere die ID des Buches in book_id
        book_id = books[0]['book_id']
        # Füge eine neue Rezension hinzu und speichere die Antwort in response
        response = self.client.post(
            f'/books/{book_id}/reviews',
            json={'rating': 5, 'comment': 'Test Comment', 'review_date': '11.11.2020', 'price': 10.00}
        )
        # Prüfe ob der Statuscode gleich 201 ist
        assert response.status_code == 201
        # Prüfe ob in response message gleich 'Review added' ist
        assert json.loads(response.data)['message'] == 'Review added'
        # Prüfe, ob average_rating aktualisiert wurde

        # Hole das Buch
        book = self.client.get(f'/books/{book_id}')
        # Überprüfe das average_rating
        book = json.loads(book.data)
        average_rating = book['average_rating']

    def test_update_review(self):
        # Logge den Benutzer mit den Daten {username: 'user1', password: 'pass'}
        self.login('user1', 'pass')
        # Füge ein neues Buch hinzu
        self.client.post(
            '/books',
            json={'title': 'Test Book', 'author': 'Test Author', 'release_date': '11.11.2020', 'average_rating': 1, 'price': 10.00}
        )
        # Hole alle Bücher und speichere sie in books_response
        books_response = self.client.get('/books')
        # Speichere die Daten aus books_response in books
        books = json.loads(books_response.data)
        # Speichere die ID des Buches in book_id
        book_id = books[0]['book_id']
        # Hole alle Reviews vom ersten Buch aus der Liste books und speichere die Antwort in response
        response = self.client.get(f'/books/{book_id}/reviews')
        # Prüfe ob der Statuscode gleich 200 ist
        assert response.status_code == 200
        # Speichere die Daten aus response in books
        reviews = json.loads(response.data)
        # Überprüfe, ob die reviews-Liste nicht leer ist
        assert len(reviews) > 0
        # Speichere die erste Rezension aus der Liste books in first_book_id
        first_review_id = reviews[0]['review_id']
        # Aktualisiere die erste Rezension der reviews-Liste mit neuen Daten und speichere die Antwort in response
        response = self.client.put(
            f'/books/{book_id}/reviews/{first_review_id}',
            json={'rating': 5, 'comment': 'Updated Test Comment', 'review_date': '22.11.2020', 'price': 10.00}
        )
        # Prüfe ob der Statuscode gleich 200 ist
        assert response.status_code == 200
        # Überprüfe ob die message aus response gleich 'Review updated' ist
        assert json.loads(response.data)['message'] == 'Review updated'

    def test_delete_review(self):
        # Logge den Benutzer mit den Daten {username: 'user1', password: 'pass'}
        self.login('user1', 'pass')
        # Hole alle Bücher und speichere sie in books_response
        books_response = self.client.get('/books')
        # Speichere die Daten aus books_response in books
        books = json.loads(books_response.data)
        # Speichere die ID des Buches in book_id
        book_id = books[0]['book_id']
        # Hole alle Reviews und speichere die Antwort in response
        response = self.client.get(f'/books/{book_id}/reviews')
        # Überprüfe, ob der Statuscode gleich 200 ist
        assert response.status_code == 200
        # Speichere die Daten aus Response in reviews
        reviews = json.loads(response.data)
        # Überprüfe, ob die reviews-Liste nicht leer ist
        assert len(reviews) > 0
        # Hole die ID des ersten Elements in der Liste reviews
        first_review_id = reviews[0]['review_id']
        # Lösche das erste reviews-Element und speichere die Antwort in response
        response = self.client.delete(f'/books/{book_id}/reviews/{first_review_id}')
        # Überprüfe, ob der Statuscode gleich 200 ist
        assert response.status_code == 200
        # Überprüfe, ob message aus response gleich 'Review deleted' ist
        assert json.loads(response.data)['message'] == 'Review deleted'

    def test_book_discount(self):
        self.login('user1', 'pass')
        books_response = self.client.get('/books')
        books = json.loads(books_response.data)
        book = books[0]
        book_id = book['book_id']
        expected_price = lambda price, discount: price * discount
        original_price = book['price']
        discount = 0.8
        response = self.client.put(
            f'/books/{book_id}/discount',
            json={'discount': 20},
        )
        updated_book_response = self.client.get(f'/books/{book_id}')
        updated_book = json.loads(updated_book_response.data)
        assert response.status_code == 200
        assert json.loads(response.data)['message'] == 'Book updated'
        assert updated_book['price'] == expected_price(original_price,discount)


