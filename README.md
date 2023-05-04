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

# Server Code

The server code consists of several functions and a main function that starts the server.

## Main Function (`start_server()`)
The `start_server()` function is the entry point of the server program. It sets up the server socket, listens for client connections, and handles each client connection in a separate thread using the `handle_client()` function.

## Client Connection Handling (`handle_client()`)
The `handle_client()` function is responsible for handling a client connection. It receives the client socket as a parameter and performs the following tasks:

- If the maximum number of connections is not set (`max_connections == 0`), it prompts the client to enter the maximum number of connections allowed and the username. It checks if the client is ready to start the game and adds the client to the list of connected clients.
- If the maximum number of connections is reached (`len(connected_clients) >= max_connections`), it informs the client and disconnects the client.
- If the last player joined (`len(connected_clients) == (max_connections - 1)`), it prompts the last player to enter their username, checks if the client is ready, and increments the `lastclient` variable.
- For all other players, it prompts the client to enter their username, checks if the client is ready, and adds the client to the list of connected clients.
- If the last player is ready, it starts the countdown and sends the generated number to all clients.
- For each round, it checks the client's response, calculates the round trip time (RTT), checks if the received number matches the expected number, and determines the winner with the minimum RTT. It handles multiple rounds of the game based on the number of connected clients.

## Other Helper Functions
- `checking()`: This function checks the client's response, calculates the round trip time (RTT), and determines the winner with the minimum RTT for each round.
- `remove_client()`: This function removes a client from the list of connected clients.
- `random_number_generator()`: This function generates a random number between 0 and 9.
- `is_ready()`: This function checks if the client is ready to start the game by sending a prompt and receiving the client's response.
- `countdown()`: This function starts the countdown before the game starts by sending countdown prompts to all clients.
- `countdownSocket()`: This function starts the countdown before the game starts for individual sockets.
- `send_number()`: This function sends the generated number to all clients.

# Client Code

The client code connects to the server and allows the user to participate in the number guessing game.

## Connection and Prompt Handling
The client code starts by creating a socket and connecting to the server using the specified host and port.

The client then enters a loop where it receives prompts from the server and handles them accordingly. There are two types of prompts:

- Maximum number of connections prompt: If the server prompts the client to enter the maximum number of connections allowed, the client reads the input from the user and sends it to the server. The client also enters a username and sends it to the server.
- Username prompt: If the server prompts the client to enter a username, the client reads the input from the user and sends it to the server.

# Game Rounds

After the countdown, the game begins with multiple rounds. Each round consists of the following steps:

## Round 1

1. The server sends a message to all clients indicating that it's the first round.
2. Clients send their readiness for the round to the server.
3. Once all clients are ready, the server starts a countdown specific to the round.
4. The server generates a random number using the `random_number_generator()` function.
5. The server sends the generated number to all clients with a 5-second time limit to send their number.
6. Clients enter their numbers and send them to the server.
7. The server receives the numbers, checks if they match the generated number, and calculates the round trip time (RTT).
8. If a client's number matches the generated number, their username and RTT are added to the `temp_RTT` list.
9. The server determines the winner of the round based on the minimum RTT from the `temp_RTT` list.
10. The winner's username is added to the `round_winners` list.
11. Duplicate winners are removed from the `round_winners` list.
12. The server sends the winner's username to all clients.

## Round 2

1. The server sends a message to all clients indicating that it's the second round.
2. Clients send their readiness for the round to the server.
3. Once all clients are ready, the server starts a countdown specific to the round.
4. The server generates a new random number for round 2.
5. The server sends the generated number to all clients with a 5-second time limit to send their number.
6. Clients enter their numbers and send them to the server.
7. The server receives the numbers, checks if they match the generated number, and calculates the RTT.
8. If a client's number matches the generated number, their username and RTT are added to the `temp_RTT` list.
9. The server determines the winner of round 2 based on the minimum RTT from the `temp_RTT` list.
10. The winner's username is added to the `round_winners` list.
11. Duplicate winners are removed from the `round_winners` list.
12. The server sends the winner's username to all clients.

## Round 3

1. The server sends a message to all clients indicating that it's the third round.
2. Clients send their readiness for the round to the server.
3. Once all clients are ready, the server starts a countdown specific to the round.
4. The server generates a new random number for round 3.
5. The server sends the generated number to all clients with a 5-second time limit to send their number.
6. Clients enter their numbers and send them to the server.
7. The server receives the numbers, checks if they match the generated number, and calculates the RTT.
8. If a client's number matches the generated number, their username and RTT are added to the `temp_RTT` list.
9. The server determines the winner of round 3 based on the minimum RTT from the `temp_RTT` list.
10. The winner's username is added to the `round_winners` list.
11. Duplicate winners are removed from the `round_winners` list.
12. The server sends the winner's username to all clients.

After the third round, the server announces the winner of the game based on the results of all three rounds.

## Conclusion

The provided server and client code implements a multiplayer number-guessing game. The server manages the connections, handles
