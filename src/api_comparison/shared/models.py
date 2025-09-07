"""
Shared data models for both REST and GraphQL APIs
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Author:
    id: int
    name: str
    bio: str
    birth_year: int

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "bio": self.bio,
            "birth_year": self.birth_year,
        }


@dataclass
class Book:
    id: int
    title: str
    author_id: int
    price: float
    genre: str
    published_year: int
    isbn: str

    def to_dict(self, include_author=False, author=None):
        result = {
            "id": self.id,
            "title": self.title,
            "author_id": self.author_id,
            "price": self.price,
            "genre": self.genre,
            "published_year": self.published_year,
            "isbn": self.isbn,
        }
        if include_author and author:
            result["author"] = author.to_dict()
        return result


@dataclass
class Customer:
    id: int
    name: str
    email: str
    registration_date: datetime

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "registration_date": self.registration_date.isoformat(),
        }


@dataclass
class Order:
    id: int
    customer_id: int
    book_ids: List[int]
    total_amount: float
    order_date: datetime

    def to_dict(
        self, include_customer=False, include_books=False, customer=None, books=None
    ):
        result = {
            "id": self.id,
            "customer_id": self.customer_id,
            "book_ids": self.book_ids,
            "total_amount": self.total_amount,
            "order_date": self.order_date.isoformat(),
        }

        if include_customer and customer:
            result["customer"] = customer.to_dict()

        if include_books and books:
            result["books"] = [book.to_dict() for book in books]

        return result
