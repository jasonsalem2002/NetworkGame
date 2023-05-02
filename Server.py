import socket
import random
import time
import threading


def remove_client(client_socket):
    if client_socket in connected_clients:
        connected_clients.remove(client_socket)
    client_socket.close()


def random_number_generator():
    random.seed(time.time())
    return random.randint(0, 9)


def is_ready(client_socket, username):
    client_socket.send("Send 'ready' to begin the game".encode())
    while True:
        try:
            ready_response = client_socket.recv(1024).decode().strip()
            if ready_response.lower() == "ready":
                client_socket.send("Game will soon begin!".encode())
                print(username, "is ready.")
                break
            else:
                client_socket.send("Invalid input! Send 'ready' to start the game".encode())
        except ConnectionResetError:
            print("Connection closed unexpectedly.")
            break
        except Exception as e:
            print("An error occurred:", str(e))
            break
    return True


def countdown():
    for i in range(3, 0, -1):
        print(i, end=' ')
        for client_socket in connected_clients:
            try:
                client_socket.send(str(i).encode())
            except ConnectionResetError:
                print("Connection closed unexpectedly.")
                remove_client(client_socket)
                break
            except Exception as e:
                print("An error occurred:", str(e))
                break
        time.sleep(1)


def send_number(number):
    for client_socket in connected_clients:
        try:
            client_socket.send(f"Number is: {number}, you have 5 seconds to send it!".encode())
        except ConnectionResetError:
            print("Connection closed unexpectedly.")
            remove_client(client_socket)
            break
        except Exception as e:
            print("An error occurred:", str(e))
            break


def handle_client(client_socket, number):
    global max_connections, connected_clients, ready_clients, lastclient, round_winners, temp_RTT

    try:
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
            remove_client(client_socket)
            return

        elif len(connected_clients) == (max_connections - 1):
            print("Last player joined")
            client_socket.send("Please enter your username: ".encode())
            username = client_socket.recv(1024).decode().strip()
            print(f"{username} joined the game!")
            connected_clients.append(client_socket)
            if is_ready(client_socket, username):
                ready_clients.append(username)
            lastclient += 1

        else:
            client_socket.send("Please enter your username: ".encode())
            username = client_socket.recv(1024).decode().strip()
            print(f"{username} joined the game!")
            connected_clients.append(client_socket)
            if is_ready(client_socket, username):
                ready_clients.append(username)

        if lastclient == 1:
            print("All players are ready. Starting the countdown!")
            countdown()
            send_number(number)
            lastclient += 1

        while True:
            if lastclient == 2:
                start_time = time.time()
                data = client_socket.recv(1024).decode()
                end_time = time.time()
                if not data:
                    print("Connection closed by client.")
                    remove_client(client_socket)
                rtt = end_time - start_time
                print(f"Received from {username}: {data} in {rtt} seconds")
                if int(number) == int(data):
                    temp_dic = {username: rtt}
                    temp_RTT.append(temp_dic)
                    print(temp_RTT)
                else:
                    print("Wrong, disqualified")
                time.sleep(5)
                break

        min_data = float('inf')
        min_username = None
        for dictionary in temp_RTT:
            name, roundtrip = list(dictionary.items())[0]
            if roundtrip < min_data:
                min_data = roundtrip
                min_username = name
        print("Username with the lowest data:", min_username)
        round_winners.append({min_username})
        print(round_winners)
        unique_round_winners = []
        for element in round_winners:
            if element not in unique_round_winners:
                unique_round_winners.append(element)
        print(unique_round_winners)

    except ConnectionResetError:
        print("Connection closed unexpectedly.")
        remove_client(client_socket)
    except Exception as e:
        print("An error occurred:", str(e))
        remove_client(client_socket)


def start_server():
    host = '127.0.0.1'
    port = 8080
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    number = random_number_generator()
    print("Server listening on {}:{}".format(host, port))

    try:
        while True:
            client_socket, address = server_socket.accept()
            print("Client connected from {}:{}".format(address[0], address[1]))
            client_thread = threading.Thread(target=handle_client, args=(client_socket, number))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server interrupted by keyboard. Shutting down...")
    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        server_socket.close()


lastclient = 0
connected_clients = []
ready_clients = []
max_connections = 0
round_winners = []
temp_RTT = []
start_server()
