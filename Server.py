import socket, random, time, threading


def random_number_generator():
    random.seed(time.time())
    return random.randint(0, 9)


def is_ready(client_socket, username):
    client_socket.send("Send 'ready' to begin the game".encode())
    while True:
        ready_response = client_socket.recv(1024).decode().strip()
        if ready_response.lower() == "ready":
            client_socket.send("Game will soon begin!".encode())
            print(username, "is ready.")
            break
        else:
            client_socket.send("Invalid input! Send 'ready' to start the game".encode())
    return True


def countdown():
    for i in range(3, 0, -1):
        print(i, end=' ')
        for client_socket in connected_clients:
            client_socket.send(str(i).encode())
        time.sleep(1)

def send_number(number):
    for client_socket in connected_clients:
        client_socket.send(f"Number is: {number}".encode())

    nummm = client_socket.recv(1024).decode().strip()
    print(nummm)

def handle_client(client_socket, number):
    global max_connections, connected_clients, ready_clients

    if max_connections == 0:
        client_socket.send("Enter the maximum number of connections allowed: ".encode())
        max_connections = int(client_socket.recv(1024).decode().strip())
        print("Maximum number of connections set to:", max_connections)
        client_socket.send("Please enter your username: ".encode())
        username = client_socket.recv(1024).decode().strip()
        print(f"{username} joined the game!")
        connected_clients.append(client_socket)
        if is_ready(client_socket, username):
            ready_clients.append(username)

    elif len(connected_clients) >= max_connections:
        client_socket.send("Maximum number of connections reached. Disconnecting.".encode())
        print("Server at Capacity, rejecting new connections")
        client_socket.close()
        return

    elif len(connected_clients) == (max_connections - 1):
        print("Last player joined")
        client_socket.send("Please enter your username: ".encode())
        username = client_socket.recv(1024).decode().strip()
        print(f"{username} joined the game!")
        connected_clients.append(client_socket)
        if is_ready(client_socket, username):
            ready_clients.append(username)

    else:
        client_socket.send("Please enter your username: ".encode())
        username = client_socket.recv(1024).decode().strip()
        print(f"{username} joined the game!")
        connected_clients.append(client_socket)
        if is_ready(client_socket, username):
            ready_clients.append(username)


    if len(ready_clients) == max_connections:
        print("All players are ready. Starting the countdown!")
        countdown()
        send_number(number)


def start_server():
    host = '127.0.0.1'
    port = 8080
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    number = random_number_generator()
    print("Server listening on {}:{}".format(host, port))

    while True:
        client_socket, address = server_socket.accept()
        print("Client connected from {}:{}".format(address[0], address[1]))
        client_thread = threading.Thread(target=handle_client, args=(client_socket, number))
        client_thread.start()


connected_clients = []
ready_clients = []
max_connections = 0
start_server()
