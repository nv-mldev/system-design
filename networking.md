# Networking Essentials for System Design

This document provides a summary of key networking concepts that are essential for system design interviews, based on the provided video transcript.

## The OSI Model and Networking Basics

Networking is often conceptualized as a layered cake, where each layer provides a level of abstraction and builds upon the one below it. For system design interviews, we are primarily concerned with three of these layers:

*   **Layer 3: The Network Layer:** This is where protocols like **IP** (Internet Protocol) live. It's responsible for addressing and routing packets across the network.
*   **Layer 4: The Transport Layer:** This layer includes protocols like **TCP** and **UDP**, which provide services like guaranteed delivery and ordering.
*   **Layer 7: The Application Layer:** This is the top layer, featuring protocols that developers interact with directly, such as **HTTP**, **WebSockets**, and **gRPC**.

These layers work together. For example, an HTTP request (Layer 7) is transmitted over a TCP connection (Layer 4), which in turn uses IP addresses (Layer 3) to route the data. This layering creates overhead and latency, especially during connection setup (e.g., the TCP three-way handshake), which is an important consideration in system design.

## Layer 3: The Network Layer (IP)

The **Internet Protocol (IP)** is responsible for giving usable names (addresses) to nodes on a network and allowing for routing.

*   **IPv4 vs. IPv6:**
    *   **IPv4:** 4-byte addresses. We have run out of these.
    *   **IPv6:** 16-byte addresses. More modern and plentiful.
    *   Typically, you'll use IPv4 for external-facing services for compatibility and IPv6 internally.

*   **Public vs. Private IP Addresses:**
    *   **Public IPs:** Globally unique and routable on the public internet. Assigned by a central authority. Used for your API gateways, load balancers, and other externally facing components.
    *   **Private IPs:** Used within a private network (e.g., your home network or a VPC in the cloud). Not routable on the public internet. Used for all your internal microservices and hosts.

## Layer 4: The Transport Layer (TCP, UDP, QUIC)

The transport layer provides important functionality on top of IP.

*   **TCP (Transmission Control Protocol):**
    *   The **default** choice for most applications.
    *   Provides **guaranteed delivery** and **ordering** of packets using sequence numbers and acknowledgements.
    *   It's reliable, but this reliability comes at the cost of higher latency and lower throughput, as lost packets must be retransmitted.

*   **UDP (User Datagram Protocol):**
    *   Offers higher performance (lower latency, higher throughput) by sacrificing the guarantees of TCP.
    *   It's a "fire and forget" protocol. Packets can be lost or arrive out of order.
    *   **Use cases:** Real-time applications where latency is critical and some data loss is acceptable, such as:
        *   Video and audio conferencing
        *   Multiplayer gaming
        *   Live streaming

*   **QUIC:** A more modern transport protocol built on top of UDP that aims to provide the reliability of TCP with lower latency. It's increasingly used for web traffic.

## Layer 7: The Application Layer

This is where most of the application-level logic and protocols reside.

### HTTP and REST

*   **HTTP (Hypertext Transfer Protocol):** The most popular application layer protocol. It uses a simple text-based request/response model.
    *   **Requests** include a method (verb) like `GET`, `POST`, `PUT`, `DELETE`, a URL, and headers.
    *   **Responses** include a status code (e.g., `200 OK`, `404 Not Found`), headers, and a body.
    *   **Content Negotiation:** Clients and servers use headers to negotiate content types, encodings, etc., which makes HTTP highly flexible and extensible.

*   **REST (Representational State Transfer):** The most common architectural style for building APIs on top of HTTP.
    *   It's organized around **resources** (identified by URLs) and **verbs** (HTTP methods).
    *   Example: To get user 1, you would make a `GET` request to `/users/1`. To create a new user, you would `POST` to `/users`.
    *   REST is the default choice for building APIs in system design interviews due to its simplicity, scalability, and wide adoption.

### GraphQL

GraphQL is a query language for APIs that provides an alternative to REST.

*   **Problem it solves:**
    *   **Under-fetching:** When a single API endpoint doesn't provide enough data, requiring the client to make multiple requests.
    *   **Over-fetching:** When an endpoint returns more data than the client needs.
*   **How it works:** The client sends a single query specifying the exact shape of the data it needs, and the server returns a JSON object matching that shape.
*   **Use cases:**
    *   When the frontend is changing rapidly or has complex data requirements (e.g., news feeds).
    *   When you need to aggregate data from multiple backend services.

### gRPC (Google Remote Procedure Call)

gRPC is a high-performance RPC framework.

*   **How it works:**
    *   Uses **Protocol Buffers (Protobufs)** as its schema definition language and serialization format. Protobufs are a highly efficient binary format.
    *   Defines services and messages in `.proto` files, which can be compiled into client and server stubs in many languages.
*   **Advantages:**
    *   **High performance:** Can be up to 10x faster than REST/JSON due to efficient binary serialization.
    *   **Features:** Supports client-side load balancing, streaming, and authentication.
*   **Disadvantages:**
    *   Not natively supported by web browsers.
    *   Binary format is harder to debug than human-readable JSON.
