from src.settings import *
import pygame
from os.path import join
from abc import ABC, abstractmethod

class InputManager(ABC):
    """
    Centralized input manager to handle keyboard and controller inputs.
    """
    def __init__(self):
        self.actions = {
            "move_up": False,
            "move_down": False,
            "move_left": False,
            "move_right": False,
        }

    @abstractmethod
    def update(self):
        """
        Update the state of actions based on input devices.
        """

    @abstractmethod
    def _handle_keyboard(self):
        """
        Map keyboard inputs to actions.
        """

    @abstractmethod
    def get_direction(self):
        """
        Calculate the direction vector based on actions.
        """

class KeyboardInputManager(InputManager):
    def __init__(self):
        super().__init__()

    def update(self):
        self._handle_keyboard()

    def _handle_keyboard(self):
        keys = pygame.key.get_pressed()
        self.actions["move_up"] = keys[pygame.K_UP] or keys[pygame.K_z]
        self.actions["move_down"] = keys[pygame.K_DOWN] or keys[pygame.K_s]
        self.actions["move_left"] = keys[pygame.K_LEFT] or keys[pygame.K_q]
        self.actions["move_right"] = keys[pygame.K_RIGHT] or keys[pygame.K_d]

    def get_direction(self):
        self.update()
        direction = pygame.Vector2(
            int(self.actions["move_right"]) - int(self.actions["move_left"]),
            int(self.actions["move_down"]) - int(self.actions["move_up"]),
        )
        print(direction)
        return direction.normalize() if direction.length() > 0 else direction
