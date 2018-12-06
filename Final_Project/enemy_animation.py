import pygame
import gamebox
import random

camera = gamebox.Camera(800, 600)
images = gamebox.load_sprite_sheet('enemy.png', 1, 5)

tick_count = 0
to_draw = []

x = 100
y = 100
enemy = gamebox.from_image(x, y, images[0])
enemy.scale_by(0.2)

def animation_enemy(keys):
    global tick_count
    camera.clear('green')
    enemy.image = images[tick_count // 2 % len(images)]  # Rotates through images
    tick_count += 1
    to_draw.append(enemy)
    for i in to_draw:
        camera.draw(i)
    camera.display()

gamebox.timer_loop(30, animation_enemy)




