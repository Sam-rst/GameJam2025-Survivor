import random
import pygame
from src.settings import *
from src.entities.player import Player
from src.systems.collision import *
from pytmx.util_pygame import load_pygame
from src.systems.input_manager import KeyboardInputManager, NintendoSwitchProInputManager


INPUTS_MANAGERS = {
    "keyboard": KeyboardInputManager(layout=DEFAULT_LAYOUT),
    "nintendo_switch_pro": NintendoSwitchProInputManager(),
    "xbox_one_windows": NintendoSwitchProInputManager(),
}

class Game:
    def __init__(self):

        self.input_manager = INPUTS_MANAGERS["keyboard"]
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Survivor")
        self.clock = pygame.time.Clock()
        self.running = True

        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()

        # Sprites --
        self.player = Player(pos=(500, 300), groups=self.all_sprites, collision_sprites=self.collision_sprites, input_manager=self.input_manager)
        

    def setup(self):
        map = load_pygame(join('assets', 'data', 'maps', 'world.tmx'))
            
        for x,y,image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites,))
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick() / 1000

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Si une touche du clavier est pressée
                elif event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                    print("Changement avec le clavier")
                    self.player.change_input_manager(INPUTS_MANAGERS["keyboard"])
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                # Si un bouton de la manette est pressé
                elif event.type in [pygame.JOYBUTTONDOWN]:
                    joystick = pygame.joystick.Joystick(event.joy)
                    print(joystick.get_name())
                    if joystick.get_name() == "Nintendo Switch Pro Controller":
                        print("Changement avec une manette Nintendo Switch Pro")
                        self.input_manager = INPUTS_MANAGERS["nintendo_switch_pro"]
                        self.player.change_input_manager(self.input_manager)
                        if event.button == 6:
                            self.running = False
                    if joystick.get_name() == "Controller (Xbox One For Windows)":
                        print("Changement avec une manette Nintendo Switch Pro")
                        self.input_manager = INPUTS_MANAGERS["xbox_one_windows"]
                        self.player.change_input_manager(self.input_manager)
                        if event.button == 6:
                            self.running = False

            # Update
            self.all_sprites.update(dt)

            # Draw
            self.display_surface.fill("black")
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
