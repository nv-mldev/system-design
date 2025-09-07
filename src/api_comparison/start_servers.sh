#!/bin/bash

# API Comparison Startup Script
# Starts both REST and GraphQL servers for comparison

echo "Starting API Comparison Demo"
echo "============================"

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Function to start a server in the background
start_server() {
    local dir=$1
    local port=$2
    local name=$3
    
    echo "Starting $name server on port $port..."
    cd "$dir"
    python app.py &
    local pid=$!
    echo "$name server PID: $pid"
    cd ..
    return $pid
}

# Start REST API server
start_server "rest_api" 8000 "REST"
REST_PID=$!

# Wait a moment for REST server to start
sleep 2

# Start GraphQL API server
start_server "graphql_api" 8001 "GraphQL"
GRAPHQL_PID=$!

# Wait a moment for GraphQL server to start
sleep 3

echo ""
echo "Servers started successfully!"
echo "REST API: http://localhost:8000"
echo "  - Swagger docs: http://localhost:8000/docs"
echo "  - Health check: http://localhost:8000/health"
echo ""
echo "GraphQL API: http://localhost:8001/graphql"
echo "  - GraphiQL UI: http://localhost:8001/graphql"
echo "  - Health check: http://localhost:8001/health"
echo ""
echo "To run the comparison:"
echo "  cd client_examples"
echo "  python compare_apis.py"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $REST_PID 2>/dev/null
    kill $GRAPHQL_PID 2>/dev/null
    echo "Servers stopped."
    exit 0
}

# Trap Ctrl+C and cleanup
trap cleanup SIGINT

# Keep script running
while true; do
    sleep 1
done