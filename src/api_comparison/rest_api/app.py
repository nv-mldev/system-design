"""
Flask REST API for the bookstore
Demonstrates traditional REST API patterns
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add parent directory to path to import shared modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.database import db


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route("/")
def home():
    return jsonify(
        {
            "message": "Bookstore REST API",
            "version": "1.0",
            "endpoints": {
                "books": "/api/books",
                "authors": "/api/authors",
                "customers": "/api/customers",
                "orders": "/api/orders",
            },
        }
    )


# Book endpoints
@app.route("/api/books", methods=["GET"])
def get_books():
    """Get all books - returns ALL book data (over-fetching demo)"""
    books = db.get_all_books()

    # Option to include author data (requires query parameter)
    include_author = request.args.get("include_author", "false").lower() == "true"

    result = []
    for book in books:
        if include_author:
            author = db.get_author_for_book(book)
            result.append(book.to_dict(include_author=True, author=author))
        else:
            result.append(book.to_dict())

    return jsonify(result)


@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    """Get single book by ID"""
    book = db.get_book_by_id(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    include_author = request.args.get("include_author", "false").lower() == "true"

    if include_author:
        author = db.get_author_for_book(book)
        return jsonify(book.to_dict(include_author=True, author=author))

    return jsonify(book.to_dict())


@app.route("/api/books", methods=["POST"])
def create_book():
    """Create a new book"""
    data = request.get_json()

    required_fields = ["title", "author_id", "price", "genre", "published_year", "isbn"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        book = db.create_book(
            title=data["title"],
            author_id=data["author_id"],
            price=float(data["price"]),
            genre=data["genre"],
            published_year=int(data["published_year"]),
            isbn=data["isbn"],
        )
        return jsonify(book.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/books/by-genre/<genre>", methods=["GET"])
def get_books_by_genre(genre):
    """Get books by genre"""
    books = db.get_books_by_genre(genre)
    return jsonify([book.to_dict() for book in books])


# Author endpoints
@app.route("/api/authors", methods=["GET"])
def get_authors():
    """Get all authors"""
    authors = db.get_all_authors()
    return jsonify([author.to_dict() for author in authors])


@app.route("/api/authors/<int:author_id>", methods=["GET"])
def get_author(author_id):
    """Get single author by ID"""
    author = db.get_author_by_id(author_id)
    if not author:
        return jsonify({"error": "Author not found"}), 404
    return jsonify(author.to_dict())


@app.route("/api/authors/<int:author_id>/books", methods=["GET"])
def get_author_books(author_id):
    """Get all books by a specific author - requires separate endpoint"""
    author = db.get_author_by_id(author_id)
    if not author:
        return jsonify({"error": "Author not found"}), 404

    books = db.get_books_by_author(author_id)
    return jsonify([book.to_dict() for book in books])


# Customer endpoints
@app.route("/api/customers", methods=["GET"])
def get_customers():
    """Get all customers"""
    customers = db.get_all_customers()
    return jsonify([customer.to_dict() for customer in customers])


@app.route("/api/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    """Get single customer by ID"""
    customer = db.get_customer_by_id(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(customer.to_dict())


@app.route("/api/customers/<int:customer_id>/orders", methods=["GET"])
def get_customer_orders(customer_id):
    """Get all orders for a customer - separate endpoint needed"""
    customer = db.get_customer_by_id(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    orders = db.get_orders_by_customer(customer_id)

    # Option to include book details
    include_books = request.args.get("include_books", "false").lower() == "true"

    result = []
    for order in orders:
        if include_books:
            books = db.get_books_for_order(order)
            result.append(order.to_dict(include_books=True, books=books))
        else:
            result.append(order.to_dict())

    return jsonify(result)


@app.route("/api/customers", methods=["POST"])
def create_customer():
    """Create a new customer"""
    data = request.get_json()

    required_fields = ["name", "email"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        customer = db.create_customer(name=data["name"], email=data["email"])
        return jsonify(customer.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Order endpoints
@app.route("/api/orders", methods=["GET"])
def get_orders():
    """Get all orders"""
    orders = db.get_all_orders()
    return jsonify([order.to_dict() for order in orders])


@app.route("/api/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    """Get single order by ID"""
    order = db.get_order_by_id(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    include_customer = request.args.get("include_customer", "false").lower() == "true"
    include_books = request.args.get("include_books", "false").lower() == "true"

    customer = db.get_customer_for_order(order) if include_customer else None
    books = db.get_books_for_order(order) if include_books else None

    return jsonify(
        order.to_dict(
            include_customer=include_customer,
            include_books=include_books,
            customer=customer,
            books=books,
        )
    )


@app.route("/api/orders", methods=["POST"])
def create_order():
    """Create a new order"""
    data = request.get_json()

    required_fields = ["customer_id", "book_ids"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Validate customer exists
    customer = db.get_customer_by_id(data["customer_id"])
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    # Validate all books exist
    for book_id in data["book_ids"]:
        book = db.get_book_by_id(book_id)
        if not book:
            return jsonify({"error": f"Book with ID {book_id} not found"}), 404

    try:
        order = db.create_order(
            customer_id=data["customer_id"], book_ids=data["book_ids"]
        )
        return jsonify(order.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    print("Starting Bookstore REST API...")
    print("Available at: http://localhost:5000")
    print("\nExample endpoints:")
    print("- GET  /api/books")
    print("- GET  /api/books/1")
    print("- GET  /api/authors/1/books")
    print("- GET  /api/customers/1/orders?include_books=true")
    print("- POST /api/books")
    print("- POST /api/orders")

    app.run(debug=True, port=5000)
