# API Comparison: REST vs GraphQL

This project demonstrates the practical differences between REST and GraphQL APIs through a complete bookstore example with authors, books, customers, and orders.

## 🎯 Learning Objectives

- Understand REST API limitations (N+1 queries, over-fetching, multiple requests)
- Experience GraphQL advantages (single queries, precise data fetching, type safety)
- Compare performance and development experience between approaches
- See real-world examples of API design trade-offs

## 📁 Project Structure

```
api_comparison/
├── shared/                    # Shared components
│   ├── models.py             # Data models (Author, Book, Customer, Order)
│   └── database.py           # Mock in-memory database with sample data
├── rest_api/                 # Traditional REST API
│   └── app.py                # Flask server with CRUD endpoints
├── graphql_api/              # Modern GraphQL API
│   ├── schema.py             # GraphQL schema, types, and resolvers
│   └── app.py                # FastAPI + Strawberry GraphQL server
├── client_examples/          # Demonstration clients
│   ├── rest_client.py        # Shows REST API problems
│   ├── graphql_client.py     # Shows GraphQL solutions
│   └── compare_apis.py       # Side-by-side comparison
├── requirements.txt          # Python dependencies
├── start_servers.sh          # Convenient startup script
└── README.md                 # This file
```

## 🚀 Quick Start

### Option 1: Automatic Setup

```bash
# Start both servers automatically
./start_servers.sh
```

### Option 2: Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Terminal 1: Start REST API
cd rest_api
python app.py
# Runs on http://localhost:8000

# Terminal 2: Start GraphQL API  
cd graphql_api
python app.py
# Runs on http://localhost:8001

# Terminal 3: Run comparison
cd client_examples
python compare_apis.py
```

## 🔍 API Exploration

### REST API (Flask)

- **Base URL**: <http://localhost:8000>
- **Swagger Docs**: <http://localhost:8000/docs>
- **Health Check**: <http://localhost:8000/health>

**Example REST Endpoints:**

```bash
GET    /authors                    # List all authors
GET    /authors/1                  # Get specific author
POST   /authors                    # Create author
GET    /books?author_id=1          # Get books by author
GET    /customers/1/orders         # Get customer orders
```

### GraphQL API (Strawberry + FastAPI)

- **GraphQL Endpoint**: <http://localhost:8001/graphql>
- **GraphiQL UI**: <http://localhost:8001/graphql> (interactive playground)
- **Health Check**: <http://localhost:8001/health>

**Example GraphQL Queries:**

```graphql
# Get author with books (single request)
query {
  author(id: 1) {
    name
    email
    books {
      title
      price
      genre
    }
  }
}

# Search books with precise field selection
query {
  searchBooks(query: "Python", limit: 5) {
    title
    price
    author {
      name
    }
  }
}

