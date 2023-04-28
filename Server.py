import socket
import time
import random
import threading

def random_number_generator():
    random.seed(time.time())
    return random.randint(0, 9)

def send_message(client_socket, message):
    client_socket.send(message.encode())

def handle_client(client_socket, username, username1, other_client, number):
    while True:
        data = client_socket.recv(1024).decode().strip()
        data1 = other_client.recv(1024).decode().strip()
        if data == data1:
            print(f"{username} and {username1} are ready to play!")
            countdown_threads = []

            for i in range(3, 0, -1):
                countdown = str(i)
                print(countdown)

                # Create a thread for each client to send the countdown message
                t1 = threading.Thread(target=send_message, args=(client_socket, countdown))
                t2 = threading.Thread(target=send_message, args=(other_client, countdown))

                t1.start()
                t2.start()

                countdown_threads.append(t1)
                countdown_threads.append(t2)

                time.sleep(1)

            # Wait for all countdown threads to finish before sending the number
            for thread in countdown_threads:
                thread.join()

            message = f"Number is: {number}"

            # Send the number to both clients
            send_message(client_socket, message)
            send_message(other_client, message)

    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 12345
server_socket.bind((host, port))
server_socket.listen(2)
print("Server is listening for incoming connections...")
connections = 0
usernames = []
clients = []

while True:
    if connections == 0:
        conn1, addr1 = server_socket.accept()
        clients.append(conn1)
        connections += 1
        conn1.send("Please enter a username: ".encode())
        username1 = conn1.recv(1024).decode().strip()
        usernames.append(username1)
        conn1.send(f"Welcome {usernames[0]}! Kindly wait for another player to join the game.".encode())
    elif connections == 1:
        conn2, addr2 = server_socket.accept()
        clients.append(conn2)
        connections += 1
        conn2.send("Please enter a username: ".encode())
        username2 = conn2.recv(1024).decode().strip()
        usernames.append(username2)
        conn2.send(f"Welcome {usernames[1]}! You will be playing against {usernames[0]}.".encode())
        conn1.send(f"{usernames[1]} joined the game!".encode())

        print(f"Connected with {usernames[0]} on {addr1} and {usernames[1]} on {addr2}")
        number = random_number_generator()

        # Send the "ready" message to both clients
        send_message(conn1, "Send 'ready' to start the game: ")
        send_message(conn2, "Send 'ready' to start the game: ")

        t1 = threading.Thread(target=handle_client, args=(conn1, username1, username2, conn2, number))
        t1.start()
