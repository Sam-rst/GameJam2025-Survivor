import random
import pygame
from src.settings import *
from src.entities.player import Player
from src.systems.collision import *
from pytmx.util_pygame import load_pygame
from src.systems.input_manager import (
    KeyboardInputManager,
    NintendoSwitchProInputManager,
    XboxInputManager,
)
from src.utils.groups import AllSprites

LIST_CONTROLLERS_INPUT_MANAGERS = [NintendoSwitchProInputManager, XboxInputManager]
INPUTS_MANAGERS = {
    LAYOUTS["AZERTY"]: KeyboardInputManager(),
    LAYOUTS["QWERTY"]: KeyboardInputManager(),
    LAYOUTS["NSPRO"]: NintendoSwitchProInputManager(),
    LAYOUTS["XBOX"]: XboxInputManager(),
}


class Game:
    def __init__(self):
        self.selected_layout = DEFAULT_LAYOUT
        self.input_manager = INPUTS_MANAGERS[self.selected_layout]

        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Survivor")
        self.clock = pygame.time.Clock()
        self.running = True

        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()

        # Sprites --

    def setup(self):
        map = load_pygame(join("assets", "data", "maps", "world.tmx"))

        for x, y, image in map.get_layer_by_name("Ground").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites,))

        for obj in map.get_layer_by_name("Objects"):
            CollisionSprite(
                (obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites)
            )

        for obj in map.get_layer_by_name("Collisions"):
            CollisionSprite(
                (obj.x, obj.y),
                pygame.Surface((obj.width, obj.height)),
                self.collision_sprites,
            )

        for obj in map.get_layer_by_name("Entities"):
            if obj.name == "Spawn":
                print("Je suis un player")
                self.player = Player(
                    (obj.x, obj.y),
                    self.all_sprites,
                    self.collision_sprites,
                    self.input_manager,
                )

    def change_input_manager(self, layout: LAYOUTS):
        self.selected_layout = layout
        self.input_manager = INPUTS_MANAGERS[self.selected_layout]
        if isinstance(self.input_manager, tuple(LIST_CONTROLLERS_INPUT_MANAGERS)): # Pour les manettes
            self.input_manager.set_joystick(0)  # Toujours utiliser la première manette
        self.player.change_input_manager(self.input_manager)


    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick(60) / 1000

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Si une touche du clavier est pressée
                elif event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                    self.change_input_manager(DEFAULT_LAYOUT)
                    print("Changement avec le clavier")

                    if event.key in COMMAND_LAYOUTS[self.selected_layout]["pause"]:
                        self.running = False


                # Si un bouton de la manette est pressé
                elif event.type in [pygame.JOYBUTTONDOWN]:
                    joystick = pygame.joystick.Joystick(event.joy)
                    # print(f"Changement avec une manette {event.button}")

                    if joystick.get_name() == "Nintendo Switch Pro Controller":
                        print(f"Changement avec une manette {joystick.get_name()}")
                        self.change_input_manager(LAYOUTS["NSPRO"])
                    elif joystick.get_name() == "Controller (Xbox One For Windows)":
                        print(f"Changement avec une manette {joystick.get_name()}")
                        self.change_input_manager(LAYOUTS["XBOX"])
                    else:
                        print("Manette inconnue, retour au clavier.")
                        self.change_input_manager(LAYOUTS[DEFAULT_LAYOUT])

                    if event.button in COMMAND_LAYOUTS[self.selected_layout]["pause"]:
                        self.running = False

                # Détection de branchement de manette
                elif event.type == pygame.JOYDEVICEADDED:
                    try:
                        joystick = pygame.joystick.Joystick(event.device_index)
                        joystick.init()
                        print(f"Nouvelle manette détectée : {joystick.get_name()}")

                        # Changer dynamiquement l'input manager selon le type de manette
                        if joystick.get_name() == "Nintendo Switch Pro Controller":
                            print("Nintendo Switch Pro Controller initialized.")
                            self.change_input_manager(LAYOUTS["NSPRO"])
                        elif joystick.get_name() == "Controller (Xbox One For Windows)":
                            print("Xbox Controller initialized.")
                            self.change_input_manager(LAYOUTS["XBOX"])
                        else:
                            print("Manette inconnue, retour au clavier.")
                            self.change_input_manager(LAYOUTS[DEFAULT_LAYOUT])
                    except pygame.error as e:
                        print(f"Erreur lors de l'ajout d'une manette : {e}")

                # Détection de débranchement de manette
                elif event.type == pygame.JOYDEVICEREMOVED:
                    try:
                        print(f"Manette déconnectée : ID {event.instance_id}")
                        if pygame.joystick.get_count() == 0:
                            print("Aucune manette connectée, retour au clavier.")
                            self.change_input_manager(LAYOUTS[DEFAULT_LAYOUT])
                    except KeyError as e:
                        print(f"Erreur lors de la déconnexion de la manette : {e}")

            # Update
            self.all_sprites.update(dt)

            # Draw
            self.display_surface.fill("black")
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()
        print("Game closed.")


if __name__ == "__main__":
    game = Game()
    game.run()
