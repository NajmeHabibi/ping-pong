import socket
import time
import json
from Game import Map
import threading


class Server:
    max_clients = 2
    time_sleep = 0.1
    start = True
    restart = True

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((socket.gethostname(), 8080))
        self.game_map = Map()
        self.x = {'left_rocket': self.game_map.left_rocket.coordiante,
                  'right_rocket': self.game_map.right_rocket.coordiante,
                  'ball': self.game_map.ball.coordinate,
                  'scoreA': self.game_map.player1.score,
                  'scoreB': self.game_map.player2.score,
                  }

    def start_game(self):
        while self.start:
            self.socket.listen(self.max_clients)
            player1_socket, address_player1 = self.socket.accept()
            print(f"Connection from {address_player1} has been established.")
            player2_socket, address_player2 = self.socket.accept()
            print(f"Connection from {address_player2} has been established.")
            while self.start and self.restart:
                time.sleep(self.time_sleep)
                if self.time_sleep != 0.1:
                    self.time_sleep = 0.1
                self.game_map.move_ball()
                self.x['ball'] = self.game_map.ball.coordinate
                t1 = threading.Thread(target=self.player_socket_def,
                                      args=(player1_socket, player2_socket, address_player1))
                t1.start()
                t2 = threading.Thread(target=self.player_socket_def,
                                      args=(player2_socket, player1_socket, address_player2))
                t2.start()

    def refresh(self):
        self.x['left_rocket'] = self.game_map.left_rocket.coordiante
        self.x['right_rocket'] = self.game_map.right_rocket.coordiante
        self.x['scoreA'] = self.game_map.player1.score
        self.x['scoreB'] = self.game_map.player2.score

    def player_socket_def(self, player_socket, seconde, address):
        if self.start:
            if self.x['scoreB'] == 3 or self.x['scoreA'] == 3:
                # player_socket.send(bytes('end', "utf-8"))
                self.restart = False

            self.refresh()
            y = json.dumps(self.x)
            player_socket.send(bytes(y, "utf-8"))
            msg = player_socket.recv(4096)
            print(msg)
            if msg == b'r':
                self.time_sleep = 5
                self.game_map.reset()
                self.restart = True
                print('r')
            elif msg == b'x':
                self.start = False
                seconde.send(bytes('exit', "utf-8"))
                # player_socket.send(bytes('exit', "utf-8"))
                self.socket.close()
                print('x')
            else:
                a = (str(msg)[2:-1]).split(',')
                if 'right' in a:
                    if 'up' in a:
                        self.game_map.right_rocket.move('up')
                    else:
                        self.game_map.right_rocket.move('down')
                else:
                    if 'up' in a:
                        self.game_map.left_rocket.move('up')
                    else:
                        self.game_map.left_rocket.move('down')


if __name__ == '__main__':
    server = Server()
    server.start_game()