# Complex nested query (impossible with single REST request)
query {
  customer(id: 1) {
    name
    orders {
      orderDate
      totalAmount
      items {
        quantity
        book {
          title
          author {
            name
          }
        }
      }
    }
  }
}
```

## ⚡ Performance Comparison

### Problem 1: Multiple Requests

**REST**: Author + Books = 2 requests

```bash
GET /authors/1      # Request 1
GET /books?author_id=1  # Request 2
```

**GraphQL**: Author + Books = 1 request

```graphql
query {
  author(id: 1) {
    name
    books { title price }
  }
}
```

### Problem 2: N+1 Query Problem

**REST**: Customer with order details = 1 + N + M requests

- 1 request for customer
- N requests for each order  
- M requests for each book in orders

**GraphQL**: Customer with order details = 1 request

```graphql
query {
  customer(id: 1) {
    orders {
      items {
        book { title }
      }
    }
  }
}
```

### Problem 3: Over-fetching vs Precise Fetching

**REST**: Always returns all fields

```json
{
  "id": 1,
  "title": "Python Programming",
  "isbn": "978-1234567890",
  "price": 29.99,
  "publication_date": "2023-01-15T00:00:00",
  "author_id": 1,
  "genre": "Programming",
  "description": "A comprehensive guide to Python..."
}
```

**GraphQL**: Request only needed fields

```graphql
query {
  books {
    title    # Only title
    price    # Only price
  }
}
```

## 🔧 Technologies Used

### REST API Stack

- **Framework**: Flask (lightweight Python web framework)
- **Documentation**: Swagger/OpenAPI (automatic API docs)
- **Validation**: Manual request validation
- **Serialization**: JSON with manual handling

### GraphQL API Stack

- **Framework**: FastAPI (modern async Python framework)
- **GraphQL Library**: Strawberry GraphQL (Python-native GraphQL)
- **Documentation**: GraphiQL (interactive GraphQL explorer)
- **Validation**: Automatic with type system
- **Serialization**: Automatic with schema types

### Shared Components

- **Database**: In-memory mock database with sample data
- **Models**: Python dataclasses for type safety
- **Testing**: HTTP clients for comparison demonstrations

## 📊 Comparison Results

Run `python client_examples/compare_apis.py` to see real performance metrics:

**Typical Results:**

```
COMPARISON 1: Author with Books
REST API:     2 requests, 1,250 bytes, 0.045s
GraphQL API:  1 request, 890 bytes,   0.023s
GraphQL is 2.0x fewer requests, 1.4x less data, 2.0x faster

COMPARISON 2: Customer Order Details  
REST API:     8 requests, 3,420 bytes, 0.124s (N+1 problem)
GraphQL API:  1 request, 1,680 bytes, 0.031s
GraphQL is 8.0x fewer requests, 2.0x less data, 4.0x faster
```

## 🎓 Key Learnings

### REST API Challenges

- ❌ **Multiple Requests**: Need separate calls for related data
- ❌ **N+1 Problem**: Nested relationships create exponential requests
- ❌ **Over-fetching**: Always returns all fields
- ❌ **Under-fetching**: Missing data requires additional requests
- ❌ **API Versioning**: Breaking changes need new endpoints

### GraphQL Advantages

- ✅ **Single Request**: Get complex nested data in one call
- ✅ **Precise Fetching**: Request exactly the fields you need
- ✅ **No N+1 Problem**: Resolvers handle relationships efficiently
- ✅ **Strong Types**: Schema provides type safety and validation
- ✅ **Self-Documenting**: Introspection and GraphiQL explorer
- ✅ **Evolutionary**: Add fields without breaking existing clients

### When to Choose What

**Choose GraphQL When:**

- Complex data relationships
- Multiple client types (mobile, web, desktop)
- Performance is critical
- Rapid frontend development
- Strong typing is important

**Choose REST When:**

- Simple CRUD operations
- File uploads/downloads
- HTTP caching is critical
- Team is unfamiliar with GraphQL
- Simple microservices

## 🛠️ Development Tips

### Extending the APIs

**Adding a new field to REST:**

1. Update database model
2. Modify endpoint response
3. Update documentation
4. Version API if breaking change

**Adding a new field to GraphQL:**

1. Update database model
2. Add field to GraphQL type
3. Schema automatically updates
4. No breaking changes for existing clients

### Testing the APIs

**REST Testing:**

```bash
# Using curl
curl http://localhost:8000/authors/1

# Using httpie
http localhost:8000/authors/1
```

**GraphQL Testing:**

```bash
# Using curl
curl -X POST http://localhost:8001/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ author(id: 1) { name } }"}'

# Or use the GraphiQL UI at http://localhost:8001/graphql
```

## 📚 Further Reading

- [GraphQL Official Documentation](https://graphql.org/)
- [Strawberry GraphQL Documentation](https://strawberry.rocks/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [REST API Design Best Practices](https://restfulapi.net/)

## 🤝 Contributing

This is an educational project. Feel free to:

- Add more complex queries
- Implement additional features (pagination, filtering, subscriptions)
- Add authentication examples
- Create frontend clients
- Improve error handling

## 📝 License

This project is created for educational purposes. Use freely for learning and teaching.
