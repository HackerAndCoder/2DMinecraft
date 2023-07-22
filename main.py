import pygame, colors, os, perlin, random
from blocks import *
from settings import *
import structures
from player import Player
from world import *
import gui

pygame.init()

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Cave game (Updated)')

game_clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 30)

current_gui = gui.INGAME

onscreen_blocks = []
y_velocity = 0
player_on_block = False
gravity_amplifier = 0.3
debug_menu_open = True
player_jumped = False
last_player_pos = ()

esc_dimmer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
esc_dimmer.set_alpha(128)

world = World()

for i in range(10):
    i -= 5
    world.gen_chunk(i)

def render_world(camera_x, camera_y, world):
    global ZOOM, SCREEN_HEIGHT, SCREEN_WIDTH, onscreen_blocks
    onscreen_blocks = []
    canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    canvas.fill(colors.WHITE)
    for key in world.blocks:
        block = world.blocks[key]
        if is_on_screen(camera_x, camera_y, key[0], key[1]):
            canvas.blit(block.texture, ((key[0] * ZOOM + camera_x * ZOOM) + SCREEN_WIDTH // 2, (key[1] * ZOOM + camera_y * ZOOM) + SCREEN_HEIGHT // 2))
            onscreen_blocks.append(pygame.Rect(key[0] * ZOOM + camera_x * ZOOM + SCREEN_WIDTH // 2, (key[1] * ZOOM + camera_y * ZOOM) + SCREEN_HEIGHT // 2, ZOOM, ZOOM))
            
    return canvas

def render_hud():
    global current_gui
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    if current_gui == gui.INGAME or current_gui == gui.PAUSE_GAME:
        screen.blit(render_world(player.get_x(), player.get_y(), world), (0, 0))
        if debug_menu_open:
            pos_text = game_font.render(f'X: {int(player.get_x())} Y: {int(player.get_y() + 64)} FPS: {int(game_clock.get_fps())}', True, colors.BLACK)
            
            for block in onscreen_blocks:
                pygame.draw.rect(screen, colors.AQUA, block, 1)
                pygame.draw.circle(screen, colors.BLUE, utils.get_center_of_rect(block), 5, 2)

            screen.blit(pos_text, (0, 0))
            if player_on_block:
                pygame.draw.rect(screen, colors.RED, player_hitbox, 1)
            else:
                pygame.draw.rect(screen, colors.AQUA, player_hitbox, 1)

        screen.blit(player.texture, (SCREEN_WIDTH // 2 - player.texture.get_width() // 2, SCREEN_HEIGHT // 2 - player.texture.get_height() // 2))

    if current_gui == gui.PAUSE_GAME:
        screen.blit(esc_dimmer, (0, 0))

    return screen

player = Player(0, world.get_highest_point(0))
player_hitbox = player.texture.get_rect()
player_hitbox = player_hitbox.move(SCREEN_WIDTH // 2 - player.texture.get_width() // 2, SCREEN_HEIGHT // 2 - player.texture.get_height() // 2)

def is_colliding(rect1, rect2):
    return rect1.colliderect(rect2)

while True:
    last_player_pos = player.get_pos()
    game_clock.tick(20)
    window.fill(colors.WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if current_gui == gui.INGAME:
                    current_gui = gui.PAUSE_GAME
                elif current_gui == gui.PAUSE_GAME:
                    current_gui = gui.INGAME
            elif event.key == pygame.K_TAB:
                player.is_flying = not player.is_flying
                gravity_amplifier = 0.1
            
            elif event.key == pygame.K_F3:
                debug_menu_open = not debug_menu_open

    keys = pygame.key.get_pressed()
    if current_gui == gui.INGAME:
        if keys[pygame.K_s]:
            if not player_on_block or player.is_flying:
                player.set_y(player.get_y() - PLAYER_MOVE_SPEED)
        if keys[pygame.K_w] or keys[pygame.K_SPACE]:
            if player.is_flying:
                player.set_y(player.get_y() + PLAYER_MOVE_SPEED)
            else:
                #if player_on_block:
                player_jumped = True
                # insert gravity stuff here to make player jump

        if keys[pygame.K_a]:
            player.set_x(player.get_x() + PLAYER_MOVE_SPEED)
        if keys[pygame.K_d]:
            player.set_x(player.get_x() - PLAYER_MOVE_SPEED)
    
    player_on_block = False

    for block in onscreen_blocks:
        if is_colliding(block, player_hitbox):
            if not player_on_block: # this is when the player hit the ground, this won't be called when the player stays on the ground
                # handle fall damage here with ticks_fallen?
                pass
            player_on_block = True
            
            block_x = utils.get_center_of_rect(block)[0]
            if block_x < player_hitbox.center[0] < block_x:
                player.set_pos(last_player_pos)
                print('reset_pos')
            

            if block.top < player_hitbox.top:
                # player should sufficate?
                pass

        if is_colliding(block, player_hitbox.move(0, -3)):
            player.set_y(player.get_y() + 0.03)

        if player_on_block:
            player.ticks_fallen = 0

    if (not player_on_block and not player.is_flying):
        player.ticks_fallen += 1
        player.set_y(player.get_y() - 0.3)


    final_render = render_hud()

    #print(f'Player x {player.get_x()}, Player y: {player.get_y()}')

    window.blit(final_render, (0, 0))

    pygame.display.flip()