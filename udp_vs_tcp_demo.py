#!/usr/bin/env python3
"""
Demonstration of TCP vs UDP connections
Shows the difference between connection-oriented and connectionless protocols
"""

import socket
import time
import threading


def tcp_server():
    """TCP Server - Connection-Oriented"""
    print("=== TCP SERVER (Connection-Oriented) ===")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 8080))
    server_socket.listen(1)
    print("TCP Server listening on port 8080...")

    while True:
        # Wait for a connection
        print("Waiting for client connection...")
        client_socket, address = server_socket.accept()
        print(f"✅ CONNECTION ESTABLISHED with {address}")
        print("   → Server now maintains connection state")
        print("   → Both sides track the session")

        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"📨 Received: {data.decode()}")
                client_socket.send(b"ACK: Message received")
                print("📤 Sent acknowledgment back")
        except:
            pass
        finally:
            print("❌ CONNECTION CLOSED")
            print("   → Server cleans up connection state")
            client_socket.close()


def udp_server():
    """UDP Server - Connectionless"""
    print("\n=== UDP SERVER (Connectionless) ===")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("localhost", 8081))
    print("UDP Server listening on port 8081...")
    print("⚠️  NO CONNECTION ESTABLISHMENT NEEDED")
    print("   → Server just waits for individual packets")
    print("   → No session state maintained")

    while True:
        try:
            data, address = server_socket.recvfrom(1024)
            print(f"📨 Received packet from {address}: {data.decode()}")
            print("   → Each packet is independent")
            print("   → No connection state to track")
            # Note: We could send back, but it's optional in UDP
        except:
            break


def tcp_client():
    """TCP Client - Must establish connection first"""
    print("\n=== TCP CLIENT ===")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("1. Attempting to connect to server...")
    try:
        client_socket.connect(("localhost", 8080))
        print("2. ✅ CONNECTION ESTABLISHED!")
        print("   → Three-way handshake completed")
        print("   → Client maintains connection state")

        # Send some data
        for i in range(3):
            message = f"TCP Message {i+1}"
            print(f"3. Sending: {message}")
            client_socket.send(message.encode())

            response = client_socket.recv(1024)
            print(f"4. ✅ Received ACK: {response.decode()}")
            time.sleep(1)

    except ConnectionRefusedError:
        print("❌ Connection refused - server not running")
    finally:
        print("5. Closing connection...")
        client_socket.close()


def udp_client():
    """UDP Client - No connection needed"""
    print("\n=== UDP CLIENT ===")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("⚠️  NO CONNECTION ESTABLISHMENT")
    print("   → Just create socket and send data")
    print("   → No handshake required")

    # Send some data
    for i in range(3):
        message = f"UDP Packet {i+1}"
        print(f"📤 Sending packet: {message}")
        client_socket.sendto(message.encode(), ("localhost", 8081))
        print("   → Packet sent immediately")
        print("   → No acknowledgment expected")
        print("   → No connection state to maintain")
        time.sleep(1)

    client_socket.close()
    print("✅ Done sending packets")


def demonstrate_difference():
    """Show the key differences"""
    print("=" * 60)
    print("TCP vs UDP COMMUNICATION PATTERNS")
    print("=" * 60)

    # Start servers in background
    tcp_thread = threading.Thread(target=tcp_server, daemon=True)
    udp_thread = threading.Thread(target=udp_server, daemon=True)

    tcp_thread.start()
    udp_thread.start()

    time.sleep(1)  # Let servers start

    # Demonstrate TCP
    tcp_client()

    time.sleep(1)

    # Demonstrate UDP
    udp_client()

    print("\n" + "=" * 60)
    print("KEY DIFFERENCES:")
    print("=" * 60)
    print("TCP (Connection-Oriented):")
    print("  ✅ Establishes logical session")
    print("  ✅ Maintains connection state")
    print("  ✅ Reliable delivery with ACKs")
    print("  ✅ Ordered delivery guaranteed")
    print("  ❌ Higher overhead")
    print("  ❌ Slower due to handshakes")

    print("\nUDP (Connectionless):")
    print("  ✅ No session establishment")
    print("  ✅ No connection state")
    print("  ✅ Very fast")
    print("  ✅ Low overhead")
    print("  ❌ No delivery guarantees")
    print("  ❌ Packets can be lost/reordered")


if __name__ == "__main__":
    demonstrate_difference()
