# API Fundamentals: REST vs GraphQL - Comprehensive Notes

Based on: <https://www.wallarm.com/what/graphql-vs-rest-all-that-you-must-know>

---

## 1. What is API? What is the Inspiration?

### Definition

**API (Application Programming Interface)** is a set of protocols, routines, and tools that allows different software applications to communicate with each other. It defines the methods of communication between various software components.

### The Inspiration Behind APIs

#### Historical Context

- **Problem**: In early software development, applications were monolithic and couldn't easily share data or functionality
- **Need**: As applications grew complex, developers needed a way to:
  - Enable different systems to communicate
  - Share data between applications
  - Reuse functionality across different platforms
  - Allow third-party integrations

#### Core Inspiration

APIs were inspired by the need to:

1. **Break down silos**: Allow isolated systems to work together
2. **Enable modularity**: Create reusable components
3. **Facilitate integration**: Connect different technologies and platforms
4. **Promote scalability**: Distribute functionality across multiple services
5. **Support innovation**: Allow developers to build on existing platforms

### API Evolution Timeline

```
Monolithic Applications → APIs → REST APIs → GraphQL → Modern API Ecosystem
```

---

## 2. REST (Representational State Transfer)

### Definition

**REST** is an architectural style for designing networked applications, introduced by Roy Fielding. It provides a set of principles for creating web services that are simple, scalable, and stateless.

### Core Principles

#### 1. **Stateless**

- Each request contains all information needed to process it
- Server doesn't store client state between requests
- Improves scalability and reliability

#### 2. **Client-Server Architecture**

- Clear separation between client and server
- Independent evolution of both sides
- Better portability and scalability

#### 3. **Cacheable**

- Responses can be cached to improve performance
- Reduces server load and network traffic

#### 4. **Uniform Interface**

- Consistent way to interact with resources
- Uses standard HTTP methods (GET, POST, PUT, DELETE)
- Resource identification through URLs

#### 5. **Layered System**

- Architecture can be composed of hierarchical layers
- Each layer only knows about the immediate layer it's communicating with

### REST Components

#### HTTP Methods

- **GET**: Retrieve data (safe, idempotent)
- **POST**: Create new resources
- **PUT**: Update/replace entire resource (idempotent)
- **PATCH**: Partial update of resource
- **DELETE**: Remove resource (idempotent)

#### Resource Identification

```
https://api.example.com/users/123
https://api.example.com/users/123/posts
https://api.example.com/posts?author=123&limit=10
```

#### Status Codes

- **2xx**: Success (200 OK, 201 Created, 204 No Content)
- **4xx**: Client Error (400 Bad Request, 404 Not Found, 401 Unauthorized)
- **5xx**: Server Error (500 Internal Server Error, 503 Service Unavailable)

### REST Features (From the blog)

- **Uniform Interface**: Device type doesn't impact communication
- **High Scalability**: Can expand to fulfill client needs
- **Easy Resource Access**: Search entities by name
- **HTTP Protocol Based**: Uses standard web protocols
- **Multiple Server Support**: Can be served from multiple servers
- **Simple Architecture**: Straightforward design patterns
- **Easy Data Transmission**: Point-to-point data transfer
- **In-memory Storage**: Supports memory-based data storage

### REST Advantages

- **Easy Development**: Simple to understand and implement
- **Scalability**: Horizontal scaling capabilities
- **Flexibility**: Works with any data format (JSON, XML, etc.)
- **Caching**: Built-in HTTP caching support
- **Stateless**: Each request is independent
- **Mature Ecosystem**: Extensive tooling and documentation

### REST Disadvantages

- **Over/Under-fetching**: May return too much or too little data
- **Multiple Requests**: Often requires multiple API calls
- **No Built-in Query Language**: Limited querying capabilities
- **Versioning Challenges**: API evolution can be complex
- **No Real-time**: Request-response model only

---

## 3. GraphQL

### Definition

**GraphQL** is a query language and runtime for APIs, developed by Facebook in 2012. It provides a more efficient, powerful, and flexible alternative to REST by allowing clients to request exactly the data they need.

### Core Concepts

#### 1. **Single Endpoint**

- All requests go through one URL endpoint
- No multiple endpoints like REST
- Query determines what data is returned

#### 2. **Declarative Data Fetching**

- Client specifies exactly what data it needs
- No over-fetching or under-fetching
- Reduces bandwidth usage

#### 3. **Strongly Typed Schema**

