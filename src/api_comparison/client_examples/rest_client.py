"""
REST API Client Examples
Demonstrates common patterns and problems with REST APIs
"""

import requests
import json
from typing import Dict, Any, List

BASE_URL = "http://localhost:8000"


class RESTBookstoreClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def get_author_with_books(self, author_id: int) -> Dict[str, Any]:
        """
        Get author details with all their books
        Demonstrates OVER-FETCHING and MULTIPLE REQUESTS problem
        """
        print(f"\n=== REST: Getting author {author_id} with books ===")

        # Request 1: Get author details
        print(f"Making request: GET {self.base_url}/authors/{author_id}")
        author_response = self.session.get(f"{self.base_url}/authors/{author_id}")
        author_data = author_response.json()

        # Request 2: Get all books by this author
        print(f"Making request: GET {self.base_url}/books?author_id={author_id}")
        books_response = self.session.get(
            f"{self.base_url}/books?author_id={author_id}"
        )
        books_data = books_response.json()

        # Combine the data
        result = {
            "author": author_data,
            "books": books_data,
            "total_requests": 2,
            "total_bytes": len(author_response.content) + len(books_response.content),
        }

        print(f"Total requests made: {result['total_requests']}")
        print(f"Total bytes received: {result['total_bytes']}")
        return result

    def get_customer_order_summary(self, customer_id: int) -> Dict[str, Any]:
        """
        Get customer with their recent orders and book details
        Demonstrates N+1 query problem and over-fetching
        """
        print(f"\n=== REST: Getting customer {customer_id} order summary ===")
        request_count = 0
        total_bytes = 0

        # Request 1: Get customer details
        print(f"Making request: GET {self.base_url}/customers/{customer_id}")
        customer_response = self.session.get(f"{self.base_url}/customers/{customer_id}")
        customer_data = customer_response.json()
        request_count += 1
        total_bytes += len(customer_response.content)

        # Request 2: Get customer's orders
        print(f"Making request: GET {self.base_url}/orders?customer_id={customer_id}")
        orders_response = self.session.get(
            f"{self.base_url}/orders?customer_id={customer_id}"
        )
        orders_data = orders_response.json()
        request_count += 1
        total_bytes += len(orders_response.content)

        # For each order, we need to get book details for each item (N+1 problem)
        enriched_orders = []
        for order in orders_data:
            enriched_order = order.copy()
            enriched_items = []

            for item in order["items"]:
                # Request N: Get book details for each item
                book_id = item["book_id"]
                print(f"Making request: GET {self.base_url}/books/{book_id}")
                book_response = self.session.get(f"{self.base_url}/books/{book_id}")
                book_data = book_response.json()
                request_count += 1
                total_bytes += len(book_response.content)

                enriched_item = item.copy()
                enriched_item["book"] = book_data
                enriched_items.append(enriched_item)

            enriched_order["items"] = enriched_items
            enriched_orders.append(enriched_order)

        result = {
            "customer": customer_data,
            "orders": enriched_orders,
            "total_requests": request_count,
            "total_bytes": total_bytes,
        }

        print(f"Total requests made: {result['total_requests']}")
        print(f"Total bytes received: {result['total_bytes']}")
        return result

    def search_books_with_authors(self, query: str) -> Dict[str, Any]:
        """
        Search books and include author information
        Demonstrates over-fetching of unnecessary data
        """
        print(f"\n=== REST: Searching books for '{query}' with authors ===")
        request_count = 0
        total_bytes = 0

        # Request 1: Search books (returns all book fields)
        print(f"Making request: GET {self.base_url}/books?search={query}")
        books_response = self.session.get(f"{self.base_url}/books?search={query}")
        books_data = books_response.json()
        request_count += 1
        total_bytes += len(books_response.content)

        # Request N: Get author for each book
        enriched_books = []
        for book in books_data:
            author_id = book["author_id"]
            print(f"Making request: GET {self.base_url}/authors/{author_id}")
            author_response = self.session.get(f"{self.base_url}/authors/{author_id}")
            author_data = author_response.json()
            request_count += 1
            total_bytes += len(author_response.content)

            enriched_book = book.copy()
            enriched_book["author"] = author_data
            enriched_books.append(enriched_book)

        result = {
            "books": enriched_books,
            "total_requests": request_count,
            "total_bytes": total_bytes,
            "note": "Received all book and author fields, even though we only needed title, price, and author name",
        }

        print(f"Total requests made: {result['total_requests']}")
        print(f"Total bytes received: {result['total_bytes']}")
        return result


def demo_rest_problems():
    """Demonstrate common REST API problems"""
    client = RESTBookstoreClient()

    try:
        # Demo 1: Author with books (multiple requests)
        author_result = client.get_author_with_books(1)
        print(f"\nAuthor: {author_result['author']['name']}")
        print(f"Books: {len(author_result['books'])} books found")

        # Demo 2: Customer order summary (N+1 problem)
        customer_result = client.get_customer_order_summary(1)
        print(f"\nCustomer: {customer_result['customer']['name']}")
        print(f"Orders: {len(customer_result['orders'])} orders found")

        # Demo 3: Book search with authors (over-fetching)
        search_result = client.search_books_with_authors("Python")
        print(f"\nSearch results: {len(search_result['books'])} books found")

        # Summary
        total_requests = (
            author_result["total_requests"]
            + customer_result["total_requests"]
            + search_result["total_requests"]
        )
        total_bytes = (
            author_result["total_bytes"]
            + customer_result["total_bytes"]
            + search_result["total_bytes"]
        )

        print(f"\n=== REST API SUMMARY ===")
        print(f"Total requests made: {total_requests}")
        print(f"Total bytes transferred: {total_bytes}")
        print(f"Average bytes per request: {total_bytes / total_requests:.1f}")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to REST API at http://localhost:8000")
        print("Please make sure the REST API server is running:")
        print("cd rest_api && python app.py")


if __name__ == "__main__":
    demo_rest_problems()
