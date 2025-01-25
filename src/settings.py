import pygame
from os.path import join
from os import walk

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 64

LAYOUTS = {"AZERTY": "AZERTY", "QWERTY": "QWERTY"}

KEYBOARD_LAYOUTS = {
    LAYOUTS["AZERTY"]: {
        "move_up": [pygame.K_z, pygame.K_UP],
        "move_down": [pygame.K_s, pygame.K_DOWN],
        "move_left": [pygame.K_q, pygame.K_LEFT],
        "move_right": [pygame.K_d, pygame.K_RIGHT],
    },
    LAYOUTS["QWERTY"]: {
        "move_up": [pygame.K_w, pygame.K_UP],
        "move_down": [pygame.K_s, pygame.K_DOWN],
        "move_left": [pygame.K_a, pygame.K_LEFT],
        "move_right": [pygame.K_d, pygame.K_RIGHT],
    },
}

DEFAULT_LAYOUT = LAYOUTS["AZERTY"]
