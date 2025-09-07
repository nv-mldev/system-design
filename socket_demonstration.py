#!/usr/bin/env python3
"""
Practical demonstration of IP, Ports, and Sockets
Shows how computers communicate via network endpoints
"""

import socket
import threading
import time


def demonstrate_socket_basics():
    """Show the fundamental concepts with real examples"""

    print("=" * 60)
    print("FUNDAMENTAL NETWORKING CONCEPTS DEMONSTRATION")
    print("=" * 60)

    # 1. Show current machine's network identity
    print("\n1. YOUR COMPUTER'S NETWORK IDENTITY:")
    print("-" * 40)

    # Get local IP
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    temp_socket.connect(("8.8.8.8", 80))
    local_ip = temp_socket.getsockname()[0]
    temp_socket.close()

    print(f"   Local IP Address: {local_ip}")
    print(f"   Loopback Address: 127.0.0.1")
    print(f"   Machine Hostname: {socket.gethostname()}")

    # 2. Demonstrate port concepts
    print("\n2. HOW PORTS WORK:")
    print("-" * 40)
    print("   Ports are like 'apartment numbers' for your IP address")
    print("   Your computer can have 65,535 different ports (0-65535)")
    print("   Multiple applications can use network simultaneously")

    # 3. Create a simple server to show port binding
    print("\n3. CREATING A SERVER SOCKET:")
    print("-" * 40)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to a specific port
    server_port = 8888
    server_socket.bind((local_ip, server_port))
    server_socket.listen(1)

    print(f"   ✅ Server created and bound to: {local_ip}:{server_port}")
    print(f"   📍 Full socket address: {local_ip}:{server_port}")
    print(f"   🎯 Other computers can connect to this socket")

    # 4. Show what happens when client connects
    print("\n4. DEMONSTRATING CLIENT-SERVER CONNECTION:")
    print("-" * 40)

    def simple_server():
        """Simple server that accepts one connection"""
        try:
            print("   🔄 Server waiting for connection...")
            client_conn, client_address = server_socket.accept()
            print(f"   ✅ Connection received from: {client_address}")

            # Show the socket pair
            local_endpoint = client_conn.getsockname()
            remote_endpoint = client_conn.getpeername()

            print(f"   📡 Socket Pair Created:")
            print(f"      Server Socket: {local_endpoint[0]}:{local_endpoint[1]}")
            print(f"      Client Socket: {remote_endpoint[0]}:{remote_endpoint[1]}")

            # Receive and respond to data
            data = client_conn.recv(1024).decode()
            print(f"   📨 Received: {data}")

            response = f"Hello from server! You connected from {remote_endpoint}"
            client_conn.send(response.encode())
            print(f"   📤 Sent: {response}")

            client_conn.close()

        except Exception as e:
            print(f"   ❌ Server error: {e}")

    # Start server in background
    server_thread = threading.Thread(target=simple_server)
    server_thread.start()

    # Give server time to start
    time.sleep(0.5)

    # 5. Create client connection
    print("\n   🔌 Creating client connection...")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((local_ip, server_port))

    # Show client's socket information
    client_local = client_socket.getsockname()
    client_remote = client_socket.getpeername()

    print(f"   📍 Client's local socket: {client_local[0]}:{client_local[1]}")
    print(f"   🎯 Client connecting to: {client_remote[0]}:{client_remote[1]}")

    # Send data
    message = "Hello from client!"
    client_socket.send(message.encode())

    # Receive response
    response = client_socket.recv(1024).decode()
    print(f"   📨 Client received: {response}")

    client_socket.close()
    server_thread.join()
    server_socket.close()

    # 6. Explain what just happened
    print("\n5. WHAT JUST HAPPENED STEP-BY-STEP:")
    print("-" * 40)
    print("   1. Server bound to IP:Port (claimed that address)")
    print("   2. Operating System updated its port table")
    print("   3. Client connected using its own temporary port")
    print("   4. OS created a socket pair (connection endpoints)")
    print("   5. Data flowed between the two sockets")
    print("   6. Connection closed, ports released")

    print("\n6. KEY CONCEPTS SUMMARY:")
    print("-" * 40)
    print("   🏠 IP Address = Street address (which computer)")
    print("   🚪 Port = Apartment number (which application)")
    print("   🔌 Socket = Complete address (IP:Port + protocol)")
    print("   📬 OS = Mail service (delivers packets to right app)")
    print("   ✅ ALL network communication uses IP + Port combination")

    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_socket_basics()
