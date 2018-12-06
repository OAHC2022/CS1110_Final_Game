# zh2wc ml6vq
import pygame
import gamebox
import sys
import numpy as np

"""
This game is to make a traditional "snake" game.
The snake will start with a head. Then, everytime it eats a block, it will grow in length. 
The player will lose if the snake head touches itself or touches the wall.
The score will be calculated.

Additional Requirements:
1. two player play in the same time
2. collectibles
3. Enemies
4. Multiple game mode
"""

direction = ["up", "down", "left", "right"]
food_exist = False
previous_key = ["up", "up"]  # to record the movement and where to turn
snake_speed = 5
position_map = {(400, 300): "up"}  # Use a dictionary to map all the turning point
white = [255, 255, 255]
black = [0, 0, 0]
red = [255, 0, 0]
green = [0, 255, 0]
wall = pygame.image.load("wall.png")
wall_size = 40
left_right_wall = pygame.transform.scale(wall, [wall_size, 600])
top_down_wall = pygame.transform.scale(wall, [800 - 2 * wall_size, wall_size])  # make the wall
grass = pygame.image.load("grass.png")
grass = pygame.transform.scale(grass, [800 - 2 * wall_size, 600 - 2 * wall_size])


def snake_generator():
    """
    generate the snake using linked list data structure
    snake_head is the beginning
    snake_tail is the end
    the snake sprite has two additional attributes: their next link and their current direction
    :return:
    """
    global snake_head
    global snake_tail
    global body
    if snake_tail.direction == "up":
        body = gamebox.from_color(snake_tail.x, snake_tail.y + 10, "red", 10, 10)
        body.direction = "up"
    elif snake_tail.direction == "down":
        body = gamebox.from_color(snake_tail.x, snake_tail.y - 10, "red", 10, 10)
        body.direction = "down"
    elif snake_tail.direction == "left":
        body = gamebox.from_color(snake_tail.x + 10, snake_tail.y, "red", 10, 10)
        body.direction = "left"
    elif snake_tail.direction == "right":
        body = gamebox.from_color(snake_tail.x - 10, snake_tail.y, "red", 10, 10)
        body.direction = "right"
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
        if snake is not snake_head and lose_condition(snake):
            return True
        camera.draw(snake)
        snake = snake.next


def lose_condition(snake):
    if snake_head.direction == "up" and snake_head.top_touches(snake):
        return True
    if snake_head.direction == "down" and snake_head.bottom_touches(snake):
        return True
    if snake_head.direction == "left" and snake_head.left_touches(snake):
        return True
    if snake_head.direction == "right" and snake_head.right_touches(snake):
        return True


def snake_movement(snake):
    """
    move all the snake according to the key pressed
    :param snake: the sprite
    :return:
    """
    key = (snake.x, snake.y)
    if key in position_map:  # find the turning point
        snake.direction = position_map[key]
        if snake is snake_tail:  # the last turning point. delete it from the dictionary
            position_map.pop(key)  # delete the lass turning point if all the snake sprites passed it
    snake_simple_movement(snake)  # move the sprites


def snake_simple_movement(snake):
    """
    the fundamental movement of the snake
    :param snake: the sprite
    :return:
    """
    if snake.direction == "up":
        snake.y -= snake_speed
    if snake.direction == "down":
        snake.y += snake_speed
    if snake.direction == "left":
        snake.x -= snake_speed
    if snake.direction == "right":
        snake.x += snake_speed


def food_generator():
    """
    generate the food location using random
    :return: the food sprite
    """
    x, y = [np.random.randint(wall_size + 5, 795 - wall_size), np.random.randint(wall_size + 5, 595 - wall_size)]
    return gamebox.from_color(x, y, "pink", 10, 10)


def event_handler(key):
    """
    handle al the key inputs
    :param key:
    :return:
    """
    global position_map
    if pygame.K_UP in key and previous_key[0] != "up" and previous_key[
        0] != "down":  # prevent double upward still has down and upward
        position = (snake_head.x, snake_head.y)
        position_map[position] = "up"
        previous_key[1] = previous_key[0]
        previous_key[0] = "up"

    elif pygame.K_DOWN in key and previous_key[0] != "down" and previous_key[0] != "up":
        position = (snake_head.x, snake_head.y)
        position_map[position] = "down"
        previous_key[1] = previous_key[0]
        previous_key[0] = "down"

    elif pygame.K_LEFT in key and previous_key[0] != "left" and previous_key[0] != "right":
        position = (snake_head.x, snake_head.y)
        position_map[position] = "left"
        previous_key[1] = previous_key[0]
        previous_key[0] = "left"

    elif pygame.K_RIGHT in key and previous_key[0] != "right" and previous_key[0] != "left":
        position = (snake_head.x, snake_head.y)
        position_map[position] = "right"
        previous_key[1] = previous_key[0]
        previous_key[0] = "right"
    key.clear()


def tick(key):
    """
    the main game
    :param key: key pressed
    :return:
    """
    global food_exist
    global food
    global previous_key

    event_handler(key)

    if not food_exist:
        # only one food can exit at a time
        food = food_generator()
        food_exist = True
    if snake_head.right_touches(food) or snake_head.left_touches(food) \
            or snake_head.top_touches(food) or snake_head.bottom_touches(food):
        # check if the food has been eaten and generate a new body
        snake_generator()
        food_exist = False

    draw_background()
    have_lost = traverse_snake()  # move snake and draw them. Needs to be put after camera.clear()
    camera.draw(food)
    pygame.display.update()
    if have_lost or touch_wall():
        end_frame()


def touch_wall():
    if snake_head.x <= wall_size or snake_head.x >= 800 - wall_size or snake_head.y <= wall_size or snake_head.y >= 600 - wall_size:
        return True


def draw_background():
    camera.draw(top_down_wall, [400, 20])
    camera.draw(top_down_wall, [400, 580])
    camera.draw(left_right_wall, [20, 300])
    camera.draw(left_right_wall, [780, 300])  # all the mid points
    camera.draw(grass, [400, 300])


def end_frame():
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            sys.exit()
        init_screen.fill(red)
        pygame.display.flip()


def start_frame():
    pygame.init()
    start_img = pygame.image.load("start_screen.png")
    text1 = my_font.render("Welcome To The Hungry Snake Game!", True, (0, 200, 0))
    text2 = my_font.render("Press Any Key to Start", True, (0, 200, 0))
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            return
        if event.type == pygame.KEYDOWN:
            break
        init_screen.fill(white)
        init_screen.blit(start_img, [400, 300])
        init_screen.blit(text1, [50, 200])
        init_screen.blit(text2, [50, 250])
        pygame.display.flip()
    gamebox.timer_loop(30, tick)  # start the actual game


if __name__ == "__main__":
    camera = gamebox.Camera(800, 600)
    init_screen = pygame.display.set_mode([800, 600])
    snake_head = gamebox.from_color(400, 300, "red", 10, 10)
    snake_head.next = None
    snake_head.direction = "up"  # initial direction up
    snake_tail = snake_head
    my_font = pygame.font.SysFont("Courtier", 40)
    start_frame()  # go to the start frame
