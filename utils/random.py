from random import randint


def random_int(number):
    percent = randint(1, 100) / 100
    return number * percent
