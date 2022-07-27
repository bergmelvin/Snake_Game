import pygame
import random
import time
from pygame.locals import *
from collections import namedtuple
from enum import Enum



pygame.init()
font = pygame.font.SysFont('comicsans', 30)

class Direction(Enum):
    RIGTH = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', ['x', 'y'])

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
BLOCK_WIDTH = 1
SPEED = 10
class Snake_Game:
    def __init__(self, width=800, height=800):
        self.w = width
        self.h = height

        # Init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        # Init game state
        self.direction = Direction.RIGTH

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.y - (2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self): # Helper function
        x = random.randint(0, (self.w - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        
        if self.food in self.snake: # We do not want to place the food inside the snake
            self._place_food()
    
    
    
    def play_step(self):
        # 1. Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == K_RIGHT:
                    self.direction = Direction.RIGTH
                elif event.key == K_DOWN:
                    self.direction = Direction.DOWN
                elif event.key == K_UP:
                    self.direction = Direction.UP
            
        # 2. Move
        self._move(self.direction) # Update the head
        self.snake.insert(0, self.head) # Insert the updated head :)
        
        # 3. Check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. Place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED) # Frame update

        # 6. return game over and score
        return game_over, self.score

    
    def _is_collision(self):
        # Check if hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True

        # Check if hits itself
        if self.head in self.snake[1:]:
            return True
        
        return False
    
    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE), BLOCK_WIDTH)
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x+4, pt.y+4, 12, 12), BLOCK_WIDTH)
        
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
    
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGTH:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        
        self.head = Point(x, y)

if __name__ == '__main__':
    game = Snake_Game()
    
    # Game loop
    game_over = False
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

        


    print(f'Your final score: {score}')    
    
    pygame.quit()