- API schema defines available operations
- Type safety at compile time
- Self-documenting API

#### 4. **Hierarchical Structure**

- Data is organized in a graph-like structure
- Relationships between data are explicit
- Can traverse related data in single query

### GraphQL Operations

#### 1. **Query** (Read Data)

```graphql
query {
  user(id: "123") {
    name
    email
    posts {
      title
      createdAt
    }
  }
}
```

#### 2. **Mutation** (Modify Data)

```graphql
mutation {
  createUser(input: {
    name: "John Doe"
    email: "john@example.com"
  }) {
    id
    name
  }
}
```

#### 3. **Subscription** (Real-time Data)

```graphql
subscription {
  messageAdded(channelId: "general") {
    id
    content
    user {
      name
    }
  }
}
```

### GraphQL Features (From the blog)

- **Statically Typed**: Backend for frontend decoupling
- **No Over-fetching**: Fetch only required data
- **HTTP Agnostic**: Can work over different protocols
- **No Documentation Overhead**: Self-documenting
- **Bandwidth Efficient**: Optimized data transfer
- **API Evolution**: No versioning needed

### GraphQL Advantages

- **Efficient Data Loading**: Fetch multiple resources in single request
- **Strong Type System**: Compile-time error checking
- **Introspection**: API is self-documenting
- **Real-time**: Built-in subscription support
- **Backward Compatibility**: Evolve API without versioning
- **Developer Experience**: Powerful tooling and IDE support

### GraphQL Disadvantages

- **Learning Curve**: More complex than REST
- **Caching Complexity**: HTTP caching is challenging
- **File Uploads**: Not straightforward
- **Query Complexity**: Risk of expensive queries
- **Smaller Ecosystem**: Fewer tools compared to REST

---

## 4. Key Differences: REST vs GraphQL

### Architecture Comparison

| Aspect | REST | GraphQL |
|--------|------|---------|
| **Architecture** | Server-driven | Client-driven |
| **Endpoints** | Multiple endpoints | Single endpoint |
| **Data Fetching** | Fixed data structure | Flexible data structure |
| **Over/Under-fetching** | Common issue | Solved by design |
| **Caching** | HTTP caching | Complex caching |
| **Learning Curve** | Easy to learn | Steeper learning curve |
| **Maturity** | Mature, established | Relatively new |
| **Type System** | Weakly typed | Strongly typed |
| **Versioning** | Requires versioning | Versionless |
| **Real-time** | Requires additional setup | Built-in subscriptions |

### Performance Comparison

#### REST Performance Characteristics

- **Multiple Round Trips**: Often requires multiple API calls
- **Over-fetching**: Returns unnecessary data
- **Under-fetching**: May not return enough data
- **HTTP Caching**: Excellent caching support
- **Predictable**: Response structure is known

#### GraphQL Performance Characteristics

- **Single Request**: Get all needed data in one call
- **Precise Data**: Fetch exactly what's needed
- **Complex Queries**: Risk of expensive operations
- **Caching Challenges**: More complex to cache
- **Network Efficiency**: Reduced bandwidth usage

### Security Comparison

#### REST Security

- **Multiple Security Options**: OAuth 2.0, API keys, JWT
- **HTTP Security**: Standard web security practices
- **Rate Limiting**: Easy to implement per endpoint
- **Attack Surface**: Multiple endpoints to secure
- **Mature Security**: Well-established security practices

#### GraphQL Security

- **Query Depth Limiting**: Prevent complex nested queries
- **Query Cost Analysis**: Analyze query complexity
- **Type Safety**: Compile-time security checks
- **Single Endpoint**: Centralized security control
- **Evolving Security**: Newer security practices

---

## 5. Schema Examples for POST Operations

### REST POST Example

#### Creating a User

```http
POST /api/v1/users
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "department": "Engineering"
}
```

#### Response

```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/v1/users/456

{
  "id": 456,
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "department": "Engineering",
  "createdAt": "2025-09-05T10:30:00Z",
  "updatedAt": "2025-09-05T10:30:00Z"
}
```

#### Creating a Post for User

```http
POST /api/v1/users/456/posts
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post...",
  "tags": ["technology", "programming", "api"],
  "published": true
}
```

### GraphQL Mutation Examples

#### Schema Definition

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  age: Int
  department: String
  posts: [Post!]!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  content: String!
  tags: [String!]!
  published: Boolean!
  author: User!
  createdAt: DateTime!
  updatedAt: DateTime!
}

