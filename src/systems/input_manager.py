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
        Should be implemented by subclasses.
        """
        pass

    def get_direction(self):
        """
        Calculate the direction vector based on active actions.
        """
        self.update()
        direction = pygame.Vector2(
            int(self.actions["move_right"]) - int(self.actions["move_left"]),
            int(self.actions["move_down"]) - int(self.actions["move_up"]),
        )
        return direction.normalize() if direction.length() > 0 else direction


class KeyboardInputManager(InputManager):
    def __init__(self, layout: LAYOUTS=DEFAULT_LAYOUT):
        super().__init__()
        self.set_layout(layout)

    def set_layout(self, layout):
        """
        Configure the key mappings based on the selected keyboard layout.
        """
        self.key_mapping = KEYBOARD_LAYOUTS[layout]

    def update(self):
        """
        Update the state of actions based on keyboard inputs.
        """
        keys = pygame.key.get_pressed()
        for action, key_list in self.key_mapping.items():
            self.actions[action] = any(keys[key] for key in key_list)


class NintendoSwitchProInputManager(InputManager):
    def __init__(self, joystick_id=0):
        super().__init__()

        # Initialiser les joysticks
        pygame.joystick.init()

        # Essayer d'initialiser la première manette détectée
        try:
            if pygame.joystick.get_count() > 0:
                print(pygame.joystick.get_count())
                joystick_id = 0  # Utiliser le premier joystick détecté
                self.joystick = pygame.joystick.Joystick(joystick_id)
                self.joystick.init()
                print("Nintendo Switch Pro Controller initialized.")
            else:
                print("No controller detected.")
        except pygame.error as e:
            raise RuntimeError(f"Failed to initialize joystick: {e}")

    def update(self):
        """
        Update the state of actions based on controller inputs.
        """
        self.actions["move_up"] = self.joystick.get_axis(1) < -0.5
        self.actions["move_down"] = self.joystick.get_axis(1) > 0.5
        self.actions["move_left"] = self.joystick.get_axis(0) < -0.5
        self.actions["move_right"] = self.joystick.get_axis(0) > 0.5
