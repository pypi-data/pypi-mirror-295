import pygame
from pygame import Surface
import pygame.transform
import random


class Player():
    speed = 0
    JUMP = 15
    jumped = False
    jump_y = 0
    score = 0
    level = 0
    gameover = False
    direction = 2
    def __init__(self,parent,screen:Surface,filename:str, width:int, height:int,flip: bool) -> None:
        self.parent = parent
        self.screen = screen      
        self.img_gameover = None  
        img = pygame.image.load(f'{filename}').convert_alpha()
        if flip:
            self.image_src_l = pygame.transform.scale(img,(width,height))
            self.image_src_r = pygame.transform.flip(self.image_src_l,True,False)
        else:
            self.image_src_r = pygame.transform.scale(img,(width,height))
            self.image_src_l = pygame.transform.flip(self.image_src_r,True,False)
        self.image = self.image_src_r
        self.rect = self.image.get_rect()
        self.game_reset(True)
        self.image_bullet = None
        
        self.msg_level_text = None
        self.msg_score_text = None
        self.mfont30 = pygame.font.SysFont('malgungothic', 30)
        self.mfont40 = pygame.font.SysFont('malgungothic', 40)
        self.mfont50 = pygame.font.SysFont('malgungothic', 50)
        self.mfont60 = pygame.font.SysFont('malgungothic', 60)
        
        # self.set_gameover_image('ghost.png')
        #효과음
        self.snd_dic = {
            'coin':None,
            'jump':None,
            'monster':None,
            'game_over':None,
        }
        
    def set_gameover_image(self,filename):
        img = pygame.image.load(f'{filename}').convert_alpha()
        self.img_gameover = pygame.transform.scale(img,(self.rect.width,self.rect.height))
        
    def game_reset(self, reload_map):
        self.score = 0
        self.level = 1
        self.rect.left = 60
        self.rect.bottom = self.screen.get_height() - 60        
        self.rect_pre = self.rect.copy()
        self.gameover = False
        if reload_map:
            self.parent.map_change(self.level)
    
    def set_bullet_img(self,filename):        
        img = pygame.image.load(f'{filename}').convert_alpha()
        self.image_bullet = pygame.transform.scale(img,(40,30))
        
    def set_snd_coin(self,filename):
        self.snd_dic['coin'] = pygame.mixer.Sound(filename)
        
    def set_snd_jump(self,filename):
        self.snd_dic['jump'] = pygame.mixer.Sound(filename)
        
    def set_snd_game_over(self,filename):
        self.snd_dic['game_over'] = pygame.mixer.Sound(filename)
        
    def set_snd_monster(self,filename):
        self.snd_dic['monster'] = pygame.mixer.Sound(filename)
        
    def jump_process(self):
        dy = 0
        if len(self.parent.group_block)>0:
            self.jump_y += 1
            if self.jump_y > self.JUMP:
                self.jump_y = 1#self.JUMP
            dy = self.jump_y
        else:
            if self.jumped:
                if self.jump_y+1 >= self.JUMP:
                    self.jumped = False
                else:
                    self.jump_y += 1
                    dy = self.jump_y
        return dy
    
    def jump(self):
        if self.jumped == False:
            if self.snd_dic['jump'] is not None:
                self.snd_dic['jump'].play()
            self.jump_y = self.JUMP * (-1)
            self.jumped = True
            if self.image_bullet is not None:
                self.parent.add_bullet(self.image_bullet)
        
    def key_pressed(self):
        if self.speed == 0:
            return
        key_press = pygame.key.get_pressed()
        
        # if len(self.parent.group_block)==0:
        #     if key_press[pygame.K_UP]:
        #         self.rect.centery -= self.speed

        #     if key_press[pygame.K_DOWN]:
        #         self.rect.centery += self.speed
                
        if key_press[pygame.K_LEFT]:
            self.rect.centerx -= self.speed
            
        if key_press[pygame.K_RIGHT]:
            self.rect.centerx += self.speed
            
        if key_press[pygame.K_SPACE]:
            self.jump()
            
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image_src,angle)

    def check_img_dir(self):
        if self.rect_pre.x < self.rect.x:
            self.image = self.image_src_r
            self.direction = 2
        if self.rect_pre.x > self.rect.x:
            self.image = self.image_src_l
            self.direction = -2
            
        
    def check_img_screen_limit(self):        
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.right > self.screen.get_width():
            self.rect.right = self.screen.get_width()
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.bottom > self.screen.get_height():
            self.rect.bottom = self.screen.get_height()
            self.jumped = False
            
    def check_colliderect_blocks(self):        
        dx = self.rect.x - self.rect_pre.x
        dy = self.rect.y - self.rect_pre.y
        self.rect = self.rect_pre.copy()
        
        rect  = self.rect_pre.copy()
        xc = pygame.Rect(rect.x + dx, rect.y, rect.width, rect.height)#앞으로
        yc = pygame.Rect(rect.x, rect.y + dy, rect.width, rect.height)#위로
        yc2 = pygame.Rect(rect.x, rect.y + dy/2, rect.width, rect.height)#위로

        for block in self.parent.group_block:
            
            if block.move_y != 0:
                xc.height -= abs(block.direction)+4
            if block.move_x != 0:
                yc.width -= abs(block.direction)+4
                yc2.width -= abs(block.direction)+4
                
            if block.rect.colliderect(xc):
                dx = 0     
            if block.rect.colliderect(yc):
                col_thresh = block.rect.height/2
                if abs((rect.top + dy) - block.rect.bottom) < col_thresh:#블럭 아래?
                    self.jump_y = 0 
                    dy = block.rect.bottom - rect.top #점프중에면 블럭 아래까지만 점프
                elif abs((rect.bottom + dy) - block.rect.top) < col_thresh:#블럭 위에?
                    rect.bottom = block.rect.top - 1 #블럭위에 올려 놓는다.
                    self.jumped = False #공중에 있으면 초기화
                    dy = 0
                    # if block.move_y != 0:
                    #     dy += block.direction
                    
                    if block.move_x != 0:
                        dx += block.direction

            if block.rect.colliderect(yc2):
                col_thresh = block.rect.height/2
                if abs((rect.top + dy/2) - block.rect.bottom) < col_thresh:#블럭 아래?
                    self.jump_y = 0 #점프 중이면 초기화
                    dy = block.rect.bottom - rect.top #점프중에면 블럭 아래까지만 점프
                elif abs((rect.bottom + dy/2) - block.rect.top) < col_thresh:#블럭 위에?
                    rect.bottom = block.rect.top - 1 #블럭위에 올려 놓는다.
                    self.jumped = False #공중에 있으면 초기화
                    dy = 0
                    if block.move_y != 0:
                        dy += block.direction

        self.rect.x += dx
        self.rect.y += dy        
        self.rect_pre = self.rect.copy()
        
    def game_over_process(self):
        if self.gameover:
            if self.img_gameover is not None and self.rect.bottom > 0:
                offset = self.rect.y
                offset /= 50
                offset = int(offset)
                if offset < 2:
                    offset = 2
                print(offset)
                self.rect.y -= offset
                self.screen.blit(self.img_gameover,self.rect)
            else:
                self.game_reset(True)
            return False
        else:
            return True
        
    def check_collide_all(self):  
        if pygame.sprite.spritecollide(self, self.parent.group_coin, True):
            self.score += 10
            if self.snd_dic['coin'] is not None:
                self.snd_dic['coin'].play()
        #몬스터
        if pygame.sprite.spritecollide(self, self.parent.group_monster, False):
            if self.snd_dic['game_over'] is not None:
                self.snd_dic['game_over'].play()
                # self.game_reset(True)
                self.gameover = True

        # 용암 충돌확인? 
        if pygame.sprite.spritecollide(self, self.parent.group_lava, False):
            if self.snd_dic['game_over'] is not None:
                self.snd_dic['game_over'].play()
                # self.game_reset(True)
                self.gameover = True
            
        if pygame.sprite.spritecollide(self, self.parent.group_exitDoor, False):
            self.level += 1
            
            self.rect.left = 60
            self.rect.bottom = self.screen.get_height() - 60        
            self.rect_pre = self.rect.copy()
            self.level = self.parent.map_change(self.level)
                
    def draw_message(self, msg:str, color:tuple, x:int, y:int):
        msg = f'{msg}'
        img = self.mfont30.render(msg, True, color)
        self.screen.blit(img, (x, y))
    
    def set_msg_score(self, x=10,y=10, color = (0,0,0), text = '점수 : '):
        self.msg_score_x = x
        self.msg_score_y = y
        self.msg_score_color = color
        self.msg_score_text = text
        
    def set_msg_level(self, x=10,y=50, color = (0,0,0), text = '레벨 : '):
        self.msg_level_x = x
        self.msg_level_y = y
        self.msg_level_color = color
        self.msg_level_text = text
        
    def draw(self):
        if self.msg_score_text is not None:
            self.draw_message(f'{self.msg_score_text}{self.score}',
                            self.msg_score_color, 
                            x=self.msg_score_x,
                            y=self.msg_score_y)
        
        if self.msg_level_text is not None:
            self.draw_message(f'{self.msg_level_text}{self.level}',
                            self.msg_level_color, 
                            x=self.msg_level_x,
                            y=self.msg_level_y)
            
        if self.game_over_process():
            self.key_pressed()        
            self.check_img_dir()
            self.rect.y += self.jump_process()
            self.check_img_screen_limit()        
            self.check_colliderect_blocks()        
            self.check_collide_all()
        
            self.screen.blit(self.image, self.rect)
        
        