input CreateUserInput {
  name: String!
  email: String!
  age: Int
  department: String
}

input CreatePostInput {
  title: String!
  content: String!
  tags: [String!]!
  published: Boolean! = false
  authorId: ID!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  createPost(input: CreatePostInput!): Post!
  createUserWithPost(
    userInput: CreateUserInput!
    postInput: CreatePostInput!
  ): User!
}
```

#### Creating a User

```graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
    email
    department
    createdAt
  }
}
```

**Variables:**

```json
{
  "input": {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "department": "Engineering"
  }
}
```

**Response:**

```json
{
  "data": {
    "createUser": {
      "id": "456",
      "name": "John Doe",
      "email": "john@example.com",
      "department": "Engineering",
      "createdAt": "2025-09-05T10:30:00Z"
    }
  }
}
```

#### Creating a Post

```graphql
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    id
    title
    published
    author {
      name
      email
    }
    createdAt
  }
}
```

**Variables:**

```json
{
  "input": {
    "title": "My First Blog Post",
    "content": "This is the content of my first blog post...",
    "tags": ["technology", "programming", "api"],
    "published": true,
    "authorId": "456"
  }
}
```

#### Advanced: Creating User with Post in Single Request

```graphql
mutation CreateUserWithPost(
  $userInput: CreateUserInput!
  $postInput: CreatePostInput!
) {
  createUserWithPost(
    userInput: $userInput
    postInput: $postInput
  ) {
    id
    name
    email
    posts {
      id
      title
      published
      tags
    }
  }
}
```

### Python Code Examples

#### REST POST Implementation

```python
import requests
import json

# REST API POST example
def create_user_rest():
    url = "https://api.example.com/v1/users"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer your-token-here"
    }
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
        "department": "Engineering"
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        user = response.json()
        print(f"User created with ID: {user['id']}")
        return user
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def create_post_rest(user_id):
    url = f"https://api.example.com/v1/users/{user_id}/posts"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer your-token-here"
    }
    data = {
        "title": "My First Blog Post",
        "content": "This is the content...",
        "tags": ["technology", "programming"],
        "published": True
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json() if response.status_code == 201 else None
```

#### GraphQL Mutation Implementation

```python
import requests
import json

def create_user_graphql():
    url = "https://api.example.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer your-token-here"
    }
    
    query = """
    mutation CreateUser($input: CreateUserInput!) {
      createUser(input: $input) {
        id
        name
        email
        department
        createdAt
      }
    }
    """
    
    variables = {
        "input": {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
            "department": "Engineering"
        }
    }
    
    payload = {
        "query": query,
        "variables": variables
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        if "errors" not in result:
            user = result["data"]["createUser"]
            print(f"User created with ID: {user['id']}")
            return user
        else:
            print(f"GraphQL errors: {result['errors']}")
    else:
        print(f"HTTP Error: {response.status_code}")
    
    return None

def create_user_with_post_graphql():
    """Advanced example: Create user and post in single request"""
    url = "https://api.example.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer your-token-here"
    }
    
    query = """
    mutation CreateUserWithPost(
      $userInput: CreateUserInput!
      $postInput: CreatePostInput!
    ) {
      createUserWithPost(
        userInput: $userInput
        postInput: $postInput
      ) {
        id
        name
        email
        posts {
          id
          title
          published
          tags
        }
      }
    }
    """
    
    variables = {
        "userInput": {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "department": "Marketing"
        },
        "postInput": {
            "title": "GraphQL vs REST",
            "content": "Comparing two API approaches...",
            "tags": ["api", "graphql", "rest"],
            "published": True
        }
    }
    
    payload = {
        "query": query,
        "variables": variables
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json() if response.status_code == 200 else None
```

---

## Summary

### When to Choose REST

- **Simple CRUD operations**
- **Caching is important**
- **Team familiar with REST**
- **File uploads/downloads**
- **HTTP caching requirements**

### When to Choose GraphQL

- **Complex data requirements**
- **Mobile applications** (bandwidth concerns)
- **Rapid development cycles**
- **Real-time features needed**
- **Strong typing requirements**

### Key Takeaways

1. **REST** is mature, simple, and cacheable but can lead to over/under-fetching
2. **GraphQL** is efficient, flexible, and strongly-typed but has a steeper learning curve
3. **Choice depends on project requirements**, team expertise, and specific use cases
4. Both can coexist in the same application for different purposes
5. **Security** considerations are important for both approaches
