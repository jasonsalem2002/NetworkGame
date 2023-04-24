import socket, datetime, threading

# create socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# connect to the server
port = 12345
client_socket.connect((host, port))

def get_user_input():
    while True:
        message = input()
        client_socket.send(message.encode())

i = 0
while True:

    if i == 0:

        warning = client_socket.recv(1024).decode()

        if warning == "Sorry server is at capacity":
            print(warning)
            client_socket.close()
            break

        else:
            username = input(warning)
            client_socket.send(str(username).encode())
            i += 1
            # Start the user input thread
            user_input_thread = threading.Thread(target=get_user_input)
            user_input_thread.start()
            continue

    else:
        mes = client_socket.recv(1024).decode()
        print(mes)
