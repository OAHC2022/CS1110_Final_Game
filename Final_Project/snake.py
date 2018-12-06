# zh2wc ml6vq
import sys
import time

import numpy as np
import pygame

import gamebox

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
# to record the movement and where to turn
snake_speed = 5
snake_size = 20
white = [255, 255, 255]
black = [0, 0, 0]
red = [255, 0, 0]
green = [0, 255, 0]
my_font = pygame.font.SysFont("Courtier", 40)
wall = pygame.image.load("wall.png")
wall_size = 40
left_right_wall = pygame.transform.scale(wall, [wall_size, 600])
top_down_wall = pygame.transform.scale(wall, [800 - 2 * wall_size, wall_size])  # make the wall
grass = pygame.image.load("grass.png")
grass = pygame.transform.scale(grass, [800 - 2 * wall_size, 600 - 2 * wall_size])
crab = pygame.image.load("crab.jpg")  # load the crab image
crab_size = 50
crab = pygame.transform.scale(crab, [crab_size, crab_size])
crab_exist = False
crab_speed = 2


def crab_generator():
    """
    generste the crab
    :return: a rectangle on where the crab is drawn on
    """
    x, y = [np.random.randint(wall_size + snake_size // 2, 800 - snake_size // 2 - wall_size),
            np.random.randint(wall_size + snake_size // 2, 600 - snake_size // 2 - wall_size)]
    crab_initial_pos = pygame.Rect(x, y, crab_size, crab_size)
    return crab_initial_pos


def crab_movement(crab_location, frame):  # change here
    """
    Move the crab
    :param crab_location: the current crab postion
    :return: return a new Rect with new position
    """
    if abs(snake_set["player1"][0].x - crab_location.x) >= \
            abs(snake_set["player1"][0].y - crab_location.y):
        if snake_set["player1"][0].x >= crab_location.x:
            # if the snake_head is on the right of the crab, the crab chases the snake head
            return crab_location.move(crab_speed, 0)
        else:
            return crab_location.move(-crab_speed, 0)
    else:
        if snake_set["player1"][0].y >= crab_location.y:
            return crab_location.move(0, crab_speed)
        else:
            return crab_location.move(0, -crab_speed)

def animation():
    global count
    snake.image = images[count//2 % len(images)]
    count += 1
    camera.clear('light green')
    draw_little()
    camera.draw(snake)
    camera.display()

def draw_little():
    instructions = '''Use the arrow keys to control the snake to collect foods to grow. 
Hitting the boarder or any part of the snake will make you lose the game.
In two-player mode, player two will use "w" for up, "s" for down, "a" for left, and "d" for right.
Have fun!'''.split('\n')
    mode1 = gamebox.from_image(200, 200, 'button.png')
    mode1.scale_by(0.4)
    mode2 = gamebox.from_image(600, 200, 'button.png')
    mode2.scale_by(0.4)
    camera.draw(gamebox.from_text(400, 100, "MODE SELECTION", 40, 'black', True))
    camera.draw(mode1)
    camera.draw(gamebox.from_text(200, 200, "one player", 25, 'black', True))
    camera.draw(mode2)
    camera.draw(gamebox.from_text(600, 200, "Two players", 25, 'black', True))
    camera.draw(gamebox.from_text(105, 300, "Instructions: ", 25, 'dark green'))
    for i in range(4):
        instruction = pygame.font.SysFont("Times", 15).render(instructions[i], True, (0, 200, 0))
        init_screen.blit(instruction, [50, 320 + 30 * i])
        
def snake_generator(keys):
    """
    generate the snake using linked list data structure
    snake_head is the beginning
    snake_tail is the end
    the snake sprite has two additional attributes: their next link and their current direction
    :return:
    """
    global snake_set
    global body

    tail = snake_set[keys][1]  # this is the head # need to work on
    if tail.direction == "up":
        body = gamebox.from_image(tail.x, tail.y + snake_size, 'body.png')
        body.scale_by(0.3)
        body.direction = "up"
    elif tail.direction == "down":
        body = gamebox.from_image(tail.x, tail.y - snake_size, 'body.png')
        body.scale_by(0.3)
        body.direction = "down"
    elif tail.direction == "left":
        body = gamebox.from_image(tail.x + snake_size, tail.y, 'body.png')
        body.scale_by(0.3)
        body.direction = "left"
    elif tail.direction == "right":
        body = gamebox.from_image(tail.x - snake_size, tail.y, 'body.png')
        body.scale_by(0.3)
        body.direction = "right"
    body.next = None
    tail.next = body
    snake_set[keys][1] = body
    points(keys)


def traverse_snake():
    """
    Traverse through all the snake parts using while loop
    starting with snake_head
    move all the snake parts and draw them respectively on the screen
    :return:
    """
    global snake_set
    for keys in snake_set:
        head = snake_set[keys][0]  # this is the head
        snake = head
        position_map = snake_set[keys][3]
        while snake is not None:
            snake_movement(snake, position_map)
            if_lose = lose_condition(snake)
            camera.draw(snake)
            if if_lose:
                """
                draw rest of the snakes
                """
                snake = snake.next
                while snake is not None:
                    snake_movement(snake, position_map)
                    camera.draw(snake)
                    snake = snake.next
                return if_lose
            snake = snake.next


def lose_condition(snake):  # return the head which touches the body
    for keys in snake_set:
        head = snake_set[keys][0]  # this is the head
        if head.direction == "up" and head.top_touches(snake) and snake is not head:
            return keys
        if head.direction == "down" and head.bottom_touches(snake) and snake is not head:
            return keys
        if head.direction == "left" and head.left_touches(snake) and snake is not head:
            return keys
        if head.direction == "right" and head.right_touches(snake) and snake is not head:
            return keys


def snake_movement(snake, position_map):
    """
    move all the snake according to the key pressed
    :param snake: the sprite
    :return:
    """
    key = (snake.x, snake.y)
    if key in position_map:  # find the turning point
        snake.direction = position_map[key]
        if snake.next is None:  # the last turning point. delete it from the dictionary
            position_map.pop(key)  # delete the lass turning point if all the snake sprites passed it
    snake_simple_movement(snake)  # move the sprites


def snake_simple_movement(snake):
    """
    the fundamental movement of the snake
    :param snake: the sprite
    :return:
    """
    if snake.direction == "up":
        snake.y -= snake_speed / player_number  # because it traverse the snake twice
    if snake.direction == "down":
        snake.y += snake_speed / player_number
    if snake.direction == "left":
        snake.x -= snake_speed / player_number
    if snake.direction == "right":
        snake.x += snake_speed / player_number


def food_generator():
    """
    generate the food location using random
    :return: the food sprite
    """
    x, y = [np.random.randint(wall_size + snake_size // 2, 800 - snake_size // 2 - wall_size),
            np.random.randint(wall_size + snake_size // 2, 600 - snake_size // 2 - wall_size)]
    food = gamebox.from_image(x, y, 'food.png')
    food.scale_by(0.05)
    return food


def check_for_turn(player, head, direction):
    """

    :param player: player1 or player2
    :param head: the head of the snake
    :param direction: Check the current direction and compare with the previous ones
                      in order to make sure the snake does not overlap itself
    :return:
    """
    position = (head.x, head.y)
    for key in snake_set[player][3]:
        if abs(position[0] - key[0]) <= snake_size:
            if snake_set[player][2][1] == "down" and direction == "up":
                return None
            if snake_set[player][2][1] == "up" and direction == "down":
                return None
        if abs(position[1] - key[1]) <= snake_size:
            if snake_set[player][2][1] == "left" and direction == "right":
                return None
            if snake_set[player][2][1] == "right" and direction == "left":
                return None
    return position


def event_handler1(key, player):
    """
    handle al the key inputs
    :param key:
    :return:
    """
    global snake_set

    head = snake_set[player][0]  # this is the head
    previous_key = snake_set[player][2]
    if player == "player2":
        if previous_key[0] != "up" and previous_key[0] != "down":
            if pygame.K_UP in key:  # prevent double upward still has down and upward
                position = check_for_turn(player, head, "up")
                if not position: return
                snake_set[player][3][position] = "up"  # set position_map = snake_set[keys][3] to a direction
                snake_set[player][2][1] = snake_set[player][2][0]
                snake_set[player][2][0] = "up"
            elif pygame.K_DOWN in key:
                position = check_for_turn(player, head, "down")
                if not position: return
                snake_set[player][3][position] = "down"
                snake_set[player][2][1] = snake_set[player][2][0]
                snake_set[player][2][0] = "down"

        if previous_key[0] != "left" and previous_key[0] != "right":
            if pygame.K_LEFT in key:
                position = check_for_turn(player, head, "left")
                if not position: return
                snake_set[player][3][position] = "left"
                snake_set[player][2][1] = snake_set[player][2][0]
                snake_set[player][2][0] = "left"
            elif pygame.K_RIGHT in key:
                position = check_for_turn(player, head, "right")
                if not position: return
                snake_set[player][3][position] = "right"
                snake_set[player][2][1] = snake_set[player][2][0]
                snake_set[player][2][0] = "right"

    elif player == "player1":
        if previous_key[0] != "up" and previous_key[0] != "down":
            if pygame.K_w in key:  # prevent double upward still has down and upward
                position = check_for_turn(player, head, "up")
                if not position: return
                snake_set[player][3][position] = "up"  # position_map = snake_set[keys][3]
                snake_set[player][2][1] = snake_set[player][2][0]
                snake_set[player][2][0] = "up"
            elif pygame.K_s in key:
                position = check_for_turn(player, head, "down")
                if not position: return
                snake_set[player][3][position] = "down"
                snake_set[player][2][1] = snake_set[player][2][0]
                snake_set[player][2][0] = "down"

        if previous_key[0] != "left" and previous_key[0] != "right":
            if pygame.K_a in key:
                position = check_for_turn(player, head, "left")
                if not position: return
                snake_set[player][3][position] = "left"
                snake_set[player][2][1] = snake_set[player][2][0]
                snake_set[player][2][0] = "left"
            elif pygame.K_d in key:
                position = check_for_turn(player, head, "right")
                if not position: return
                snake_set[player][3][position] = "right"
                snake_set[player][2][1] = snake_set[player][2][0]
                snake_set[player][2][0] = "right"


def points(keys):
    global snake_set
    snake_set[keys][4] += 1


def draw_points():
    start_position = 800 // (player_number + 1)
    for count, keys in enumerate(snake_set, 1):
        pos = start_position * count
        score = my_font.render(keys + ": " + str(snake_set[keys][4]), True, black)
        init_screen.blit(score, [pos, 10])


def tick(key):
    """
    the main game
    :param key: key pressed
    :return:
    """
    global food_exist
    global crab_exist
    global crab_location
    global food
    global frame  # just for debug
    frame += 1
    real_lose = False
    for keys in snake_set:
        event_handler1(key, keys)
    key.clear()

    for keys in snake_set:
        head = snake_set[keys][0]  # this is the head
        if not food_exist:
            # only one food can exit at a time
            food = food_generator()
            food_exist = True
        if head.right_touches(food) or head.left_touches(food) \
                or head.top_touches(food) or head.bottom_touches(food):
            # check if the food has been eaten and generate a new body
            snake_generator(keys)
            food_exist = False
        if not crab_exist:
            # only one food can exit at a time
            crab_location = crab_generator()
            crab_exist = True
        draw_background()
        camera.draw(food)
        camera.__dict__['_surface'].blit(crab, crab_location)  # draw the crab on the surface

        player_have_lost = traverse_snake()  # move snake and draw them. Needs to be put after camera.clear()
        player_have_lost1 = touch_wall()
        if player_have_lost or player_have_lost1:  # make lose instantly needs to work on because it acts twice
            real_lose = True
            break
    crab_location = crab_movement(crab_location, frame)
    draw_points()
    if real_lose:
        """
        redraw everthing and have 1 second to pause before entering the end game
        """
        draw_background()
        draw_snake()
        draw_points()
        camera.draw(food)
        pygame.display.update()
        time.sleep(1)
        snake_set.clear()
        if player_have_lost:
            end_frame(player_have_lost)
        else:
            end_frame(player_have_lost1)
    pygame.display.update()


def draw_snake():
    for keys in snake_set:
        head = snake_set[keys][0]  # this is the head
        snake = head
        while snake is not None:
            camera.draw(snake)
            snake = snake.next


def touch_wall():
    for keys in snake_set:
        head = snake_set[keys][0]  # this is the head
        if head.x <= wall_size or head.x >= 800 - wall_size or head.y <= wall_size or head.y >= 600 - wall_size:
            return keys


def draw_background():
    camera.draw(top_down_wall, [400, 20])
    camera.draw(top_down_wall, [400, 580])
    camera.draw(left_right_wall, [20, 300])
    camera.draw(left_right_wall, [780, 300])  # all the mid points
    camera.draw(grass, [400, 300])


def end_frame(player_have_lost):
    text1 = my_font.render(player_have_lost + " has lost!", True, (0, 200, 0))
    while True:
        init_screen.fill(white)
        init_screen.blit(text1, [50, 200])
        mode1 = gamebox.from_image(200, 300, 'button.png')
        mode1.scale_by(0.4)
        mode2 = gamebox.from_image(600, 300, 'button.png')
        mode2.scale_by(0.4)
        camera.draw(mode1)
        camera.draw(gamebox.from_text(200, 300, "Start Over", 25, 'black', True))
        camera.draw(mode2)
        camera.draw(gamebox.from_text(600, 300, "End the Game", 25, 'black', True))
        pygame.display.flip()
        break
    while True:
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode1.x - mode1.width / 2 < camera.mousex < mode1.x + mode1.width / 2:
                if mode1.y - mode1.height / 2 < camera.mousey < mode1.y + mode1.height / 2:
                    start_frame()
            if mode2.x - mode2.width / 2 < camera.mousex < mode2.x + mode2.width / 2:
                if mode2.y - mode2.height / 2 < camera.mousey < mode2.y + mode2.height / 2:
                    sys.exit()


def start_frame():
    global player_number
    pygame.init()
    start_img = pygame.image.load("start_screen.png")
    text1 = my_font.render("Welcome To The Hungry Snake Game!", True, (0, 200, 0))
    text2 = my_font.render("Press Any Key to Start", True, (0, 200, 0))
    init_screen.fill(white)
    init_screen.blit(start_img, [400, 300])
    init_screen.blit(text1, [50, 200])
    init_screen.blit(text2, [50, 250])
    pygame.display.flip()
    mode1 = gamebox.from_image(200, 200, 'button.png')
    mode1.scale_by(0.4)
    mode2 = gamebox.from_image(600, 200, 'button.png')
    mode2.scale_by(0.4)
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            return
        if event.type == pygame.KEYDOWN:
            break
    while True:
        event = pygame.event.poll()
        animation()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode1.x - mode1.width / 2 < camera.mousex < mode1.x + mode1.width / 2:
                if mode1.y - mode1.height / 2 < camera.mousey < mode1.y + mode1.height / 2:
                    player_number = 1
                    break
            if mode2.x - mode2.width / 2 < camera.mousex < mode2.x + mode2.width / 2:
                if mode2.y - mode2.height / 2 < camera.mousey < mode2.y + mode2.height / 2:
                    player_number = 2
                    break
    for players in range(player_number):
        snake_set["player{}".format(players + 1)] = add_player(players + 1)
    gamebox.timer_loop(30, tick)  # start the actual game


def add_player(players):
    start_position = (800 - 2 * wall_size) // (player_number + 1)
    snake_head = gamebox.from_image(wall_size // 2 + start_position * players, 300, 'head.png')
    snake_head.scale_by(0.15)
    snake_head.next = None
    snake_head.direction = "up"  # initial direction up
    snake_tail = snake_head
    previous_key = ["up", "up"]
    position_map = {}  # Use a dictionary to map all the turning point
    point = 0
    return [snake_head, snake_tail, previous_key, position_map, point]


if __name__ == "__main__":
    camera = gamebox.Camera(800, 600)
    init_screen = pygame.display.set_mode([800, 600])
    images = gamebox.load_sprite_sheet('snake_right.png', 4, 4)
    snake = gamebox.from_image(200, 100, images[0])
    count = 0
    snake_set = {}
    frame = 0
    start_frame()  # go to the start frame
