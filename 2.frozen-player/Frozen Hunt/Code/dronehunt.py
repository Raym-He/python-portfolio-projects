import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
screen_center = pygame.math.Vector2(640,360)
game_active = False

#fonts
font_2p = pygame.font.Font("Fonts/PressStart2P-Regular.ttf",48)
font_2p_smallest = pygame.font.Font("Fonts/PressStart2P-Regular.ttf",28)

#text
font_2p_text = font_2p.render("FROZEN HUNT",False, (0,0,0))
text_rect = font_2p_text.get_rect(center=(640, 180))

space_to_start_text_black = font_2p_smallest.render("Press Space To Start",True,(0,0,0))
space_to_start_text_white = font_2p_smallest.render("Press Space To Start",True,(255,255,255))
which_color_text_timer = 0

#buttons
button_rect = pygame.Rect(540,500,200,70)
font_2p_smaller = pygame.font.Font("Fonts/PressStart2P-Regular.ttf",36)
start_button_font = font_2p_smaller.render("Start",True,(0,0,0))
start_button_font_rect = start_button_font.get_rect(center=(button_rect.center))

#background
background_image = pygame.image.load("Images/backgrounddetailed2.png").convert_alpha()
background_frozen_image = pygame.image.load("Images/backgrounddetailed2blue - Copy.png").convert_alpha()

#sheets
#character_sheet = pygame.image.load('Images/Small-8-Direction-Characters_by_AxulArt.png').convert_alpha()
spider_sheet = pygame.image.load('Images/PunyMonsters/Purple-Spider-32x32.png').convert_alpha()

#spider
spider_sheet_w_or_h = 32
spider_total_frames_list = [] #0 is stationary then 1-7 are different angles
for row in range(8):
    spider_frames_list = []
    for col in range(12):
        spider_sheet_x = spider_sheet_w_or_h * col #gets the last row of spiders
        spider_sheet_y = spider_sheet_w_or_h * row
        spider_cutting_rect = pygame.Rect(spider_sheet_x,spider_sheet_y,32,32)
        spider_frame = spider_sheet.subsurface(spider_cutting_rect)
        spider_frame = pygame.transform.scale(spider_frame, (128, 128))
        spider_frames_list.append(spider_frame)
    spider_total_frames_list.append(spider_frames_list)

spider_spawn_rate = 1

#score
high_score = 0

