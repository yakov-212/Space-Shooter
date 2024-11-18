from typing import Any
import pygame
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image = pygame.image.load("images/player.png").convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + WINDOW_HEIGHT/4))
        self.speed = 450
        self.direction = pygame.math.Vector2(0,0)

        self.can_shoot = True
        self.laser_shoot_time = 0
        #laser shootingrate
        self.cooldown_duration =250
        
    
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
        

    def update(self,dt):
        keys = pygame.key.get_pressed()
        set_keys = pygame.key.get_just_pressed()
        self.rect.center += self.direction * self.speed * dt
        if WINDOW_WIDTH >= self.rect.right and self.rect.left >= 0 and WINDOW_HEIGHT >= self.rect.bottom and self.rect.top >= 0:
            self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
            self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        elif WINDOW_WIDTH < self.rect.right:
            self.rect.right = WINDOW_WIDTH -5
        elif self.rect.left < 0:
            self.rect.left = 5
        elif WINDOW_HEIGHT < self.rect.bottom:
            self.rect.bottom = WINDOW_HEIGHT -5
        elif self.rect.top < 0:
            self.rect.top = 5

        self.direction = self.direction.normalize() if self.direction else self.direction
        if set_keys[pygame.K_SPACE] and self.can_shoot:
            laser_sound.play() 
            Laser((all_sprites,laser_sprites),laser_surf,self.rect.midtop)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        self.laser_timer()
    
class Star(pygame.sprite.Sprite):
    def __init__(self,groups,surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(20 ,WINDOW_WIDTH),randint(20,WINDOW_HEIGHT)))
        self.exists = pygame.time.get_ticks()
        self.killtime = 3000


    
    # def update(self,dt):
    #     # self.rect.centery += 700 *dt
    #     # if pygame.time.get_ticks() - self.killtime >= self.exists:
    #     #     self.kill()


class Metor(pygame.sprite.Sprite):
    def __init__(self,groups,surf,pos):
        super().__init__(groups)
        self.original_image = surf
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.killtime = 3000
        self.exists = pygame.time.get_ticks()
        self.direction = pygame.Vector2(uniform(-0.5,0.5),1)
        self.speed = randint(400,500)
        self.rotation = 0
        self.rotation_speed = randint(50,100)

    def update(self,dt):
        self.rect.center += self.direction* self.speed * dt
        if pygame.time.get_ticks() - self.killtime >= self.exists:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_image,self.rotation,1)
        self.rect = self.image.get_frect(center = self.rect.center)

class Laser(pygame.sprite.Sprite):
    def __init__(self,group,surf,pos):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
    
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()
            

class AnimatedExolosion(pygame.sprite.Sprite):
    def __init__(self,groups,frames,pos):
        super().__init__(groups)
        self.frames = frames
        self.frames_index = 0
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_frect(center= pos)

    def update(self,dt):
        self.frames_index += 25 * dt
        if self.frames_index < len(self.frames):
            self.image = self.frames[int(self.frames_index) % len(self.frames)]
        else:
            self.kill()
    

        


def collisions():
        global start
        if pygame.sprite.spritecollide(player,metor_sprites,False,pygame.sprite.collide_mask):
            start = False
        for laser in laser_sprites:
            collided_sprites = pygame.sprite.spritecollide(laser,metor_sprites,True)
            if collided_sprites:
                laser.kill()
                explosion_sound.play()
                AnimatedExolosion(all_sprites,explosion_frames,laser.rect.midtop)

def display_score():
    current_time = pygame.time.get_ticks() // 50
    ticks = current_time - start_tick
    text_surface = score_font.render(str(ticks),True,(200,220,235))
    text_rect = text_surface.get_frect(midbottom= (WINDOW_WIDTH/2, WINDOW_HEIGHT-50))
    pygame.draw.rect(display_surface,(200,220,235),text_rect.inflate(20,10).move(0,-8), 5, 10)
    display_surface.blit(text_surface,text_rect)





