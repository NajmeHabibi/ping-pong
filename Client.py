import socket
import time
import curses
import sys
import json


class Player:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((socket.gethostname(), 8080))
        self.player = sys.argv[1]
        self.mid = [
            "                                                                                         \n",
            "                                                                                         \n",
            "                                                                                         \n",
            "                                                                                         \n",
            "                                                                                         \n",
            "                                                                                         \n",
            "                                                                                         \n",
            "                                                                                         \n",
            "                                                                                         \n",
            "                                                                                         \n",
            "                                                                                         \n",
            "                                                                                         \n",
            "                                                                                         \n",
            "                                                                                         \n",
            "                                                                                         \n",
            "                                                                                         \n",
            "                                                                                         \n",
        ]

    def do_it(self, screen):
        curses.curs_set(0)  # Hide the cursor
        screen.nodelay(True)  # Don't block I/O calls
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        screen.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)

        j = 0
        while True:
            msg = self.socket.recv(4096)
            if msg == b'exit':
                sys.exit()

            dic = json.loads(msg)
            screen.erase()
            pre_map = self.mid.copy()
            try:
                screen.addstr("########################################################################################"
                              "##\n")
                left_coor = dic['left_rocket']
                if 0 < left_coor[1] < 16:
                    self.mid[left_coor[1] - 1] = "|" + self.mid[left_coor[1] - 1][1:]
                    self.mid[left_coor[1]] = "|" + self.mid[left_coor[1]][1:]
                    self.mid[left_coor[1] + 1] = "|" + self.mid[left_coor[1] + 1][1:]

                right_coor = dic['right_rocket']
                if 0 < right_coor[1] < 17:
                    self.mid[right_coor[1] - 1] = self.mid[right_coor[1] - 1][:-2] + "|\n"
                    self.mid[right_coor[1]] = self.mid[right_coor[1]][:-2] + "|\n"
                    self.mid[right_coor[1] + 1] = self.mid[right_coor[1] + 1][:-2] + "|\n"

                ball = dic['ball']
                self.mid[ball[1]] = self.mid[ball[1]][:ball[0]] + "O" + self.mid[ball[1]][ball[0] + 1:]

                for i in self.mid:
                    screen.addstr(i)

                self.mid = pre_map
                screen.addstr("######################################################################################"
                              "####" + '\n')
                screen.addstr("Score:\n")
                screen.addstr("Player A                                 {} - {}                                    Play"
                              "er B\n".format(dic['scoreA'], dic['scoreB']))
                screen.addstr("Exit: press 'X' Restart: press 'R'")
            except curses.error:
                pass
            j = j + 1
            a = screen.getch()
            if a == 88:
                self.socket.send(bytes('x', "utf-8"))
                time.sleep(2)
                sys.exit()
            elif a == 82:
                self.socket.send(bytes('r', "utf-8"))
            else:
                if self.player == 'left':
                    if a == 119:  # w
                        self.socket.send(bytes('left,up', "utf-8"))
                    if a == 115:  # s
                        self.socket.send(bytes('left,down', "utf-8"))
                else:
                    if a == curses.KEY_UP:
                        self.socket.send(bytes('right,up', "utf-8"))
                    if a == curses.KEY_DOWN:
                        self.socket.send(bytes('right,down', "utf-8"))
            screen.refresh()
            time.sleep(0.01)


if __name__ == '__main__':
    player1 = Player()
    curses.wrapper(player1.do_it)
