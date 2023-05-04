# Number Guessing Game - Client-Server Application

This is a simple client-server application for a number guessing game. The server generates a random number between 0 and 9, and the clients compete to guess the number as quickly as possible. The server measures the round trip time (RTT) for each client's guess and declares the winner of each round based on the minimum RTT.

## Getting Started

To run the application, you need to start the server and connect multiple clients to it. Follow the instructions below to set up and run the application.

### Prerequisites

- Python 3.x

### Server

1. Open the server code in a Python editor or IDE.
2. Set the desired values for the `host` and `port` variables in the `start_server()` function.
3. Save the changes and run the server code.

### Client

1. Open the client code in a Python editor or IDE.
2. Set the `host` and `port` variables to match the server's `host` and `port` values.
3. Save the changes and run the client code.

## How It Works

1. The server initializes variables, sets up the server socket, and starts listening for client connections.
2. When a client connects, a new thread is created to handle the client.
3. The server prompts the client to enter a maximum number of connections allowed.
4. The server prompts each client to enter a username and checks if they are ready to start the game.
5. Once the maximum number of connections is reached or all clients are ready, the server starts the countdown.
6. The server generates a random number and sends it to all clients.
7. Each client enters their guess and sends it to the server.
8. The server calculates the round trip time (RTT) for each client's guess and determines the winner of the round.
9. The process repeats for multiple rounds until a winner is declared for the final round.

