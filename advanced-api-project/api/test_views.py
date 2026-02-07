from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from api.models import Author, Book

# tests for my book api
# i dont really know what im doing but found examples online
class BookAPITests(APITestCase):

    def setUp(self):
        # this runs before each test i think
        self.client = APIClient()  # for making api requests
        self.user = User.objects.create_user(username='testuser', password='testpass')  # test user
        self.author = Author.objects.create(name='Test Author')  # test author
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author
        )  # test book

    def test_get_books_list(self):
        # test getting all books
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, 200)  # should be ok
        self.assertEqual(len(response.data), 1)  # should have 1 book

    def test_get_single_book(self):
        # test getting one book
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Test Book')  # check title

    def test_create_book_without_auth(self):
        # try to create book without login - should fail
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, 403)  # should be forbidden not unauthorized

    def test_create_book_with_auth(self):
        # create book with login - should work
        self.client.force_authenticate(user=self.user)  # login
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, 201)  # should be created
        self.assertEqual(Book.objects.count(), 2)  # now have 2 books

    def test_create_book_with_login(self):
        # another way to login - found this online
        login_success = self.client.login(username='testuser', password='testpass')
        self.assertTrue(login_success)  # make sure login worked
        data = {
            'title': 'Login Test Book',
            'publication_year': 2022,
            'author': self.author.id
        }
        response = self.client.post('/api/books/create/', data)
        # not sure if this will work but lets try

    def test_update_book_without_auth(self):
        # try to update without login
        data = {'title': 'Updated Book'}
        response = self.client.put(f'/api/books/update/', data)
        self.assertEqual(response.status_code, 403)  # forbidden not unauthorized

    def test_update_book_with_auth(self):
        # update with login - but this wont work without pk in url
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Updated Book',
            'publication_year': 2021,
            'author': self.author.id
        }
        response = self.client.put(f'/api/books/update/', data)
        # this will probably fail because urls need pk but lets see

    def test_delete_book_without_auth(self):
        # try to delete without login
        response = self.client.delete(f'/api/books/delete/')
        self.assertEqual(response.status_code, 403)  # forbidden

    def test_delete_book_with_auth(self):
        # delete with login - also wont work without pk
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/books/delete/')
        # this will fail too because no pk in url

    def test_search_books(self):
        # test searching
        response = self.client.get('/api/books/?search=Test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # should find 1 book

    def test_filter_books_by_year(self):
        # test filtering by year
        response = self.client.get('/api/books/?publication_year=2020')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_ordering_books(self):
        # create another book for ordering test
        Book.objects.create(title='Another Book', publication_year=2019, author=self.author)
        response = self.client.get('/api/books/?ordering=publication_year')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['publication_year'], 2019)  # first should be 2019

    def test_invalid_publication_year(self):
        # test validation - future year should fail
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Future Book',
            'publication_year': 2030,  # future year
            'author': self.author.id
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, 400)  # should be bad request

# some tests fail because my urls are weird
# update and delete need pk parameter but my urls dont have them
# learned that 403 is forbidden, 401 is unauthorized
# APIClient is useful for testing api endpoints
# setUp runs before each test to create test data