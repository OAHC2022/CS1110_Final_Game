#zh2wc ml6vq
import pygame
import gamebox
import math
import numpy as np


direction = ["up", "down", "left", "right"]
current_direction = "up"
food_exist = False
change_d_coordinate = [400, 300]  # the coordinate which the key is pressed
previous_key = ["up", "up"]  # to record the movement and where to turn
snake_speed = 5


def snake_generator():
    """
    generate the snake using linked list
    snake_head is the beginning
    snake_tail is the end
    :return:
    """
    global snake_head
    global snake_tail
    global body
    if current_direction == "up":
        body = gamebox.from_color(snake_tail.x, snake_tail.y + 10, "red", 10, 10)
    elif current_direction == "down":
        body = gamebox.from_color(snake_tail.x, snake_tail.y - 10, "red", 10, 10)
    elif current_direction == "left":
        body = gamebox.from_color(snake_tail.x + 10, snake_tail.y, "red", 10, 10)
    elif current_direction == "right":
        body = gamebox.from_color(snake_tail.x - 10, snake_tail.y, "red", 10, 10)  # need to work on

    body.next = None
    snake_tail.next = body
    snake_tail = body


def traverse_snake():
    """
    Traverse through all the snake parts using while loop
    starting with snake_head
    move all the snake parts and draw them respectively on the screen
    :return:
    """
    snake = snake_head
    while snake is not None:
        snake_movement(snake)
        camera.draw(snake)
        snake = snake.next


def snake_movement(snake):
    """
    move all the snake according to the key pressed
    :param snake:
    :return:
    """
    print(previous_key)
    if previous_key[1] == "left" and snake.x <= change_d_coordinate[0]:  # it was turning left
        if current_direction == "up":
            # pass the changing point so that the body will turn
            snake.y -= snake_speed
        elif current_direction == "down":
            snake.y += snake_speed
        else:
            snake.x -= snake_speed
    elif previous_key[1] == "left":
        # did not pass the point
        snake.x -= snake_speed

    if previous_key[1] == "right" and snake.x >= change_d_coordinate[0]:  # it was turning left
        if current_direction == "up":
            # pass the changing point so that the body will turn
            snake.y -= snake_speed
        elif current_direction == "down":
            snake.y += snake_speed
        else:
            snake.x += snake_speed
    elif previous_key[1] == "right":
        # did not pass the point
        snake.x += snake_speed

    if previous_key[1] == "up" and snake.y <= change_d_coordinate[1]:  # it was turning left
        if current_direction == "left":
            # pass the changing point so that the body will turn
            snake.x -= snake_speed
        elif current_direction == "right":
            snake.x += snake_speed
        else:  # the other teo keys will not affect the previous
            snake.y -= snake_speed
    elif previous_key[1] == "up":  # it was turning left
        # did not pass the point
        snake.y -= snake_speed

    if previous_key[1] == "down" and snake.y >= change_d_coordinate[1]:  # it was turning left
        if current_direction == "left":
            # pass the changing point so that the body will turn
            snake.x -= snake_speed
        elif current_direction == "right":
            snake.x += snake_speed
        else:
            snake.y += snake_speed
    elif previous_key[1] == "down":  # it was turning left
        # did not pass the point
        snake.y += snake_speed


def food_generator():
    """
    generate the food location using random
    :return: the food sprite
    """
    x, y = [np.random.randint(5, 795), np.random.randint(5, 595)]
    return gamebox.from_color(x, y, "green", 10, 10)


def tick(key):
    """
    the main game
    :param key: key pressed
    :return:
    """
    global food_exist
    global current_direction
    global food
    global change_d_coordinate
    global previous_key

    if pygame.K_UP in key and previous_key[0] != "up" and previous_key[0] != "down": # prevent double upward
        current_direction = direction[0]
        change_d_coordinate = [snake_head.x, snake_head.y]
        previous_key[1] = previous_key[0]  # the last one is the most previous and the first one is the current
        previous_key[0] = "up"

    elif pygame.K_DOWN in key and previous_key[0] != "down" and previous_key[0] != "up":
        current_direction = direction[1]
        change_d_coordinate = [snake_head.x, snake_head.y]
        previous_key[1] = previous_key[0]
        previous_key[0] = "down"

    elif pygame.K_LEFT in key and previous_key[0] != "left" and previous_key[0] != "right":
        current_direction = direction[2]
        change_d_coordinate = [snake_head.x, snake_head.y]
        previous_key[1] = previous_key[0]
        previous_key[0] = "left"

    elif pygame.K_RIGHT in key and previous_key[0] != "right" and previous_key[0] != "left":
        current_direction = direction[3]
        change_d_coordinate = [snake_head.x, snake_head.y]
        previous_key[1] = previous_key[0]
        previous_key[0] = "right"
    key.clear()

    if not food_exist:
        # only one food can exit at a time
        food = food_generator()
        food_exist = True
    if snake_head.right_touches(food) or snake_head.left_touches(food) \
            or snake_head.top_touches(food) or snake_head.bottom_touches(food):
        # check if the food has been eaten and generate a new body
        snake_generator()
        food_exist = False

    camera.clear("white")
    traverse_snake()  # move snake and draw them. Needs to be put after camera.clear(
    camera.draw(food)
    camera.display()


if __name__ == "__main__":
    camera = gamebox.Camera(800, 600)
    snake_head = gamebox.from_color(400, 300, "red", 10, 10)
    snake_head.next = None
    snake_tail = snake_head

    gamebox.timer_loop(30, tick)
