from src.settings import *
import pygame
from os.path import join
from abc import ABC, abstractmethod


class InputManager(ABC):
    """
    Centralized input manager to handle keyboard and controller inputs.
    """

    def __init__(self, layout: LAYOUTS = DEFAULT_LAYOUT):
        self.set_layout(layout)

        self.actions = {
            "move_up": {"state": False, "key": COMMAND_LAYOUTS[layout]["move_up"]},
            "move_down": {"state": False, "key": COMMAND_LAYOUTS[layout]["move_down"]},
            "move_left": {"state": False, "key": COMMAND_LAYOUTS[layout]["move_left"]},
            "move_right": {
                "state": False,
                "key": COMMAND_LAYOUTS[layout]["move_right"],
            },
            "pause": {"state": False, "key": COMMAND_LAYOUTS[layout]["pause"]},
        }

    def set_layout(self, layout):
        """
        Configure the key mappings based on the selected keyboard layout.
        """
        self.key_mapping = COMMAND_LAYOUTS[layout]

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
            int(self.actions["move_right"]["state"])
            - int(self.actions["move_left"]["state"]),
            int(self.actions["move_down"]["state"])
            - int(self.actions["move_up"]["state"]),
        )
        return direction.normalize() if direction.length() > 0 else direction


class KeyboardInputManager(InputManager):
    def __init__(self, layout: LAYOUTS = DEFAULT_LAYOUT):
        super().__init__(layout=layout)
        self.set_layout(layout)

    def update(self):
        """
        Update the state of actions based on keyboard inputs.
        """
        keys = pygame.key.get_pressed()
        for action, key_list in self.key_mapping.items():
            self.actions[action]["state"] = any(keys[key] for key in key_list)


class NintendoSwitchProInputManager(InputManager):
    def __init__(self, joystick_id=0, layout: LAYOUTS = LAYOUTS["NSPRO"]):
        super().__init__(layout=layout)
        pygame.joystick.init()
        self.joystick = None
        self.set_joystick(joystick_id)

    def set_joystick(self, joystick_id):
        """Initialize or update the joystick."""
        if pygame.joystick.get_count() > 0:
            try:
                self.joystick = pygame.joystick.Joystick(joystick_id)
                self.joystick.init()
                print("Nintendo Switch Pro Controller initialized.")
            except pygame.error as e:
                print(f"Failed to initialize Nintendo Switch Pro Controller: {e}")
        else:
            print("No Nintendo Switch Pro Controller detected.")
            self.joystick = None

    def update(self):
        """Update the state of actions based on controller inputs."""
        if self.joystick:
            self.actions["move_up"]["state"] = self.joystick.get_axis(1) < -0.5
            self.actions["move_down"]["state"] = self.joystick.get_axis(1) > 0.5
            self.actions["move_left"]["state"] = self.joystick.get_axis(0) < -0.5
            self.actions["move_right"]["state"] = self.joystick.get_axis(0) > 0.5
        else:
            print("No joystick available for update.")


class XboxInputManager(InputManager):
    def __init__(self, joystick_id=0, layout: LAYOUTS = LAYOUTS["NSPRO"]):
        super().__init__(layout=layout)
        pygame.joystick.init()
        self.joystick = None
        self.set_joystick(joystick_id)

    def set_joystick(self, joystick_id):
        """Initialize or update the joystick."""
        if pygame.joystick.get_count() > 0:
            try:
                self.joystick = pygame.joystick.Joystick(joystick_id)
                self.joystick.init()
                print("Xbox Controller initialized.")
            except pygame.error as e:
                print(f"Failed to initialize Xbox Controller: {e}")
        else:
            print("No Xbox Controller detected.")
            self.joystick = None

    def update(self):
        """Update the state of actions based on controller inputs."""
        if self.joystick:
            self.actions["move_up"]["state"] = self.joystick.get_axis(1) < -0.5
            self.actions["move_down"]["state"] = self.joystick.get_axis(1) > 0.5
            self.actions["move_left"]["state"] = self.joystick.get_axis(0) < -0.5
            self.actions["move_right"]["state"] = self.joystick.get_axis(0) > 0.5
        else:
            print("No joystick available for update.")
