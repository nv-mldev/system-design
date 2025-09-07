"""
FastAPI GraphQL Server for Bookstore API
Demonstrates modern GraphQL API with Strawberry and FastAPI
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from schema import schema

# Create FastAPI app
app = FastAPI(
    title="Bookstore GraphQL API",
    description="A comprehensive GraphQL API for a bookstore with authors, books, customers, and orders",
    version="1.0.0",
)

# Add CORS middleware for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create GraphQL router
graphql_app = GraphQLRouter(schema, graphiql=True)

# Mount GraphQL endpoint
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Bookstore GraphQL API",
        "graphql_endpoint": "/graphql",
        "graphiql_ui": "/graphql (with GraphiQL interface)",
        "documentation": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "api": "GraphQL Bookstore API"}


if __name__ == "__main__":
    print("Starting GraphQL Bookstore API...")
    print("GraphQL endpoint: http://localhost:8001/graphql")
    print("GraphiQL UI: http://localhost:8001/graphql")
    print("API documentation: http://localhost:8001/docs")

    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True, log_level="info")