class Character(pygame.sprite.Sprite):
    def __init__(self,filename, color, screenw, screenh):
        super().__init__()

        #about sheet + cutting
        self.sheet = pygame.image.load('Images/Small-8-Direction-Characters_by_AxulArt.png').convert_alpha()
        self.sheet_width, self.sheet_height = self.sheet.get_size()
        self.frame_width = self.sheet_width // 8
        self.frame_height = self.sheet_height // 12

        self.all_frames = []
        scaled_variable = 5

        if color.lower() == 'white':
            start_row = 1
            end_row = 4
        elif color.lower() == 'blue':
            start_row = 5
            end_row = 9
        elif color.lower() == 'orange':
            start_row = 9 
            end_row = 13

        for animation_row in range(start_row, end_row):
            for col in range(8):
                x_pixel = col * self.frame_width
                y_pixel = (animation_row  * self.frame_height)
                cutting_rect = pygame.Rect(x_pixel, y_pixel, self.frame_width, self.frame_height)
                frame = self.sheet.subsurface(cutting_rect)
                scaled_frame = pygame.transform.scale_by(frame,scaled_variable)
                self.all_frames.append(scaled_frame)

        self.image = self.all_frames[4]
        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-40, -40)
        self.pos = pygame.math.Vector2(screenw//2,screenh//2)
        self.rect.center = (round(self.pos.x),round(self.pos.y))
        self.image_constant = self.all_frames[4]
        self.image_scaled = pygame.transform.scale_by(self.image_constant,2)
        self.image_open_screen = self.image_scaled.get_rect(center=(640, 360))

        #animation timing
        self.frame_index = 0.0
        self.animation_speed = 0.2

        #direction
        self.current_direction = 4
        self.direction_index = {
        (0, -1): 0,   # Up (Row 0)
        (1, -1): 1,   # Up-Right (Row 1)
        (1, 0):  2,   # Right (Row 2)
        (1, 1):  3,   # Down-Right (Row 3)
        (0, 1):  4,   # Down (Row 4)
        (-1, 1): 5,   # Down-Left (Row 5)
        (-1, 0): 6,   # Left (Row 6)
        (-1, -1): 7   # Up-Left (Row 7)
        }

    def update(self):
        #movement keys
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]

        if (dx, dy) != (0,0):
            self.current_direction = self.direction_index[(dx ,dy)]
            self.frame_index += self.animation_speed
            frame_num = int(self.frame_index) % 3
            self.image = self.all_frames[(frame_num * 8) + self.current_direction]
        else:
            self.frame_index = 0
            self.image = self.all_frames[self.current_direction]

        self.pos += pygame.math.Vector2(dx, dy) * 4
        self.rect.center = (round(self.pos.x),round(self.pos.y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self,frames,world_pos_x, world_pos_y):
        super().__init__()
        self.frames = frames
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-30, -30)
        self.pos = pygame.math.Vector2(world_pos_x, world_pos_y)
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.speed = 1.5
        #animation
        self.animation_speed = 0.05
        self.all_frames = []
        self.frame_index = 0
        self.current_direction = 0

    def update(self,player_pos,is_frozen):
        #freeze
        if is_frozen:
            return
        #follows the player
        direction = player_pos - self.pos
        if direction.length() > 0 :
            direction = direction.normalize()
            self.pos += direction * self.speed

        #finds (dx,dy) for animation
        if direction.x > 0.3:
            dx = 1
        elif direction.x < -0.3:
            dx = -1
        else:
            dx = 0

        if direction.y > 0.3:
            dy = 1
        elif direction.y < -0.3:
            dy = -1
        else:
            dy = 0

        self.direction_index = {
                (0, -1): 4,   # up (Row 4)
                (1, -1): 3,   # Up-Right (Row 3)
                (1, 0):  2,   # Right (Row 2)
                (1, 1):  1,   # Down-Right (Row 1)
                (0, 1):  0,   # Down (Row 0)
                (-1, 1): 7,   # Down-Left (Row 7)
                (-1, 0): 6,   # Left (Row 6)
                (-1, -1): 5   # Up-Left (Row 5)
                }

        if (dx,dy) in self.direction_index:
            self.current_direction = self.direction_index[(dx,dy)]
            self.frame_index += self.animation_speed
            self.frames_num = int(self.frame_index % 12)
            self.image = spider_total_frames_list[self.current_direction][self.frames_num]
    
        self.rect.center = (round(self.pos.x),round(self.pos.y))

          
#Frozen stuff
is_frozen = False
normal_timer = 0
frozen_timer = 0
game_frozen = 175 #(2s which is 60fps twice)
game_unfrozen = 300 #(5s)

#spawn rate
spider_spawn_timer = 0
spawn_interval = 90 #(1.5s)

#SPITES-character
character = Character('Images/Small-8-Direction-Characters_by_AxulArt.png','white',1280,720)
player_group = pygame.sprite.Group()
player_group.add(character)
character_center_rect = character.image.get_rect(center=(screen_center.x, screen_center.y))

#SPITES-spider
spider_group = pygame.sprite.Group()

