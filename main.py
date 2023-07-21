import pygame, colors, os, perlin, random
from blocks import *
from settings import *
import structures
from player import Player
from world import *

pygame.init()

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

game_clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 30)


world = World()

for i in range(10):
    i -= 5
    world.gen_chunk(i)

def render_world(camera_x, camera_y, world):
    global ZOOM, SCREEN_HEIGHT, SCREEN_WIDTH
    canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    canvas.fill(colors.WHITE)
    for key in world.blocks:
        block = world.blocks[key]
        if is_on_screen(camera_x, camera_y, key[0], key[1]):
            canvas.blit(block.texture, ((key[0] * ZOOM + camera_x * ZOOM) + SCREEN_WIDTH // 2, (key[1] * ZOOM + camera_y * ZOOM) + SCREEN_HEIGHT // 2))
    return canvas

def render_hud(canvas):
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(canvas, (0, 0))
    pos_text = game_font.render(f'X: {int(player.get_x())} Y: {int(player.get_y() + 64)}', True, colors.BLACK)

    # temp text for testing
    #highest_point = game_font.render(f'The highest point is {world.get_highest_point(int(player.get_x()))}', True, colors.BLACK)

    screen.blit(pos_text, (0, 0))
    #screen.blit(highest_point, (0, 15))

    return screen

player = Player(0, world.get_highest_point(0))

while True:
    game_clock.tick(20)
    window.fill(colors.WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        player.set_y(player.get_y() - PLAYER_MOVE_SPEED)
    if keys[pygame.K_w]:
        player.set_y(player.get_y() + PLAYER_MOVE_SPEED)
    if keys[pygame.K_a]:
        player.set_x(player.get_x() + PLAYER_MOVE_SPEED)
    if keys[pygame.K_d]:
        player.set_x(player.get_x() - PLAYER_MOVE_SPEED)

    world_render = render_world(player.get_x(), player.get_y(), world)
    final_render = render_hud(world_render)

    #print(f'Player x {player.get_x()}, Player y: {player.get_y()}')

    window.blit(final_render, (0, 0))

    pygame.display.flip()
