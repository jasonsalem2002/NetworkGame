import socket
import time

host = '127.0.0.1'  # Localhost
port = 8080

# Create a client socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
print("Connected to the server.")

while True:
    # Receive a prompt from the server
    prompt = client_socket.recv(1024).decode()

    if prompt == "Maximum number of connections reached. Disconnecting.":
        # Handle the prompt indicating the maximum number of connections is reached
        print(prompt, end=' ')
        client_socket.close()
        break

    if prompt == "Enter the maximum number of connections allowed: ":
        # Handle the prompt asking for the maximum number of connections
        print(prompt, end=' ')
        max_connections = int(input())
        client_socket.send(str(max_connections).encode())

        # Receive and handle the next prompt asking for a username
        prompt_username0 = client_socket.recv(1024).decode()
        print(prompt_username0, end=' ')
        user0 = input()
        client_socket.send(user0.encode())

        if user0:
            while True:
                # Receive and handle the "ready" prompt indicating the game is about to begin
                ready = client_socket.recv(1024).decode()
                if ready == "Game will soon begin!":
                    print(ready)

                    while True:
                        # Receive and handle the countdown prompt for each round
                        countdown = client_socket.recv(1024).decode()
                        print(countdown)

                        if "Number" in countdown:
                            # Prompt the user to enter a number and send it to the server
                            send_number = input("Enter the number: ")
                            client_socket.send(send_number.encode())

                        elif "Round 2" in countdown:
                            # Prompt the user to indicate readiness for round 2
                            ready2 = input()
                            client_socket.send(ready2.encode())

                            while True:
                                # Receive and handle the countdown prompt for round 2
                                countdown2 = client_socket.recv(1024).decode()
                                print(countdown2)

                                if "Number" in countdown2:
                                    # Prompt the user to enter a number for round 2 and send it to the server
                                    send_number2 = input("Enter the number: ")
                                    client_socket.send(send_number2.encode())
                                    break

                        elif "Round 3" in countdown:
                            # Prompt the user to indicate readiness for round 3
                            ready3 = input()
                            client_socket.send(ready3.encode())

                            while True:
                                # Receive and handle the countdown prompt for round 3
                                countdown3 = client_socket.recv(1024).decode()
                                print(countdown3)

                                if "Number" in countdown3:
                                    # Prompt the user to enter a number for round 3 and send it to the server
                                    send_number3 = input("Enter the number: ")
                                    client_socket.send(send_number3.encode())
                                    print("game over")

                    client_socket.close()
                    break

                print(ready, end=' ')
                is_ready = input()
                client_socket.send(is_ready.encode())
            break

    elif prompt == "Please enter your username: ":
        # Handle the prompt asking for a username
        print(prompt, end=' ')
        user = input()
        client_socket.send(user.encode())

        if user:
            while True:
                # Receive and handle the "ready" prompt indicating the game is about to begin
                ready = client_socket.recv(1024).decode()
                if ready == "Game will soon begin!":
                    print(ready)
                    while True:
                        # Receive and handle the countdown prompt for each round
                        countdown = client_socket.recv(1024).decode()
                        print(countdown)

                        if "Number" in countdown:
                            # Prompt the user to enter a number and send it to the server
                            send_number = input("Enter the number: ")
                            client_socket.send(send_number.encode())

                        elif "Round 2" in countdown:
                            # Prompt the user to indicate readiness for round 2
                            ready2 = input()
                            client_socket.send(ready2.encode())

                            while True:
                                # Receive and handle the countdown prompt for round 2
                                countdown2 = client_socket.recv(1024).decode()
                                print(countdown2)

                                if "Number" in countdown2:
                                    # Prompt the user to enter a number for round 2 and send it to the server
                                    send_number2 = input("Enter the number: ")
                                    client_socket.send(send_number2.encode())
                                    break

                        elif "Round 3" in countdown:
                            # Prompt the user to indicate readiness for round 3
                            ready3 = input()
                            client_socket.send(ready3.encode())

                            while True:
                                # Receive and handle the countdown prompt for round 3
                                countdown3 = client_socket.recv(1024).decode()
                                print(countdown3)

                                if "Number" in countdown3:
                                    # Prompt the user to enter a number for round 3 and send it to the server
                                    send_number3 = input("Enter the number: ")
                                    client_socket.send(send_number3.encode())
                                    print("game over")

                    client_socket.close()
                    break

                print(ready, end=' ')
                is_ready = input()
                client_socket.send(is_ready.encode())
            break