while running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_active:
                if button_rect.collidepoint(event.pos):
                    game_active = True
                    start_ticks = pygame.time.get_ticks()
        if event.type == pygame.KEYDOWN:
            if not game_active:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_ticks = pygame.time.get_ticks()


    if game_active:
        #camera offset        
        camera_offset = character.pos - screen_center

        #frozen mechanics
        if not is_frozen:
            normal_timer += 1
            current_bg = background_image
            if normal_timer >= game_unfrozen:
                normal_timer = 0
                spider_spawn_rate = 1
                is_frozen = True
        elif is_frozen:
            frozen_timer += 1
            current_bg = background_frozen_image
            if frozen_timer >= game_frozen:
                frozen_timer = 0
                spider_spawn_rate = 20
                is_frozen = False
    
        #inf background
        start_bg_x = int(camera_offset.x // 500) - 1
        end_bg_x = int((camera_offset.x + 1280 )// 500) + 2
        start_bg_y = int(camera_offset.y // 500) - 1
        end_bg_y = int((camera_offset.y + 720 ) // 500) + 2

        for x in range(start_bg_x, end_bg_x):
            for y in range(start_bg_y, end_bg_y):
                bg_tile_x = x * 500
                bg_tile_y = y * 500
                
                tile_screen_x = bg_tile_x - camera_offset.x
                tile_screen_y = bg_tile_y - camera_offset.y

                screen.blit(current_bg, (tile_screen_x, tile_screen_y))

        #character
        player_group.update()
        screen.blit(character.image,character_center_rect)

        #spider
        spider_spawn_timer += spider_spawn_rate
        if spider_spawn_timer >= 90:
            spider_spawn_timer = 0
            side = random.choice(["left","right","top","bottom"])

            if side == "left":
                spider_spawn_x = character.pos.x - 800
                spider_spawn_y = character.pos.y + random.randint(-400,400)
            elif side == "right":
                spider_spawn_x = character.pos.x + 800
                spider_spawn_y = character.pos.y + random.randint(-400,400)
            elif side == "top":
                spider_spawn_y = character.pos.y - 400
                spider_spawn_x = character.pos.x + random.randint(-800,800)
            elif side == "bottom":
                spider_spawn_y = character.pos.y + 400
                spider_spawn_x = character.pos.x + random.randint(-800,800)

            spawned_spiders = Enemy(spider_frames_list,spider_spawn_x,spider_spawn_y)
            spider_group.add(spawned_spiders)

        for spider in spider_group:
            spider_screen_pos = spider.pos - camera_offset
            screen_rect = spider.image.get_rect(center=(round(spider_screen_pos.x) ,round(spider_screen_pos.y)))
            screen.blit(spider.image, screen_rect)
        spider_group.update(character.pos,is_frozen)

        #checks collisions
        hit_spider = pygame.sprite.spritecollideany(character,spider_group)
        if hit_spider:
            game_active = False
            spider_group.empty()
            spider_spawn_timer = 0
            character.pos = pygame.math.Vector2(640,360)
            if survival_time > high_score:
                high_score = survival_time

        #score
        survival_time = (pygame.time.get_ticks() - start_ticks) // 1000
        score_surface = font_2p_smaller.render(f"Score:{survival_time}",True, (255,255,255))
        score_rect = score_surface.get_rect(topleft=(20,20))
        screen.blit(score_surface,score_rect)
        pygame.display.flip()
        clock.tick(60) 
    else:  
        #backgorund
        for x in range(-1,3):
            for y in range(-1,3):
                screen.blit(background_image,(x * 500, y * 500))
        #screen.fill("grey")
        screen.blit(font_2p_text,text_rect)
        screen.blit(character.image_scaled,character.image_open_screen)

        #button
        pygame.draw.rect(screen,(0,150,0),button_rect) 
        pygame.draw.rect(screen,(255,255,255),button_rect,3)
        screen.blit(start_button_font,start_button_font_rect)

        #text
        which_color_text_timer += 0.1
        if int((which_color_text_timer % 2)) == 1:
            text_color = space_to_start_text_black
            text_color_rect = text_color.get_rect(center=(640, 650))
        else:
            text_color = space_to_start_text_white
            text_color_rect = text_color.get_rect(center=(640, 650))
        screen.blit(text_color,text_color_rect)

        #text-score
        high_score_surface = font_2p_smallest.render(f"High Score:{high_score}",True,(0,0,0))
        high_score_text_rotate = pygame.transform.rotate(high_score_surface,25.5)
        high_score_rect = high_score_text_rotate.get_rect(center = (360,360))
        screen.blit(high_score_text_rotate,high_score_rect)
        pygame.display.flip()
        clock.tick(60) 