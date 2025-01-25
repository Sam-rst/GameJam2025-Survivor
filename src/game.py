import random
import pygame
from src.settings import *
from src.entities.player import Player
from src.systems.collision import *
from pytmx.util_pygame import load_pygame
from src.systems.input_manager import KeyboardInputManager


class Game:
    def __init__(self):
        input_manager = KeyboardInputManager()

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
        self.player = Player(pos=(500, 300), groups=self.all_sprites, collision_sprites=self.collision_sprites, input_manager=input_manager)
        

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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.QUIT:
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