#general setup
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.RESIZABLE)



pygame.display.set_caption("Space Shooter")
leave = False
start = False
countdown_start = False
count = 239
clock = pygame.time.Clock()




#import
meteor_surf = pygame.image.load("images/meteor.png").convert_alpha()
laser_surf = pygame.image.load("images/laser.png").convert_alpha()
star_surf = pygame.image.load("images/star.png").convert_alpha()
explosion_frames = [pygame.image.load(f"images/explosion/{i}.png").convert_alpha()
                     for i in range(21)]

#audio imports
game_music = pygame.mixer.Sound("audio/game_music.wav")
game_music.set_volume(.15)
game_music.play(loops= -1)
explosion_sound = pygame.mixer.Sound("audio/explosion.wav")
explosion_sound.set_volume(.1)
laser_sound = pygame.mixer.Sound("audio/laser.wav")
laser_sound.set_volume(.12)
damage_sound = pygame.mixer.Sound("audio/damage.ogg")

#fonts
score_font = pygame.font.Font("images/Oxanium-Bold.ttf",40)
start_font = pygame.font.Font("images/Oxanium-Bold.ttf",60)
count_font = pygame.font.Font("images/Oxanium-Bold.ttf",120)

#start button 
start_surf = start_font.render("Start Game",True,"Red")
start_rect = start_surf.get_rect(center= (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))





#sprites
all_sprites = pygame.sprite.Group()
metor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
star_sprites = pygame.sprite.Group()
for i in range(20):
    Star((all_sprites,star_sprites),star_surf)
player = Player(all_sprites)




#metor event
metor_event = pygame.event.custom_type()
pygame.time.set_timer(metor_event,200)

# star_event = pygame.event.custom_type()
# pygame.time.set_timer(star_event, 50)



#starting screen
while not leave:
    dt = clock.tick() / 1000
    display_surface.fill("#3a2e3f")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            leave = True
            start = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect.collidepoint(start_rect.inflate(20,20).move(0,-8),(pygame.mouse.get_pos())):
                countdown_start = True
                start = True
        elif event.type == pygame.VIDEORESIZE:
            screen_info = pygame.display.Info()
            WINDOW_WIDTH, WINDOW_HEIGHT = screen_info.current_w, screen_info.current_h
            pygame.time.set_timer(metor_event,75)


 
    if not countdown_start:
        start_border = pygame.draw.rect(display_surface,"Blue",start_rect.inflate(20,20).move(0,-8))
        display_surface.blit(start_surf,start_rect)
        start_rect.center = WINDOW_WIDTH/2,WINDOW_HEIGHT/2
    elif countdown_start:
        dt = clock.tick(60) 
        count_surf = count_font.render(str(count//60),True,(200,220,235))
        count_frect = count_surf.get_frect(center= (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        count -= 1
        display_surface.blit(count_surf,count_frect)
        if count// 60 < 1:
            leave = True


    star_sprites.draw(display_surface)
    pygame.display.update()

start_tick = pygame.time.get_ticks() // 50
#game play
while start:
    dt = clock.tick() / 1000

    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            
        if event.type == metor_event:
            metor = Metor((all_sprites,metor_sprites),meteor_surf,(randint(0,WINDOW_WIDTH), randint(-200,-100)))
        # elif event.type == star_event:
        #     Star((all_sprites,star_sprites),star_surf)
        if event.type == pygame.VIDEORESIZE:
            screen_info = pygame.display.Info()
            WINDOW_WIDTH, WINDOW_HEIGHT = screen_info.current_w, screen_info.current_h
            pygame.time.set_timer(metor_event,75)

    collisions()
    
    #update
    all_sprites.update(dt)



    #draw the game
    display_surface.fill("#3a2e3f")
    display_score()
    all_sprites.draw(display_surface)
    
    pygame.display.update()


pygame.quit()