from typing import Any
import pygame
from sys import exit
from random import randint, choice

# initialization
pygame.init()
pygame.display.set_caption('Dino Run')
icon = pygame.image.load('assets/graphics/favicon.png')
pygame.display.set_icon(icon)

# variables
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
text_font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 45)
score_font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 20)
game_active = False
game_speed = 1
start_time = 0
score = 0

# Text
game_over = text_font.render("Game Over", False, '#272727')
game_over_rectangle = game_over.get_rect(center = (400,180))
restart = score_font.render("Press Enter to restart", False, '#272727')
restart_rectangle = restart.get_rect(center = (400,350))
welcome_message = score_font.render("Welcome to DINO RUN", False, '#272727')
welcome_message_rect = welcome_message.get_rect(center = (400,180))
start_text = score_font.render("Press Enter to start", False, '#272727')
start_text_rect = start_text.get_rect(center = (400,220))

# Ground
ground_surface = pygame.transform.scale2x(pygame.image.load('assets/graphics/ground.png').convert_alpha())
ground_x = 0

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Dino Walking
        dino_walk1 = pygame.image.load('assets/graphics/dino/Dino1.png').convert_alpha()
        dino_walk2 = pygame.image.load('assets/graphics/dino/Dino2.png').convert_alpha()
        dino_walk1_scale = pygame.transform.scale(dino_walk1, (int(dino_walk1.get_width()*1.2), int(dino_walk1.get_height()*1.2)))
        dino_walk2_scale = pygame.transform.scale(dino_walk2, (int(dino_walk2.get_width()*1.2), int(dino_walk2.get_height()*1.2)))
        self.dino_walk = [dino_walk1_scale, dino_walk2_scale]
        self.dino_index = 0
        self.dino_surface = self.dino_walk[self.dino_index]
        # Dino Jumping
        dino_jumping = pygame.image.load('assets/graphics/dino/DinoJumping.png').convert_alpha()
        self.dino_jump = pygame.transform.scale(dino_jumping, (int(dino_jumping.get_width()*1.2), int(dino_jumping.get_height()*1.2)))
        # Dino Ducking
        dino_duck1 = pygame.image.load('assets/graphics/dino/DinoDucking1.png').convert_alpha()
        dino_duck2 = pygame.image.load('assets/graphics/dino/DinoDucking2.png').convert_alpha()
        dino_duck1_scale = pygame.transform.scale(dino_duck1, (int(dino_duck1.get_width()*1.2), int(dino_duck1.get_height()*1.2)))
        dino_duck2_scale = pygame.transform.scale(dino_duck2, (int(dino_duck2.get_width()*1.2), int(dino_duck2.get_height()*1.2)))
        self.dino_duck = [dino_duck1_scale, dino_duck2_scale]
        self.dino_duck_index = 0
        self.dino_duck_surface = self.dino_duck[self.dino_duck_index]

        
        
        self.image = self.dino_walk[self.dino_index]
        self.rect = self.image.get_rect(midbottom=(80, 360))
        self.gravity = 0
        
        self.ducking = False
        

    def dino_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 356:
            self.gravity = -15
        if keys[pygame.K_s]:
            self.rect.y += 20
            self.ducking = True
        else: self.ducking = False
            
            
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 360 and not self.ducking:
            self.rect.bottom = 360
        elif self.rect.bottom >= 380 and self.ducking:
            self.rect.bottom = 380
        
    
    def animation_state(self):
        if self.rect.bottom > 361:
            self.dino_duck_index += 0.1
            if self.dino_duck_index >= len(self.dino_duck):
                self.dino_duck_index = 0
            self.image = self.dino_duck[int(self.dino_duck_index)]
        elif self.rect.bottom < 360:
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
        
        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, y, moving):
        super().__init__()
        y_pos = y
        if moving:
            self.animation_index = 0
            frame_1 = pygame.image.load(f'assets/graphics/{type}/{type}1.png').convert_alpha()
            frame_2 = pygame.image.load(f'assets/graphics/{type}/{type}2.png').convert_alpha()
            self.frames = [frame_1, frame_2]
            self.image = self.frames[self.animation_index]
        else:
            type_dr = type
            try:
                int(type[-1])
                type_dr = type[:-1]
            except ValueError:
                pass
            self.image = pygame.image.load(f'assets/graphics/{type_dr}/{type}.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))
    
    def update(self):
        self.rect.x -= 6
        self.destroy()
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
            
class MovingObstacle(Obstacle, pygame.sprite.Sprite):
    def __init__(self, type, y, moving):
        super().__init__(type, y, moving)
        
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

class Bird(MovingObstacle):
    def __init__(self):
        super().__init__('bird', 300, True)

class Cactus1(Obstacle):
    def __init__(self):
        super().__init__('cactus1', 360, False)

class Cactus2(Obstacle):
    def __init__(self):
        super().__init__('cactus2', 360, False)

class Cactus3(Obstacle):
    def __init__(self):
        super().__init__('cactus3', 360, False)

class Cactus4(Obstacle):
    def __init__(self):
        super().__init__('cactus4', 360, False)

class Cactus5(Obstacle):
    def __init__(self):
        super().__init__('cactus5', 360, False)

class Cactus6(Obstacle):
    def __init__(self):
        super().__init__('cactus6', 360, False)

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        cloud = pygame.image.load('assets/graphics/cloud.png').convert_alpha()
        self.image = pygame.transform.scale2x(cloud)
        self.rect = self.image.get_rect(bottomleft = (randint(900,2000),300))
        
    def cloud_movement(self):
        self.rect.x -= game_speed
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
            
    
    def update(self):
        self.cloud_movement()
        self.destroy()
                
def collisions(dino, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if dino.colliderect(obstacle_rect):
                obstacle_group.empty()
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(dino.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True
    
def display_time():
    current_time = int((pygame.time.get_ticks()/1000) - start_time)
    score_surface = text_font.render(f'YOUR SCORE: {current_time}', False, '#272727' )
    score_rectangle = score_surface.get_rect(midtop = (400,50))
    screen.blit(score_surface, score_rectangle)
    return current_time

# Timers
obstacle_timer = pygame.USEREVENT +1
pygame.time.set_timer(obstacle_timer, 1500)

cloud_timer = pygame.USEREVENT +2
pygame.time.set_timer(cloud_timer, 1500)

# Groups
dino = pygame.sprite.GroupSingle()
dino.add(Dino())

obstacle_group = pygame.sprite.Group()

clouds = pygame.sprite.Group()

# Main Loop
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
                start_time = int(pygame.time.get_ticks()/1000)
                dino.sprite.rect.y = 360
                clouds.empty()
                
        
        if event.type == obstacle_timer and game_active:
            obstacle_group.add(choice([Bird(), Cactus1(), Cactus2(), Cactus3(), Cactus4(), Cactus5(), Cactus6()]))

        if event.type == cloud_timer and game_active:
            clouds.add(Cloud())
        
        
    if game_active:
        game_speed += 0.0025
        
        # background
        screen.fill('White')
        ground_x -= game_speed
        screen.blit(ground_surface, (ground_x, 330))
        screen.blit(ground_surface, (ground_x + 1280, 330))
        if ground_x <= -1280:
            ground_x = 0
        
        # Text
        score = display_time()
        
        # cloud
        clouds.draw(screen)
        clouds.update()
        
        # dino
        dino.draw(screen)
        dino.update()
        
        # obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        # Collision
        game_active = collision_sprite()
    else:
        if score != 0:
            screen.fill('White')
            game_speed = 1
            score_message = score_font.render(f"Your score is: {score}",False, '#272727')
            score_message_rectangle = score_message.get_rect(center = (400,220))
            screen.blit(game_over,game_over_rectangle)
            screen.blit(restart,restart_rectangle)
            screen.blit(score_message, score_message_rectangle)
        else:
            game_speed = 1
            screen.fill('White')
            screen.blit(welcome_message, welcome_message_rect)
            screen.blit(start_text, start_text_rect)
            
    pygame.display.update()
    clock.tick(60)
