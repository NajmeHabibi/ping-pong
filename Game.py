#najme habibi 9512762130
import random
class Map:
    list_move = [[1, 1], [1, -1], [-1, 1], [-1, -1]]

    def __init__(self):
        self.player1 = Player("A", 0)
        self.player2 = Player("B", 0)
        self.mid = [
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
            "|                                                                                       |",
            "|                                          O                                            |",
            "|                                                                                       |",
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
        ]
        self.ball = Ball()
        self.right_rocket = Rocket([88, 8])
        self.left_rocket = Rocket([0, 8])
        self.move_d = self.list_move[random.choice([0, 1, 2, 3])]

    def reset(self):
        self.player1 = Player("A", 0)
        self.player2 = Player("B", 0)
        self.mid = [
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
            "|                                                                                       |",
            "|                                          O                                            |",
            "|                                                                                       |",
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
            "                                                                                         ",
        ]
        self.ball = Ball()
        self.right_rocket = Rocket([88, 8])
        self.left_rocket = Rocket([0, 8])
        self.move_d = self.list_move[random.choice([0, 1, 2, 3])]

    def move_ball(self):
        left_y = self.left_rocket.coordiante[1]
        right_y = self.right_rocket.coordiante[1]
        left_coor = [left_y - 1, left_y, left_y + 1]
        right_coor = [right_y - 1, right_y, right_y + 1]

        x, y = self.ball.coordinate
        mx, my = self.move_d
        newx = mx + x
        newy = my + y
        if newy == 0:
            self.move_d = [mx, -my]
        if newy == 16:
            self.move_d = [mx, -my]
        if newx == 0:
            if newy in left_coor:
                self.move_d = [-mx, my]

            else:
                newx, newy = [44, 8]
                self.move_d = self.list_move[random.choice([0, 1, 2, 3])]
                self.player2.score += 1
        if newx == 89:
            if newy in right_coor:
                self.move_d = [-mx, my]
            else:
                newx, newy = [44, 8]
                self.move_d = self.list_move[random.choice([0, 1, 2, 3])]
                self.player1.score += 1
        self.ball.coordinate = [newx, newy]

class Player:

    def __init__(self, player_name, score):
        self.name = player_name
        self.score = score


class Rocket:

    def __init__(self, coordinate):
        self.coordiante = coordinate

    def move(self, side):
        if side == 'up':
            value = self.coordiante[1] - 1
            if value > 0:
                self.coordiante[1] = value
        else:
            value = self.coordiante[1] + 1
            if value < 16:
                self.coordiante[1] = value



class Ball:
    def __init__(self):
        self.coordinate = [44, 8]



