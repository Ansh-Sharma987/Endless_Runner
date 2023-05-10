import pygame
from sys import exit
from random import randint,choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('Images/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('Images/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('Images/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (50,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('Audio/jump.mp3')
        self.jump_sound.set_volume(0.4)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('Images/Obstacle/Fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('Images/Obstacle/Fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 200
        else:
            snail_1 = pygame.image.load('Images/Obstacle/Snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('Images/Obstacle/Snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(500, 50))
    screen.blit(score_surface, score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((740,400))

pygame.display.set_caption('Endless Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('Font/font.otf', 40)
game_active = False
start_time = 0
score = 0

bg_music = pygame.mixer.Sound('Audio/bg_music.mp3')
bg_music.set_volume(0.7)
bg_music.play(loops = -1)

#player
player = pygame.sprite.GroupSingle()
player.add(Player())

#obstacles
obstacle_group = pygame.sprite.Group()

#backgroud
sky_surface = pygame.image.load('Images/sky.jpg').convert()
ground_surface = pygame.image.load('Images/ground.png').convert()


#intro screen
player_stand = pygame.image.load('Images/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center= (360,200))

game_name = test_font.render('ENDLESS RUNNER',False,(111,196,169))
game_name_rect= game_name.get_rect(center=(360,80))

game_msg = test_font.render('Press space to run',False,(111,196,169))
game_msg_rect = game_msg.get_rect(center=(360,340))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))

        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)

        obstacle_group.update()

        game_active = collision_sprite()
    else:
        screen.fill((64,64,64))
        screen.blit(player_stand,player_stand_rect)

        score_msg = test_font.render(f'Your score: {score}',False,(111,196,169))
        score_msg_rect = score_msg.get_rect(center=(360,340))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_msg, game_msg_rect)
        else:
            screen.blit(score_msg, score_msg_rect)

    pygame.display.update()
    clock.tick(60)
