"""
GraphQL Schema for Bookstore API using Strawberry GraphQL
Demonstrates modern GraphQL patterns with type-safe resolvers
"""

import strawberry
from typing import List, Optional
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.database import database


@strawberry.type
class Author:
    id: int
    name: str
    email: str
    bio: Optional[str] = None
    created_at: datetime

    @strawberry.field
    def books(self) -> List["Book"]:
        """Get all books by this author"""
        return [Book(**book) for book in database.get_books_by_author(self.id)]


@strawberry.type
class Book:
    id: int
    title: str
    isbn: str
    price: float
    publication_date: datetime
    author_id: int
    genre: Optional[str] = None
    description: Optional[str] = None

    @strawberry.field
    def author(self) -> Optional[Author]:
        """Get the author of this book"""
        author_data = database.get_author(self.author_id)
        return Author(**author_data) if author_data else None


@strawberry.type
class Customer:
    id: int
    name: str
    email: str
    address: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime

    @strawberry.field
    def orders(self) -> List["Order"]:
        """Get all orders by this customer"""
        return [Order(**order) for order in database.get_orders_by_customer(self.id)]


@strawberry.type
class OrderItem:
    book_id: int
    quantity: int
    price: float

    @strawberry.field
    def book(self) -> Optional[Book]:
        """Get the book for this order item"""
        book_data = database.get_book(self.book_id)
        return Book(**book_data) if book_data else None


@strawberry.type
class Order:
    id: int
    customer_id: int
    order_date: datetime
    total_amount: float
    status: str
    items: List[OrderItem]

    @strawberry.field
    def customer(self) -> Optional[Customer]:
        """Get the customer for this order"""
        customer_data = database.get_customer(self.customer_id)
        return Customer(**customer_data) if customer_data else None


# Input types for mutations
@strawberry.input
class AuthorInput:
    name: str
    email: str
    bio: Optional[str] = None


@strawberry.input
class BookInput:
    title: str
    isbn: str
    price: float
    author_id: int
    genre: Optional[str] = None
    description: Optional[str] = None


@strawberry.input
class CustomerInput:
    name: str
    email: str
    address: Optional[str] = None
    phone: Optional[str] = None


@strawberry.input
class OrderItemInput:
    book_id: int
    quantity: int


@strawberry.input
class OrderInput:
    customer_id: int
    items: List[OrderItemInput]


# Query root
@strawberry.type
class Query:
    @strawberry.field
    def authors(self, limit: Optional[int] = None) -> List[Author]:
        """Get all authors with optional limit"""
        authors_data = database.get_all_authors()
        if limit:
            authors_data = authors_data[:limit]
        return [Author(**author) for author in authors_data]

    @strawberry.field
    def author(self, id: int) -> Optional[Author]:
        """Get a specific author by ID"""
        author_data = database.get_author(id)
        return Author(**author_data) if author_data else None

    @strawberry.field
    def books(
        self,
        limit: Optional[int] = None,
        author_id: Optional[int] = None,
        genre: Optional[str] = None,
    ) -> List[Book]:
        """Get books with optional filters"""
        if author_id:
            books_data = database.get_books_by_author(author_id)
        else:
            books_data = database.get_all_books()

        # Apply genre filter if specified
        if genre:
            books_data = [book for book in books_data if book.get("genre") == genre]

        # Apply limit if specified
        if limit:
            books_data = books_data[:limit]

        return [Book(**book) for book in books_data]

    @strawberry.field
    def book(self, id: int) -> Optional[Book]:
        """Get a specific book by ID"""
        book_data = database.get_book(id)
        return Book(**book_data) if book_data else None

    @strawberry.field
    def customers(self, limit: Optional[int] = None) -> List[Customer]:
        """Get all customers with optional limit"""
        customers_data = database.get_all_customers()
        if limit:
            customers_data = customers_data[:limit]
        return [Customer(**customer) for customer in customers_data]

    @strawberry.field
    def customer(self, id: int) -> Optional[Customer]:
        """Get a specific customer by ID"""
        customer_data = database.get_customer(id)
        return Customer(**customer_data) if customer_data else None

    @strawberry.field
    def orders(
        self,
        limit: Optional[int] = None,
        customer_id: Optional[int] = None,
        status: Optional[str] = None,
    ) -> List[Order]:
        """Get orders with optional filters"""
        if customer_id:
            orders_data = database.get_orders_by_customer(customer_id)
        else:
            orders_data = database.get_all_orders()

        # Apply status filter if specified
        if status:
            orders_data = [
                order for order in orders_data if order.get("status") == status
            ]

        # Apply limit if specified
        if limit:
            orders_data = orders_data[:limit]

        return [Order(**order) for order in orders_data]

    @strawberry.field
    def order(self, id: int) -> Optional[Order]:
        """Get a specific order by ID"""
        order_data = database.get_order(id)
        return Order(**order_data) if order_data else None

    @strawberry.field
    def search_books(self, query: str, limit: Optional[int] = 10) -> List[Book]:
        """Search books by title or description"""
        all_books = database.get_all_books()
        matching_books = []

        for book in all_books:
            if query.lower() in book["title"].lower() or (
                book.get("description") and query.lower() in book["description"].lower()
            ):
                matching_books.append(book)

        if limit:
            matching_books = matching_books[:limit]

        return [Book(**book) for book in matching_books]


