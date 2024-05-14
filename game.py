import pygame
from sys import exit
from random import randint, choice

# initialization
pygame.init()
pygame.display.set_caption('Dino Run')

# variables
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
text_font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf')
game_active = False

# Ground
ground_surface = pygame.transform.scale2x(pygame.image.load('assets/graphics/ground.png').convert_alpha())
ground_rectangle = ground_surface.get_rect(topleft=(0, 300))

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        dino_walk1 = pygame.transform.scale2x(pygame.image.load('assets/graphics/dino/Dino1.png').convert_alpha())
        dino_walk2 = pygame.transform.scale2x(pygame.image.load('assets/graphics/dino/Dino2.png').convert_alpha())
        self.dino_walk = [dino_walk1, dino_walk2]
        self.dino_index = 0
        self.dino_surface = self.dino_walk[self.dino_index]
        self.dino_jump = pygame.transform.scale2x(pygame.image.load('assets/graphics/dino/DinoJumping.png').convert_alpha())
        
        self.image = self.dino_walk[self.dino_index]
        self.rect = self.image.get_rect(midbottom=(80, 350))
        self.gravity = 0
        

    def dino_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 350:
            self.gravity = -20
            
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 350:
            self.rect.bottom = 350
    
    def animation_state(self):
        if self.rect.bottom < 350:
            self.image = self.dino_jump
        else:
            self.dino_index += 0.1
            if self.dino_index >= len(self.dino_walk):
                self.dino_index = 0
            self.image = self.dino_walk[int(self.dino_index)]

    def update(self):
        self.dino_input()
        self.apply_gravity()
        self.animation_state()


# Groups
dino = pygame.sprite.GroupSingle()
dino.add(Dino())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
        # Turning off the game
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        # Starting the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_active = True
        
    if game_active:
        # background
        screen.fill('White')
        screen.blit(ground_surface, ground_rectangle)
        
        # dino
        dino.draw(screen)
        dino.update()

    pygame.display.update()
    clock.tick(60)
