import socket
import time
from random import random


def get_num_players(conn, addr):
    conn.send("Please enter the number of players (2-5): ".encode())
    num_players = conn.recv(1024).decode().strip()
    while not num_players.isdigit() or int(num_players) < 2 or int(num_players) > 5:
        conn.send("Invalid input. Please enter a number between 2 and 5: ".encode())
        num_players = conn.recv(1024).decode().strip()
    print(f"{addr} has chosen to play with {num_players} players.")
    return int(num_players)


def get_username(conn, addr, player_num):
    conn.send(f"Please enter your username for Player {player_num}: ".encode())
    username = conn.recv(1024).decode().strip()
    while not username:
        conn.send("Invalid input. Please enter a username: ".encode())
        username = conn.recv(1024).decode().strip()
    print(f"{addr} has chosen the username '{username}' for Player {player_num}.")
    return username


def announce_new_player(conn_list, new_player_username):
    for conn in conn_list:
        conn.send(f"{new_player_username} has joined the game.".encode())


def send_countdown(conn_list):
    for conn in conn_list:
        conn.send(f"The game will start in 3 seconds.".encode())
        time.sleep(1)

    for i in range(3, 0, -1):
        for conn in conn_list:
            conn.send(f"{i}...".encode())
            time.sleep(1)


def run_server():
    host = ""
    port = 9999
    backlog = 5
    player_num = 1
    ready_players = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(backlog)
        print(f"Server listening on {host}:{port}...")
        conn_list = []
        num_rounds = 3
        final_scores = {}
        num_players = 0
        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            conn_list.append(conn)

            if num_players == 0:
                num_players = get_num_players(conn, addr)
                conn.send(f"You are Player {player_num}. There will be {num_players} players in this game.".encode())
            else:
                username = get_username(conn, addr, player_num)
                announce_new_player(conn_list, username)
                conn.send(f"You are Player {player_num}. There will be {num_players} players in this game.".encode())

            player_num += 1
            if player_num > num_players:
                break

        print(f"All players connected. Game starting with {num_players} players.")

        for round_num in range(1, num_rounds + 1):

            for conn in conn_list:
                conn.send(
                    f"Game starting with {num_players} players. Send 'ready' when you're ready to start.".encode())

            while ready_players < num_players:
                conn, addr = s.accept()
                message = conn.recv(1024).decode().strip()
                if message.lower() == "ready":
                    ready_players += 1

            print(f"All players are ready.")

            print(f"Round {round_num} starting...")

            send_countdown(conn_list)

            random.seed(time.time_ns())
            number = random.randint(0, 9)

            # send the number to all clients
            for conn in conn_list:
                conn.send(f"The number is: {number}".encode())

            # start the timer for all clients
            start_time = time.time()
            rtt_list = []
            while time.time() - start_time < 3:
                # receive the numbers entered by clients and check if they match the sent number
                for conn in conn_list:
                    try:
                        received_data = conn.recv(1024).decode().strip()
                        if int(received_data) != number:
                            conn.close()
                            conn_list.remove(conn)
                        else:
                            rtt = time.time() - start_time
                            rtt_list.append((conn.getpeername()[0], rtt))
                    except:
                        pass

            # sort the RTT list in ascending order
            sorted_rtt = sorted(rtt_list)

            # determine the winner
            winner_rtt = sorted_rtt[0]
            winner_index = rtt_list.index(winner_rtt)
            winner_conn = conn_list[winner_index]

            for rtt in rtt_list:
                conn_ip = rtt[0]
                rtt_time = rtt[1]
                if conn_ip not in final_scores:
                    final_scores[conn_ip] = [rtt_time]
                else:
                    final_scores[conn_ip].append(rtt_time)

                # existing code to clear the connection list and ready players for the next round
            conn_list.clear()
            ready_players = 0

    final_scores_list = []
    for conn_ip, scores in final_scores.items():
        total_score = sum(scores)
        final_scores_list.append((conn_ip, total_score))
    final_scores_list = sorted(final_scores_list, key=lambda x: x[1])

    # determine the final winner
    winner_conn_ip = final_scores_list[0][0]
    winner_score = final_scores_list[0][1]
    winner_conn = None
    for conn in conn_list:
        if conn.getpeername()[0] == winner_conn_ip:
            winner_conn = conn

    # send message to the final winner
    winner_message = f"Congratulations! You won the game with a total score of {winner_score:.3f} seconds!"
    winner_conn.send(winner_message.encode())

    # send message to other players with their total scores and ranks
    for i, conn in enumerate(conn_list):
        if conn.getpeername()[0] != winner_conn_ip:
            conn_ip = conn.getpeername()[0]
            total_score = sum(final_scores[conn_ip])
            rank = final_scores_list.index((conn_ip, total_score)) + 1
            message = f"You finished in {rank} place with a total score of {total_score:.3f} seconds."
            conn.send(message.encode())


if __name__ == "__main__":
    run_server()
