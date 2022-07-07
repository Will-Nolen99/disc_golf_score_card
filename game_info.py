from random import randint


class Player:
    def __init__(self, name, basket_count):
        self.name = name
        self.scores = [0 for _ in range(basket_count)]


class Course:
    def __init__(self, name, basket_count):
        self.name = name
        self.basket_count = basket_count
        self.pars = [3 for _ in range(basket_count)]

    def set_par(self, par, hole):
        self.pars[hole] = par


class Game:
    def __init__(self, course, player_count):
        self.course = course
        self.player_count = player_count
        self.players = []
        self.current_hole = 1
