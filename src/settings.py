import pygame
from os.path import join
from os import walk

WINDOW_WIDTH, WINDOW_HEIGHT = 2560, 1440
TILE_SIZE = 64

LAYOUTS = {"AZERTY": "AZERTY", "QWERTY": "QWERTY", "XBOX": "XBOX", "NSPRO": "NSPRO", "PS5": "PS5"}
COMMAND_LAYOUTS = {
    LAYOUTS["AZERTY"]: {
        "move_up": [pygame.K_z, pygame.K_UP],
        "move_down": [pygame.K_s, pygame.K_DOWN],
        "move_left": [pygame.K_q, pygame.K_LEFT],
        "move_right": [pygame.K_d, pygame.K_RIGHT],
        "pause": [pygame.K_ESCAPE],
    },
    LAYOUTS["QWERTY"]: {
        "move_up": [pygame.K_w, pygame.K_UP],
        "move_down": [pygame.K_s, pygame.K_DOWN],
        "move_left": [pygame.K_a, pygame.K_LEFT],
        "move_right": [pygame.K_d, pygame.K_RIGHT],
        "pause": [pygame.K_ESCAPE],
    },
    LAYOUTS["XBOX"]: {
        "move_up": [pygame.JOYAXISMOTION],
        "move_down": [pygame.JOYAXISMOTION],
        "move_left": [pygame.JOYAXISMOTION],
        "move_right": [pygame.JOYAXISMOTION],
        "pause": [7],
    },
    LAYOUTS["NSPRO"]: {
        "move_up": [pygame.JOYAXISMOTION],
        "move_down": [pygame.JOYAXISMOTION],
        "move_left": [pygame.JOYAXISMOTION],
        "move_right": [pygame.JOYAXISMOTION],
        "pause": [6],
    },
    LAYOUTS["PS5"]: {
        "move_up": [pygame.JOYAXISMOTION],
        "move_down": [pygame.JOYAXISMOTION],
        "move_left": [pygame.JOYAXISMOTION],
        "move_right": [pygame.JOYAXISMOTION],
        "pause": [6],
    }
}

DEFAULT_LAYOUT = LAYOUTS["AZERTY"]

