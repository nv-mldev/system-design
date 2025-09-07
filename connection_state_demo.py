#!/usr/bin/env python3
"""
Simple demo showing connection state vs connectionless
"""

import socket
import time

print("=== DEMONSTRATING CONNECTION STATE ===\n")

# 1. Create TCP socket (will establish connection state)
print("1. Creating TCP connection to google.com...")
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.connect(("google.com", 80))
print("   ✅ TCP connection established!")
print("   → Your OS now maintains state for this connection")
print("   → Google's server also maintains state for this connection")
print("   → Both sides allocated memory and resources")

time.sleep(2)

# 2. Create UDP socket (no connection state)
print("\n2. Creating UDP socket...")
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("   ✅ UDP socket created!")
print("   → No connection established")
print("   → No state maintained on either side")
print("   → No resources allocated for 'session'")

# 3. Let's see the difference in network tools
print("\n3. Check network connections now...")
print("   Run this command: ss -t | grep google")
print("   You'll see the TCP connection listed")
print("   UDP connections are NOT listed because there's no 'connection'")

tcp_sock.close()
udp_sock.close()

print("\n=== REAL-WORLD ANALOGY ===")
print("TCP = Phone Call:")
print("  • You dial, they answer, conversation established")
print("  • Both parties 'on the line' throughout")
print("  • Resources held (phone line, attention)")
print("  • 'Connection' exists until someone hangs up")

print("\nUDP = Sending Letters:")
print("  • You write letter, drop in mailbox")
print("  • No 'conversation' established")
print("  • No resources held between letters")
print("  • Each letter is independent")

print("\n📬 THE POSTAL SERVICE (physical medium) exists in both cases!")
print("📞 The difference is whether you establish a 'conversation'")
