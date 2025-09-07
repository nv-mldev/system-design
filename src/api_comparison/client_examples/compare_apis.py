"""
API Comparison Script
Compares REST vs GraphQL performance and efficiency
"""

import time
import requests
from rest_client import RESTBookstoreClient
from graphql_client import GraphQLBookstoreClient


def check_servers():
    """Check if both API servers are running"""
    rest_running = False
    graphql_running = False

    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            rest_running = True
    except:
        pass

    try:
        response = requests.get("http://localhost:8001/health", timeout=2)
        if response.status_code == 200:
            graphql_running = True
    except:
        pass

    return rest_running, graphql_running


def compare_author_with_books():
    """Compare getting author with books between REST and GraphQL"""
    print("\n" + "=" * 60)
    print("COMPARISON 1: Author with Books")
    print("=" * 60)

    rest_client = RESTBookstoreClient()
    graphql_client = GraphQLBookstoreClient()

    # REST approach
    start_time = time.time()
    rest_result = rest_client.get_author_with_books(1)
    rest_time = time.time() - start_time

    # GraphQL approach
    start_time = time.time()
    graphql_result = graphql_client.get_author_with_books(1)
    graphql_time = time.time() - start_time

    print(f"\nRESULTS:")
    print(f"REST API:")
    print(f"  - Requests: {rest_result['total_requests']}")
    print(f"  - Bytes: {rest_result['total_bytes']}")
    print(f"  - Time: {rest_time:.3f}s")

    print(f"GraphQL API:")
    print(f"  - Requests: {graphql_result['total_requests']}")
    print(f"  - Bytes: {graphql_result['total_bytes']}")
    print(f"  - Time: {graphql_time:.3f}s")

    print(f"\nGraphQL is:")
    print(
        f"  - {rest_result['total_requests'] / graphql_result['total_requests']:.1f}x fewer requests"
    )
    print(
        f"  - {rest_result['total_bytes'] / graphql_result['total_bytes']:.1f}x less data"
    )
    print(f"  - {rest_time / graphql_time:.1f}x faster")


def compare_customer_orders():
    """Compare getting customer with order details"""
    print("\n" + "=" * 60)
    print("COMPARISON 2: Customer with Order Details")
    print("=" * 60)

    rest_client = RESTBookstoreClient()
    graphql_client = GraphQLBookstoreClient()

    # REST approach (demonstrates N+1 problem)
    start_time = time.time()
    rest_result = rest_client.get_customer_order_summary(1)
    rest_time = time.time() - start_time

    # GraphQL approach (single query)
    start_time = time.time()
    graphql_result = graphql_client.get_customer_order_summary(1)
    graphql_time = time.time() - start_time

    print(f"\nRESULTS:")
    print(f"REST API (N+1 Problem):")
    print(f"  - Requests: {rest_result['total_requests']}")
    print(f"  - Bytes: {rest_result['total_bytes']}")
    print(f"  - Time: {rest_time:.3f}s")

    print(f"GraphQL API (Single Query):")
    print(f"  - Requests: {graphql_result['total_requests']}")
    print(f"  - Bytes: {graphql_result['total_bytes']}")
    print(f"  - Time: {graphql_time:.3f}s")

    print(f"\nGraphQL eliminates the N+1 problem:")
    print(
        f"  - {rest_result['total_requests'] / graphql_result['total_requests']:.1f}x fewer requests"
    )
    print(f"  - {rest_time / graphql_time:.1f}x faster")


def compare_book_search():
    """Compare book search with author information"""
    print("\n" + "=" * 60)
    print("COMPARISON 3: Book Search with Authors")
    print("=" * 60)

    rest_client = RESTBookstoreClient()
    graphql_client = GraphQLBookstoreClient()

    # REST approach (over-fetching)
    start_time = time.time()
    rest_result = rest_client.search_books_with_authors("Python")
    rest_time = time.time() - start_time

    # GraphQL approach (precise fetching)
    start_time = time.time()
    graphql_result = graphql_client.search_books_with_authors("Python")
    graphql_time = time.time() - start_time

    print(f"\nRESULTS:")
    print(f"REST API (Over-fetching):")
    print(f"  - Requests: {rest_result['total_requests']}")
    print(f"  - Bytes: {rest_result['total_bytes']}")
    print(f"  - Time: {rest_time:.3f}s")
    print(f"  - Note: {rest_result['note']}")

    print(f"GraphQL API (Precise fetching):")
    print(f"  - Requests: {graphql_result['total_requests']}")
    print(f"  - Bytes: {graphql_result['total_bytes']}")
    print(f"  - Time: {graphql_time:.3f}s")
    print(f"  - Note: {graphql_result['note']}")

    print(f"\nGraphQL reduces over-fetching:")
    print(
        f"  - {rest_result['total_bytes'] / graphql_result['total_bytes']:.1f}x less data transferred"
    )


def demonstrate_graphql_flexibility():
    """Show GraphQL's flexibility for different client needs"""
    print("\n" + "=" * 60)
    print("DEMONSTRATION: GraphQL Flexibility")
    print("=" * 60)

    graphql_client = GraphQLBookstoreClient()
    result = graphql_client.get_flexible_book_data()

    print(f"\nSame API endpoint, different data for different clients:")
    print(f"Mobile app (minimal data): {result['mobile_bytes']} bytes")
    print(f"Desktop app (rich data): {result['desktop_bytes']} bytes")
    print(f"Desktop is {result['desktop_bytes'] / result['mobile_bytes']:.1f}x larger")
    print(f"\nWith REST, you'd need separate endpoints or over-fetch for mobile")


def main():
    """Run the complete API comparison"""
    print("REST vs GraphQL API Comparison")
    print("=" * 60)

    # Check if servers are running
    rest_running, graphql_running = check_servers()

    if not rest_running:
        print("❌ REST API server is not running!")
        print("Start it with: cd rest_api && python app.py")
        return

    if not graphql_running:
        print("❌ GraphQL API server is not running!")
        print("Start it with: cd graphql_api && python app.py")
        return

    print("✅ Both API servers are running")

    try:
        # Run comparisons
        compare_author_with_books()
        compare_customer_orders()
        compare_book_search()
        demonstrate_graphql_flexibility()

        # Final summary
        print("\n" + "=" * 60)
        print("SUMMARY: Key Differences")
        print("=" * 60)
        print("\nREST API Challenges:")
        print("  ❌ Multiple requests needed for related data")
        print("  ❌ N+1 query problem for nested relationships")
        print("  ❌ Over-fetching unnecessary data")
        print("  ❌ Under-fetching requires additional requests")
        print("  ❌ API versioning needed for changes")

        print("\nGraphQL Advantages:")
        print("  ✅ Single request for complex data")
        print("  ✅ No N+1 problem with proper resolvers")
        print("  ✅ Fetch exactly what you need")
        print("  ✅ No under-fetching or over-fetching")
        print("  ✅ Schema evolution without versioning")
        print("  ✅ Self-documenting with introspection")
        print("  ✅ Strong type system")

        print("\nWhen to use GraphQL:")
        print("  • Complex data relationships")
        print("  • Multiple client types (mobile, web, etc.)")
        print("  • Performance-critical applications")
        print("  • Rapid frontend development")

        print("\nWhen REST might be better:")
        print("  • Simple CRUD operations")
        print("  • File uploads/downloads")
        print("  • Caching is critical")
        print("  • Team unfamiliar with GraphQL")

    except Exception as e:
        print(f"Error during comparison: {e}")
        print("Make sure both API servers are running and accessible")


if __name__ == "__main__":
    main()
