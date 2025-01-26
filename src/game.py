from random import randint, choice
import pygame
from src.settings import *
from src.entities.player import Player
from src.systems.collision import Enemy
from src.systems.collision import *
from pytmx.util_pygame import load_pygame
from src.systems.input_manager import (
    KeyboardInputManager,
    NintendoSwitchProInputManager,
    XboxInputManager,
    PS5InputManager,
)
from src.utils.groups import AllSprites

LIST_CONTROLLERS_INPUT_MANAGERS = [NintendoSwitchProInputManager, XboxInputManager, PS5InputManager]
INPUTS_MANAGERS = {
    LAYOUTS["AZERTY"]: KeyboardInputManager(),
    LAYOUTS["QWERTY"]: KeyboardInputManager(),
    LAYOUTS["NSPRO"]: NintendoSwitchProInputManager(),
    LAYOUTS["XBOX"]: XboxInputManager(),
    LAYOUTS["PS5"]: PS5InputManager(),
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
        self.bullet_sprites = pygame.sprite.Group()
        self.ennemy_sprites = pygame.sprite.Group()

        # gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

        # enemy timer
        self.ennemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.ennemy_event, 300)
        self.spawn_position = []

        # audio
        self.shoot_song = pygame.mixer.Sound(join('assets', 'sounds', 'shoot.wav'))
        self.shoot_song.set_volume(0.4)
        self.impact_sound = pygame.mixer.Sound(join('assets', 'sounds', 'impact.ogg'))
        self.music = pygame.mixer.Sound(join('assets', 'sounds', 'music.wav'))
        self.music.set_volume(0.3)
        self.music.play(loops = -1)

        # setup
        self.load_images()
        self.setup()

    def load_images(self):
        self.bullet_surf = pygame.image.load(join('assets', 'images', 'gun', 'bullet.png')).convert_alpha()

        folders = list(walk(join('assets', 'images', 'enemies')))[0][1]
        self.ennemy_frame = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join('assets', 'images', 'enemies', folder)):
                self.ennemy_frame[folder] = []
                for file_name in sorted(file_names, key=lambda name: name.split('.')[0]):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.ennemy_frame[folder].append(surf)

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.shoot_song.play()
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True


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
                self.player = Player(
                    (obj.x, obj.y),
                    self.all_sprites,
                    self.collision_sprites,
                    self.input_manager,
                )
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_position.append((obj.x, obj.y))

    def change_input_manager(self, layout: LAYOUTS):
        self.selected_layout = layout
        self.input_manager = INPUTS_MANAGERS[self.selected_layout]
        if isinstance(self.input_manager, tuple(LIST_CONTROLLERS_INPUT_MANAGERS)): # Pour les manettes
            self.input_manager.set_joystick(0)  # Toujours utiliser la première manette
        self.player.change_input_manager(self.input_manager)

    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.ennemy_sprites, False, pygame.sprite.collide_mask)
                if collision_sprites:
                    self.impact_sound.play()
                    for sprite in collision_sprites:
                        sprite.destroy()
                    bullet.kill()

    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.ennemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False

    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick(60) / 1000

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.ennemy_event:
                    Enemy(choice(self.spawn_position), choice(list(self.ennemy_frame.values())), (self.all_sprites, self.ennemy_sprites), self.player, self.collision_sprites)

                # Si une touche du clavier est pressée
                elif event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                    self.change_input_manager(DEFAULT_LAYOUT)
                    print("Changement avec le clavier")
                    if event.type == pygame.KEYDOWN:
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
                    elif joystick.get_name() == "DualSense Wireless Controller":
                        print(f"Changement avec une manette {joystick.get_name()}")
                        self.change_input_manager(LAYOUTS["PS5"])
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
                        elif joystick.get_name() == "DualSense Wireless Controller":
                            print("PS5 Controller initialized.")
                            self.change_input_manager(LAYOUTS["PS5"])
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
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)
            self.bullet_collision()
            self.player_collision()

            # Draw
            self.display_surface.fill("black")
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()
        print("Game closed.")


if __name__ == "__main__":
    game = Game()
    game.run()
