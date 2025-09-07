"""
GraphQL API Client Examples
Demonstrates efficiency and flexibility of GraphQL
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8001/graphql"


class GraphQLBookstoreClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def execute_query(
        self, query: str, variables: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute a GraphQL query"""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        response = self.session.post(self.base_url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_author_with_books(self, author_id: int) -> Dict[str, Any]:
        """
        Get author details with all their books in ONE REQUEST
        Demonstrates GraphQL efficiency
        """
        print(f"\n=== GraphQL: Getting author {author_id} with books ===")

        query = """
        query GetAuthorWithBooks($authorId: Int!) {
            author(id: $authorId) {
                id
                name
                email
                bio
                books {
                    id
                    title
                    price
                    genre
                    publicationDate
                }
            }
        }
        """

        print(f"Making ONE request: POST {self.base_url}")
        response = self.session.post(
            self.base_url, json={"query": query, "variables": {"authorId": author_id}}
        )

        result = response.json()
        result["total_requests"] = 1
        result["total_bytes"] = len(response.content)

        print(f"Total requests made: {result['total_requests']}")
        print(f"Total bytes received: {result['total_bytes']}")
        return result

    def get_customer_order_summary(self, customer_id: int) -> Dict[str, Any]:
        """
        Get customer with their orders and book details in ONE REQUEST
        Demonstrates solving N+1 problem with GraphQL
        """
        print(f"\n=== GraphQL: Getting customer {customer_id} order summary ===")

        query = """
        query GetCustomerOrderSummary($customerId: Int!) {
            customer(id: $customerId) {
                id
                name
                email
                orders {
                    id
                    orderDate
                    totalAmount
                    status
                    items {
                        quantity
                        price
                        book {
                            id
                            title
                            price
                        }
                    }
                }
            }
        }
        """

        print(f"Making ONE request: POST {self.base_url}")
        response = self.session.post(
            self.base_url,
            json={"query": query, "variables": {"customerId": customer_id}},
        )

        result = response.json()
        result["total_requests"] = 1
        result["total_bytes"] = len(response.content)

        print(f"Total requests made: {result['total_requests']}")
        print(f"Total bytes received: {result['total_bytes']}")
        return result

    def search_books_with_authors(self, query_text: str) -> Dict[str, Any]:
        """
        Search books and get ONLY the fields we need
        Demonstrates precise data fetching with GraphQL
        """
        print(f"\n=== GraphQL: Searching books for '{query_text}' ===")

        query = """
        query SearchBooksWithAuthors($searchQuery: String!) {
            searchBooks(query: $searchQuery, limit: 10) {
                title
                price
                author {
                    name
                }
            }
        }
        """

        print(f"Making ONE request: POST {self.base_url}")
        response = self.session.post(
            self.base_url,
            json={"query": query, "variables": {"searchQuery": query_text}},
        )

        result = response.json()
        result["total_requests"] = 1
        result["total_bytes"] = len(response.content)
        result["note"] = (
            "Received ONLY the fields requested: title, price, and author name"
        )

        print(f"Total requests made: {result['total_requests']}")
        print(f"Total bytes received: {result['total_bytes']}")
        return result

    def get_flexible_book_data(self) -> Dict[str, Any]:
        """
        Demonstrate GraphQL flexibility - different clients can request different data
        """
        print(f"\n=== GraphQL: Flexible data fetching ===")

        # Mobile app query - minimal data for performance
        mobile_query = """
        query MobileBookList {
            books(limit: 5) {
                id
                title
                price
            }
        }
        """

        # Desktop app query - rich data for detailed display
        desktop_query = """
        query DesktopBookList {
            books(limit: 5) {
                id
                title
                price
                genre
                description
                publicationDate
                author {
                    name
                    bio
                }
            }
        }
        """

        print("Mobile query - fetching minimal data...")
        mobile_response = self.session.post(self.base_url, json={"query": mobile_query})

        print("Desktop query - fetching rich data...")
        desktop_response = self.session.post(
            self.base_url, json={"query": desktop_query}
        )

        return {
            "mobile_data": mobile_response.json(),
            "desktop_data": desktop_response.json(),
            "mobile_bytes": len(mobile_response.content),
            "desktop_bytes": len(desktop_response.content),
            "total_requests": 2,
            "note": "Same API, different data based on client needs",
        }


def demo_graphql_advantages():
    """Demonstrate GraphQL advantages over REST"""
    client = GraphQLBookstoreClient()

    try:
        # Demo 1: Author with books (single request)
        author_result = client.get_author_with_books(1)
        if "data" in author_result and author_result["data"]["author"]:
            author = author_result["data"]["author"]
            print(f"\nAuthor: {author['name']}")
            print(f"Books: {len(author['books'])} books found")

        # Demo 2: Customer order summary (single request, no N+1)
        customer_result = client.get_customer_order_summary(1)
        if "data" in customer_result and customer_result["data"]["customer"]:
            customer = customer_result["data"]["customer"]
            print(f"\nCustomer: {customer['name']}")
            print(f"Orders: {len(customer['orders'])} orders found")

        # Demo 3: Precise book search (only requested fields)
        search_result = client.search_books_with_authors("Python")
        if "data" in search_result:
            books = search_result["data"]["searchBooks"]
            print(f"\nSearch results: {len(books)} books found")

        # Demo 4: Flexible data fetching
        flexible_result = client.get_flexible_book_data()
        mobile_size = flexible_result["mobile_bytes"]
        desktop_size = flexible_result["desktop_bytes"]
        print(f"\nFlexible fetching:")
        print(f"Mobile app data: {mobile_size} bytes")
        print(f"Desktop app data: {desktop_size} bytes")
        print(f"Desktop data is {desktop_size / mobile_size:.1f}x larger")

        # Summary
        total_requests = (
            author_result["total_requests"]
            + customer_result["total_requests"]
            + search_result["total_requests"]
            + flexible_result["total_requests"]
        )
        total_bytes = (
            author_result["total_bytes"]
            + customer_result["total_bytes"]
            + search_result["total_bytes"]
            + flexible_result["mobile_bytes"]
            + flexible_result["desktop_bytes"]
        )

        print(f"\n=== GraphQL API SUMMARY ===")
        print(f"Total requests made: {total_requests}")
        print(f"Total bytes transferred: {total_bytes}")
        print(f"Average bytes per request: {total_bytes / total_requests:.1f}")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to GraphQL API at http://localhost:8001")
        print("Please make sure the GraphQL API server is running:")
        print("cd graphql_api && python app.py")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    demo_graphql_advantages()
