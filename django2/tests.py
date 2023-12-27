# tests.py
from django.test import TestCase
from django.urls import reverse
from playground.models import Book
from playground.views import BookViewSet


class BookModelTestCase(TestCase):
    def test_create_book(self):
        # Create a Book instance and save it to the database
        Book.objects.create(title='Test Book', author='Test Author', published_date='2022-01-01')

        # Retrieve the book from the database
        book = Book.objects.get(title='Test Book')

        # Verify that the retrieved book matches the expected values
        self.assertEqual(book.author, 'Test Author')





class BookViewTestCase(TestCase):
    def test_book_list_view(self):
        # Create some test books
        Book.objects.create(title='Book 1', author='Author 1', published_date='2022-01-01')
        Book.objects.create(title='Book 2', author='Author 2', published_date='2023-01-01')

        # Access the BookListView using reverse to get the URL
        response = self.client.get(reverse('book-list'))

        # Verify that the view returns a status code of 200
        self.assertEqual(response.status_code, 200)

        # Verify that the rendered context contains the expected books
