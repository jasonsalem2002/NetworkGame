import socket

host = '127.0.0.1'  # Localhost
port = 8080
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
print("Connected to the server.")

while True:

    prompt = client_socket.recv(1024).decode()

    if prompt == "Maximum number of connections reached. Disconnecting.":
        print(prompt, end=' ')
        client_socket.close()
        break

    if prompt == "Enter the maximum number of connections allowed: ":
        print(prompt, end=' ')
        max_connections = int(input())
        client_socket.send(str(max_connections).encode())
        prompt_username0 = client_socket.recv(1024).decode()
        print(prompt_username0, end=' ')
        user0 = input()
        client_socket.send(user0.encode())
        if user0:
            while True:
                ready = client_socket.recv(1024).decode()
                if ready == "Game will soon begin!":
                    print(ready)
                    while True:
                        countdown = client_socket.recv(1024).decode()
                        print(countdown)
                        if "Number" in countdown:
                            send_number = int(input("Enter the number: "))
                            client_socket.send(str(send_number).encode())
                    client_socket.close()
                    break
                print(ready, end=' ')
                is_ready = input()
                client_socket.send(is_ready.encode())
            break

    elif prompt == "Please enter your username: ":
        print(prompt, end=' ')
        user = input()
        client_socket.send(user.encode())
        if user:
            while True:
                ready = client_socket.recv(1024).decode()
                if ready == "Game will soon begin!":
                    print(ready)
                    while True:
                        countdown = client_socket.recv(1024).decode()
                        print(countdown)
                        if "Number" in countdown:
                            send_number = int(input("Enter the number: "))
                            client_socket.send(str(send_number).encode())
                    client_socket.close()
                    break
                print(ready, end=' ')
                is_ready = input()
                client_socket.send(is_ready.encode())
            break