# Mutation root
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_author(self, author_input: AuthorInput) -> Author:
        """Create a new author"""
        author_data = database.create_author(
            name=author_input.name, email=author_input.email, bio=author_input.bio
        )
        return Author(**author_data)

    @strawberry.mutation
    def update_author(self, id: int, author_input: AuthorInput) -> Optional[Author]:
        """Update an existing author"""
        author_data = database.update_author(
            id=id,
            name=author_input.name,
            email=author_input.email,
            bio=author_input.bio,
        )
        return Author(**author_data) if author_data else None

    @strawberry.mutation
    def delete_author(self, id: int) -> bool:
        """Delete an author"""
        return database.delete_author(id)

    @strawberry.mutation
    def create_book(self, book_input: BookInput) -> Book:
        """Create a new book"""
        book_data = database.create_book(
            title=book_input.title,
            isbn=book_input.isbn,
            price=book_input.price,
            author_id=book_input.author_id,
            genre=book_input.genre,
            description=book_input.description,
        )
        return Book(**book_data)

    @strawberry.mutation
    def update_book(self, id: int, book_input: BookInput) -> Optional[Book]:
        """Update an existing book"""
        book_data = database.update_book(
            id=id,
            title=book_input.title,
            isbn=book_input.isbn,
            price=book_input.price,
            author_id=book_input.author_id,
            genre=book_input.genre,
            description=book_input.description,
        )
        return Book(**book_data) if book_data else None

    @strawberry.mutation
    def delete_book(self, id: int) -> bool:
        """Delete a book"""
        return database.delete_book(id)

    @strawberry.mutation
    def create_customer(self, customer_input: CustomerInput) -> Customer:
        """Create a new customer"""
        customer_data = database.create_customer(
            name=customer_input.name,
            email=customer_input.email,
            address=customer_input.address,
            phone=customer_input.phone,
        )
        return Customer(**customer_data)

    @strawberry.mutation
    def update_customer(
        self, id: int, customer_input: CustomerInput
    ) -> Optional[Customer]:
        """Update an existing customer"""
        customer_data = database.update_customer(
            id=id,
            name=customer_input.name,
            email=customer_input.email,
            address=customer_input.address,
            phone=customer_input.phone,
        )
        return Customer(**customer_data) if customer_data else None

    @strawberry.mutation
    def delete_customer(self, id: int) -> bool:
        """Delete a customer"""
        return database.delete_customer(id)

    @strawberry.mutation
    def create_order(self, order_input: OrderInput) -> Order:
        """Create a new order"""
        # Convert OrderItemInput to dict format for database
        items = [
            {"book_id": item.book_id, "quantity": item.quantity}
            for item in order_input.items
        ]

        order_data = database.create_order(
            customer_id=order_input.customer_id, items=items
        )
        return Order(**order_data)

    @strawberry.mutation
    def update_order_status(self, id: int, status: str) -> Optional[Order]:
        """Update order status"""
        order_data = database.update_order_status(id, status)
        return Order(**order_data) if order_data else None

    @strawberry.mutation
    def cancel_order(self, id: int) -> bool:
        """Cancel an order"""
        return database.update_order_status(id, "cancelled") is not None


# Create the schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
