import pygame
import random
from enum import Enum
from collections import namedtuple
import time
import sys

pygame.init()
font= pygame.font.Font('arial.ttf',25)

DIFFICULTY=0

class Direction(Enum):
    RIGHT=1
    LEFT=2
    UP=3
    DOWN=4

Point=namedtuple('Point', 'x, y')

BLACK=(0, 0, 0)
WHITE=(255, 255, 255)
BLUE=(0, 0, 255)
DARKBLUE=(0, 100, 255)
RED=(200, 0, 0)
SPEED=5
BLOCK_SIZE=20

class SnakeEnvironment:
    def __init__(self, w=640, h=480):
        self.w=w
        self.h=h

        self.mainmenu()
        
        self.display=pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Snake Game')
        
        
        self.clock=pygame.time.Clock()

        self.direction=Direction.RIGHT

        self.head=Point(self.w/2,self.h/2)
        self.snake=[self.head, Point(self.head.x-BLOCK_SIZE, self.head.y),Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score=0
        self.food=None
        self.place_food()
    
    def mainmenu(self):
        global DIFFICULTY
        self.display=pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Welcome to the Snake Game')
        font= pygame.font.Font('arial.ttf',40)
        
        text=font.render("MAIN MENU", False, WHITE)
        self.display.blit(text, [self.w/3.5, self.h/8])
        font= pygame.font.Font('arial.ttf',25)
        text=font.render("Select Difficulty", False, WHITE)
        self.display.blit(text, [self.w/3.5, self.h/3.5])
        text=font.render("1) Easy", False, WHITE)
        self.display.blit(text, [self.w/3.5, self.h/2.5])
        text=font.render("2) Medium", False, WHITE)
        self.display.blit(text, [self.w/3.5, self.h/2.1])
        text=font.render("3) Hard", False, WHITE)
        self.display.blit(text, [self.w/3.5, self.h/1.82])
        text=font.render("Enter A KEY", False, WHITE)
        self.display.blit(text, [self.w/3.5, self.h/1.6])
        pygame.display.flip()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_1:
                    DIFFICULTY=1
                    break
                if event.key==pygame.K_2:
                    DIFFICULTY=2
                    break
                if event.key==pygame.K_3:
                    DIFFICULTY=3
                    break
                
    
    def place_food(self):
        x=random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y=random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food=Point(x,y)
        if self.food in self.snake:
            self.place_food()
    
    def step(self):
        global SPEED
    
    #DEFINE MOVEMENT
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()        
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    self.direction=Direction.LEFT
                elif event.key==pygame.K_RIGHT:
                    self.direction=Direction.RIGHT
                if event.key==pygame.K_UP:
                    self.direction=Direction.UP
                if event.key==pygame.K_DOWN:
                    self.direction=Direction.DOWN
        
        self.move(self.direction)
        self.snake.insert(0, self.head) #update the head

        #check gameover
        game_over=False
        if self.is_collision():
            game_over=True
            return game_over,score

        #place new food
        if self.head==self.food:
            self.score+=1
            if(DIFFICULTY==2):
                SPEED+=1
            elif(DIFFICULTY==3):
                SPEED+=2
            self.place_food()
        
        else:
            self.snake.pop()

        self.updateUI()
        self.clock.tick(SPEED)


        game_over=False
        return game_over,self.score
    
    def updateUI(self):
        self.display.fill(BLACK)

        for point in self.snake:
            pygame.draw.rect(self.display, BLUE, pygame.Rect(point.x,point.y, BLOCK_SIZE,BLOCK_SIZE))
            pygame.draw.rect(self.display, DARKBLUE, pygame.Rect(point.x+4,point.y+4, 12,12))
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x,self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        text=font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        if DIFFICULTY==1:
            text=font.render("Difficulty: Easy" , True, WHITE)
            self.display.blit(text, [460, 0])
        elif DIFFICULTY==2:
            text=font.render("Difficulty: Medium" , True, WHITE)
            self.display.blit(text, [435, 0])
        elif DIFFICULTY==3:
            text=font.render("Difficulty: Hard" , True, WHITE)
            self.display.blit(text, [460, 0])
        pygame.display.flip()
    
    def move(self, direction):
        x=self.head.x
        y=self.head.y
        if direction==Direction.LEFT:
            x-=BLOCK_SIZE
        if direction==Direction.RIGHT:
            x+=BLOCK_SIZE
        if direction==Direction.UP:
            y-=BLOCK_SIZE
        if direction==Direction.DOWN:
            y+=BLOCK_SIZE

        self.head=Point(x,y)
    
    def is_collision(self):
        if self.head.x>(self.w-BLOCK_SIZE) or self.head.x<0 or self.head.y>(self.h-BLOCK_SIZE) or self.head.y<0:
            return True
        
        if self.head in self.snake[1:]:
            return True
        
        return False

if __name__=='__main__':
    
    
    game=SnakeEnvironment()

    while True:
        game_over,score=game.step()

        if game_over==True:
            break

    print("Score: ", score)

    pygame.quit()
    sys.exit() 