*   **Use cases:** Primarily for **internal microservice communication** where performance is critical. A common pattern is to have an external-facing REST API that communicates with internal gRPC services.

### Server-Sent Events (SSE)

SSE is a standard that allows a server to push data to a client over a standard HTTP connection.

*   **How it works:** The client makes a regular HTTP request, but the server keeps the connection open and sends events as they become available, separated by newlines.
*   **Characteristics:**
    *   **Unidirectional:** Server-to-client push only.
    *   Built on HTTP, so it works with existing infrastructure.
    *   Connections can be unreliable and are often terminated by proxies after 30-60 seconds, but clients can automatically reconnect, passing the ID of the last event received.
*   **Use cases:**
    *   Short-lived updates to a UI (e.g., status of a background job).
    *   Streaming AI responses (tokens) back to a user.

### WebSockets

WebSockets provide a **full-duplex (bidirectional)** communication channel over a single, long-lived TCP connection.

*   **How it works:** It starts with an HTTP "Upgrade" request and then transitions to a raw TCP-like connection for sending binary or text messages.
*   **Characteristics:**
    *   Low latency, high frequency, bidirectional communication.
    *   **Stateful:** Requires managing persistent connections, which adds complexity for deployments and failure handling.
*   **Use cases:**
    *   Real-time applications requiring two-way communication:
        *   Chat applications
        *   Multiplayer games
        *   Live collaboration tools

### WebRTC (Web Real-Time Communication)

WebRTC is a protocol that enables **peer-to-peer (P2P)** communication directly between browsers, primarily for audio and video.

*   **How it works:** It's complex, involving signaling servers (to coordinate connections), STUN servers (to traverse NATs), and TURN servers (as a fallback). It runs over UDP.
*   **Use cases:**
    *   Audio and video calling.
    *   Collaborative editors (often using CRDTs - Conflict-free Replicated Data Types).
*   **Interview advice:** Avoid bringing it up unless the problem is explicitly about audio/video calling or collaborative editing.

## Load Balancing

When scaling horizontally (adding more servers), you need a way to distribute traffic among them.

*   **Client-Side Load Balancing:**
    *   The client is aware of all available servers (e.g., from a service registry) and chooses one to connect to directly.
    *   **Pros:** No extra hop, lower latency.
    *   **Cons:** Clients need to be updated when servers change; less sophisticated balancing algorithms.
    *   **Use cases:** Internal microservices (gRPC supports this natively), DNS.

*   **Dedicated Load Balancer (Appliance):**
    *   A centralized server (hardware or software) that sits between clients and servers.
    *   **Layer 4 (Transport Layer):** Operates at the TCP/UDP level. It forwards packets without inspecting their content. Very high performance. Use for stateful connections like WebSockets.
    *   **Layer 7 (Application Layer):** Operates at the HTTP level. It can inspect requests and make routing decisions based on URL, headers, etc. More flexible and feature-rich, but slightly lower performance. This is the default choice for most web applications.
    *   **Algorithms:** Round Robin, Random, Least Connections.

## Deep Dives

### Regionalization and CDNs

*   **Problem:** The speed of light imposes a hard limit on latency for global applications (e.g., ~80ms between London and New York).
*   **Solution:**
    1.  **Partition your system:** If possible, partition users and data by region (e.g., Uber riders and drivers are in the same city).
    2.  **Collocate data and processing:** Keep your web servers and databases in the same region to minimize back-and-forth latency.
    3.  **Replicate data:** For read-heavy workloads, replicate data across regions so reads are fast, but accept that there will be a replication lag.
    4.  **Use a CDN (Content Delivery Network):** A CDN is a network of edge servers distributed globally. It caches static content (images, videos, JS, CSS) and serves it from a location close to the user, dramatically reducing latency.

### Failures, Timeouts, and Retries

*   **Timeouts:** Always set a sensible timeout on any network request to avoid clients waiting forever.
*   **Retries:** When a request fails, it's common to retry. However, a naive retry strategy can make a bad situation worse.
*   **The Gold Standard:** **Retries with exponential backoff and jitter.**
    *   **Exponential Backoff:** Increase the delay between retries exponentially (e.g., 1s, 2s, 4s, 8s). This gives a struggling service time to recover.
    *   **Jitter:** Add a small, random amount of time to each delay. This prevents a "thundering herd" problem where many clients retry at the exact same time.

### Cascading Failures and Circuit Breakers

*   **Cascading Failure:** A failure in one part of a system (e.g., a slow database) causes failures in upstream services, which in turn cause failures in their upstream services, leading to a system-wide outage. Retries can often exacerbate this.
*   **Circuit Breaker Pattern:** A mechanism to prevent cascading failures.
    *   **How it works:** An intermediary object monitors for failures. If the failure rate for a downstream service exceeds a threshold, the circuit breaker "trips" or "opens."
    *   While the circuit is open, all subsequent calls to the failing service fail immediately without even making a network request. This gives the downstream service a chance to recover.
    *   Periodically, the circuit breaker will enter a "half-open" state and allow a single request through. If it succeeds, the circuit closes and normal operation resumes. If it fails, the circuit remains open.
