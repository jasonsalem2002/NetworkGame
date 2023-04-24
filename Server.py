import socket, time, random


def random_number_generator():
    random.seed(time.time())
    return random.randint(0, 9)


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

    if connections >= 2:
        conn3, addr3 = server_socket.accept()
        conn3.send("Sorry server is at capacity".encode())
        conn3.close()
        print(f"Connection refused for {addr3}")
        continue

    if connections == 0:
        conn1, addr1 = server_socket.accept()
        clients.append(conn1)
        connections += 1
        conn1.send("Please enter a username: ".encode())
        username1 = conn1.recv(1024).decode().strip()
        usernames.append(username1)
        conn1.send(f"Welcome {usernames[0]}! Kindly wait for another player to join the game.".encode())

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
            client.sendall(f"Number is: {number}".encode())

