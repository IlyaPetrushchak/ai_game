import os
import time
from random import randint, choice
import numpy as np
from art import tprint


def clear():
    os.system("cls" if os.name == "nt" else "clear")


size = 10
actions = ["w", "s", "a", "d"]
q_table = np.zeros((size, size, len(actions)))


alpha = 0.1
gamma = 0.9
epsilon = 0.3

treasure_sum = 0


def reset_game():
    global \
        treasure_x, \
        treasure_y, \
        player_x, \
        player_y, \
        pit_x, \
        pit_y, \
        pit_two_x, \
        pit_two_y, \
        min_pit_x, \
        min_pit_y, \
        field
    field = [["#" for _ in range(size)] for _ in range(size)]
    treasure_x, treasure_y = randint(0, size - 1), randint(0, size - 1)
    player_x, player_y = 4, 4
    pit_x, pit_y = 4, 3
    pit_two_x, pit_two_y = 7, 5
    min_pit_x, min_pit_y = 2, 8
    field[player_x][player_y] = "X"
    field[treasure_x][treasure_y] = "$"
    field[pit_x][pit_y] = "@"
    field[pit_two_x][pit_two_y] = "@"
    field[min_pit_x][min_pit_y] = "&"


def print_field():
    for row in field:
        print(" ".join(row))


def regenerate_treasure():
    global treasure_x, treasure_y
    while True:
        new_x, new_y = randint(0, size - 1), randint(0, size - 1)
        if (new_x, new_y) != (player_x, player_y):
            treasure_x, treasure_y = new_x, new_y
            field[treasure_x][treasure_y] = "$"
            break


def choose_action(state):
    if np.random.uniform(0, 1) < epsilon:
        return choice(range(len(actions)))
    else:
        return np.argmax(q_table[state[0], state[1]])


def take_action(action):
    global player_x, player_y
    if actions[action] == "w" and player_x > 0:
        player_x -= 1
    elif actions[action] == "s" and player_x < size - 1:
        player_x += 1
    elif actions[action] == "a" and player_y > 0:
        player_y -= 1
    elif actions[action] == "d" and player_y < size - 1:
        player_y += 1


def update_field():
    global field
    field = [["#" for _ in range(size)] for _ in range(size)]
    field[player_x][player_y] = "X"
    field[treasure_x][treasure_y] = "$"
    field[pit_x][pit_y] = "@"
    field[pit_two_x][pit_two_y] = "@"
    field[min_pit_x][min_pit_y] = "&"
    tprint("MY-GAME-WITH-AI")


episodes = 1000

for episode in range(episodes):
    reset_game()
    steps = 0

    while True:
        clear()
        print_field()
        state = (player_x, player_y)

        action = choose_action(state)
        old_player_x, old_player_y = player_x, player_y
        take_action(action)
        update_field()

        if (player_x, player_y) == (treasure_x, treasure_y):
            reward = 10
            regenerate_treasure()
            treasure_sum += 1
        else:
            reward = -1

        if (player_x, player_y) == (pit_x, pit_y):
            reward = -5
            reset_game()
        elif (player_x, player_y) == (pit_two_x, pit_two_y):
            reward = -5
            reset_game()
        elif (player_x, player_y) == (min_pit_x, min_pit_y):
            reward = -2

        old_q_value = q_table[old_player_x, old_player_y, action]
        next_max = np.max(q_table[player_x, player_y])
        q_table[old_player_x, old_player_y, action] = old_q_value + alpha * (
            reward + gamma * next_max - old_q_value
        )

        steps += 1
        time.sleep(0.2)

        if steps > 50 or treasure_sum == 10:
            break

    treasure_sum = 0
    time.sleep(1)
