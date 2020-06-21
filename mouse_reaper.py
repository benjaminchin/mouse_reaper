import pygame, sys
from pygame.locals import *
import time
import random

WINDOW_HEIGHT = 480
WINDOW_WIDTH = 640

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)

score = 0
souls = []

SPAWN_RATE = 3
SOUL_SIZE = 20


GAME_OVER = 'gameover'
PLAYING = 'playing'

STATE = GAME_OVER


board = []

GENERATE = pygame.USEREVENT+1


def main():
    pygame.init()
    FPS = 30
    FPSCLOCK = pygame.time.Clock()
    pygame.time.set_timer(GENERATE, 1000)

    global score
    global board
    global STATE

    time = 60
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Mouse Reaper')

    font_obj = pygame.font.Font('freesansbold.ttf', 20)

    score_text_surface_obj = font_obj.render('Score: ' + str(score),
                                             True, BLACK
                                             )
    score_text_rect_obj = score_text_surface_obj.get_rect()
    score_text_rect_obj.topleft = (0, 0)

    gameover_text_surface_obj = font_obj.render('GAME OVER', True, GRAY)
    gameover_text_rect_obj = gameover_text_surface_obj.get_rect()
    gameover_text_rect_obj.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    click_play_text_surface_obj = font_obj.render('CLICK TO START',
                                                  True, GRAY
                                                  )
    click_play_text_rect_obj = click_play_text_surface_obj.get_rect()
    click_play_text_rect_obj.center = (WINDOW_WIDTH / 2, 280)

    timer_text_surface_obj = font_obj.render('Time: ' + str(time),
                                              True, GRAY
                                              )
    timer_text_rect_obj = timer_text_surface_obj.get_rect()
    timer_text_rect_obj.topleft = (0, 0)
   
    mousex = 0
    mousey = 0

    while True: # main game loop
        SCREEN.fill(BLACK)

        if STATE == GAME_OVER:
            SCREEN.blit(gameover_text_surface_obj, gameover_text_rect_obj)
            SCREEN.blit(click_play_text_surface_obj, click_play_text_rect_obj)
        elif STATE == PLAYING:
            timer_text_surface_obj = font_obj.render('Time: ' + str(time),
                                              True, GRAY
                                              )
            SCREEN.blit(timer_text_surface_obj, timer_text_rect_obj)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            if STATE == PLAYING:
                if event.type == GENERATE:
                    board += generate_souls(3)
                    time -= 1


            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos #Get mouse position
                if STATE == GAME_OVER:
                    # generate first 10 souls
                    board = generate_souls(10)
                    # for soul_rect in board:
                        # pygame.draw.rect(SCREEN, WHITE, soul_rect)
                    pygame.mixer.music.load('reaper.mp3') #Play music
                    pygame.mixer.music.play()
                    STATE = PLAYING

                elif STATE == PLAYING:
                    for soul_rect in board:
                        if soul_rect.collidepoint(mousex, mousey):
                            board.remove(soul_rect)

        for soul_rect in board:
            pygame.draw.rect(SCREEN, WHITE, soul_rect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generate_souls(num):
    global board
    result = []
   
    for i in range(num):
        while True:
            left = random.randint(0, WINDOW_WIDTH - SOUL_SIZE)
            top = random.randint(0, WINDOW_HEIGHT - SOUL_SIZE)
            new_soul = pygame.Rect(left, top, SOUL_SIZE, SOUL_SIZE)
            if new_soul.collidelist(board) == -1: # If no collisions
                # board.append(new_soul) # Add to list of soul rect objects
                result.append(new_soul)
                break
    return result


if __name__ == '__main__':
    main()