"""
Mock database for the bookstore API comparison
This simulates a real database with in-memory data
"""

from datetime import datetime
from typing import List, Optional
from .models import Author, Book, Customer, Order


class MockDatabase:
    def __init__(self):
        self._init_data()

    def _init_data(self):
        """Initialize mock data"""

        # Authors
        self.authors = [
            Author(
                1,
                "J.K. Rowling",
                "British author best known for Harry Potter series",
                1965,
            ),
            Author(2, "George Orwell", "English novelist and journalist", 1903),
            Author(3, "Jane Austen", "English novelist of romantic fiction", 1775),
            Author(
                4,
                "Stephen King",
                "American author of horror and supernatural fiction",
                1947,
            ),
            Author(
                5, "Agatha Christie", "English writer known for detective novels", 1890
            ),
        ]

        # Books
        self.books = [
            Book(
                1,
                "Harry Potter and the Philosopher's Stone",
                1,
                29.99,
                "Fantasy",
                1997,
                "978-0439708180",
            ),
            Book(
                2,
                "Harry Potter and the Chamber of Secrets",
                1,
                32.99,
                "Fantasy",
                1998,
                "978-0439064873",
            ),
            Book(3, "1984", 2, 19.99, "Dystopian Fiction", 1949, "978-0451524935"),
            Book(
                4,
                "Animal Farm",
                2,
                15.99,
                "Allegorical Fiction",
                1945,
                "978-0451526342",
            ),
            Book(5, "Pride and Prejudice", 3, 22.99, "Romance", 1813, "978-0141439518"),
            Book(6, "The Shining", 4, 24.99, "Horror", 1977, "978-0307743657"),
            Book(7, "It", 4, 27.99, "Horror", 1986, "978-1501142970"),
            Book(
                8,
                "Murder on the Orient Express",
                5,
                18.99,
                "Mystery",
                1934,
                "978-0062693662",
            ),
            Book(
                9,
                "And Then There Were None",
                5,
                16.99,
                "Mystery",
                1939,
                "978-0062073488",
            ),
        ]

        # Customers
        self.customers = [
            Customer(1, "Alice Johnson", "alice@example.com", datetime(2023, 1, 15)),
            Customer(2, "Bob Smith", "bob@example.com", datetime(2023, 3, 22)),
            Customer(3, "Carol Davis", "carol@example.com", datetime(2023, 5, 10)),
            Customer(4, "David Wilson", "david@example.com", datetime(2023, 7, 8)),
        ]

        # Orders
        self.orders = [
            Order(1, 1, [1, 2], 62.98, datetime(2023, 6, 1)),
            Order(2, 1, [3], 19.99, datetime(2023, 6, 15)),
            Order(3, 2, [5, 8], 41.98, datetime(2023, 7, 3)),
            Order(4, 3, [6, 7], 52.98, datetime(2023, 8, 12)),
            Order(5, 4, [4, 9], 32.98, datetime(2023, 8, 20)),
        ]

    # Author methods
    def get_all_authors(self) -> List[Author]:
        return self.authors

    def get_author_by_id(self, author_id: int) -> Optional[Author]:
        return next((author for author in self.authors if author.id == author_id), None)

    # Book methods
    def get_all_books(self) -> List[Book]:
        return self.books

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        return next((book for book in self.books if book.id == book_id), None)

    def get_books_by_author(self, author_id: int) -> List[Book]:
        return [book for book in self.books if book.author_id == author_id]

    def get_books_by_genre(self, genre: str) -> List[Book]:
        return [book for book in self.books if book.genre.lower() == genre.lower()]

    # Customer methods
    def get_all_customers(self) -> List[Customer]:
        return self.customers

    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        return next(
            (customer for customer in self.customers if customer.id == customer_id),
            None,
        )

    # Order methods
    def get_all_orders(self) -> List[Order]:
        return self.orders

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        return next((order for order in self.orders if order.id == order_id), None)

    def get_orders_by_customer(self, customer_id: int) -> List[Order]:
        return [order for order in self.orders if order.customer_id == customer_id]

    # Helper methods for related data
    def get_author_for_book(self, book: Book) -> Optional[Author]:
        return self.get_author_by_id(book.author_id)

    def get_customer_for_order(self, order: Order) -> Optional[Customer]:
        return self.get_customer_by_id(order.customer_id)

    def get_books_for_order(self, order: Order) -> List[Book]:
        return [
            self.get_book_by_id(book_id)
            for book_id in order.book_ids
            if self.get_book_by_id(book_id)
        ]

    # Create new records (for POST examples)
    def create_book(
        self,
        title: str,
        author_id: int,
        price: float,
        genre: str,
        published_year: int,
        isbn: str,
    ) -> Book:
        new_id = max(book.id for book in self.books) + 1
        new_book = Book(new_id, title, author_id, price, genre, published_year, isbn)
        self.books.append(new_book)
        return new_book

    def create_customer(self, name: str, email: str) -> Customer:
        new_id = max(customer.id for customer in self.customers) + 1
        new_customer = Customer(new_id, name, email, datetime.now())
        self.customers.append(new_customer)
        return new_customer

    def create_order(self, customer_id: int, book_ids: List[int]) -> Order:
        new_id = max(order.id for order in self.orders) + 1

        # Calculate total amount
        total = 0.0
        for book_id in book_ids:
            book = self.get_book_by_id(book_id)
            if book:
                total += book.price

        new_order = Order(new_id, customer_id, book_ids, total, datetime.now())
        self.orders.append(new_order)
        return new_order


# Global database instance
db = MockDatabase()
