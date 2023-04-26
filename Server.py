import socket, time, random, threading

def random_number_generator():
    random.seed(time.time())
    return random.randint(0, 9)

def handle_client(client_socket, username, username1, other_client, number):
    while True:
        data = client_socket.recv(1024).decode().strip()
        data1 = other_client.recv(1024).decode().strip()
        if data == data1:
            print(f"{username} and {username1} are ready to play!")
            for i in range(3, 0, -1):
                print(i)
                client_socket.send(str(i).encode())
                other_client.send(str(i).encode())
                time.sleep(1)
            client_socket.send(f"Number is: {number}".encode())
            # client_socket.recv(1024).decode.strip()
            
    #         add a way to ready number from both clients, find a way to check if wrong then connection is closed with message
    #         compute rtt using precise timing 
    #   do it in a loop 3 times to ensure that only 3 rounds
            
            
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

    elif connections ==1:
        conn2, addr2 = server_socket.accept()
        clients.append(conn2)
        connections += 1
        conn2.send("Please enter a username: ".encode())
        username2 = conn2.recv(1024).decode().strip()
        usernames.append(username2)
        conn2.send(f"Welcome {usernames[1]}! You will be playing against {usernames[0]}.".encode())
        conn1.send(f"{usernames[1]} joined the game!".encode())

        print(f"Connected with {usernames[0]} on " + str(addr1) + f" and {usernames[1]} on " + str(addr2))
        number = random_number_generator()

        for client in clients:
            t = threading.Thread(target=client.sendall, args=(f"Send 'ready' to start the game: ".encode(),))
            t.start()

        # Start a thread to handle each client
        t1 = threading.Thread(target=handle_client, args=(conn1, username1, username2, conn2, number))
        t1.start()
        t2 = threading.Thread(target=handle_client, args=(conn2, username2, username1, conn1, number))
        t2.start()

        # Wait for both threads to finish
        t1.join()
        t2.join()
        break
