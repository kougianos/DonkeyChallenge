# Pygame development

import pygame
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'DONKEY CHALLENGE'

WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

clock = pygame.time.Clock()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (450,50)
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)

class Game:
    TICK_RATE = 60 #fps

    def __init__(self, image_path, title, width, height, high_score): #constructor
        self.title = title
        self.width = width
        self.height = height
        self.high_score = high_score
        self.game_screen = pygame.display.set_mode((width, height))
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)

        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))

    def run_game_loop(self, level_speed):  #game loop
        is_game_over = False
        did_win = False
        direction = 0

        
        player_character = PlayerCharacter('donkey.png', 375, 700, 50, 50)   #creating game character
        
        enemy0 = NonPlayerCharacter('superEnemy.png',  20, 600, 50, 50)
        enemy0.SPEED *= level_speed
        enemy1 = NonPlayerCharacter('superEnemy.png',  780, 400, 50, 50)
        enemy1.SPEED *= level_speed
        enemy2 = NonPlayerCharacter('superEnemy.png',  20, 200, 50, 50)
        enemy2.SPEED *= level_speed
        
        treasure = GameObject('corn.png',  375, 50, 50, 50)
        while not is_game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True
                elif event.type == pygame.KEYDOWN:  #when pressing a key
                    if event.key == pygame.K_ESCAPE:
                        is_game_over = True
                    if event.key == pygame.K_UP:
                        direction = 1  
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                    elif event.key == pygame.K_RIGHT:
                        direction = 2
                    elif event.key == pygame.K_LEFT:
                        direction = 3
                elif event.type == pygame.KEYUP:  #when releasing a key
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        direction = 0
                    
                print(event)   #printing all events on terminal

            self.game_screen.fill(WHITE_COLOR)
            self.game_screen.blit(self.image, (0,0))
            
            player_character.move(direction, self.height, 0, self.width, 0)
            player_character.draw(self.game_screen)

            treasure.draw(self.game_screen)

            
            enemy0.move(self.width)
            enemy0.draw(self.game_screen)
            if self.high_score >= 4:
                enemy1.move(self.width)
                enemy1.draw(self.game_screen)
            if self.high_score >= 8:
                enemy2.move(self.width)
                enemy2.draw(self.game_screen)

            high_score_render = font.render("%d" %self.high_score , True, WHITE_COLOR)
            self.game_screen.blit(high_score_render, (5, 5))
            pygame.display.update()

            if player_character.detect_collision(enemy0) or player_character.detect_collision(enemy1) or player_character.detect_collision(enemy2):
                is_game_over = True
                did_win = False
                text = font.render('You suck', True, BLACK_COLOR)
                self.game_screen.blit(text, (300, 350))
                pygame.display.update()
                clock.tick(1)
                break
            elif player_character.detect_collision(treasure):
                is_game_over = True
                did_win = True
                self.high_score += 1
                text = font.render('You win', True, BLACK_COLOR)
                self.game_screen.blit(text, (300, 350))
                pygame.display.update()
                clock.tick(1)
                break

            
            pygame.display.update()  # similar to flip
            clock.tick(self.TICK_RATE)

        if did_win:
            #alternate way: level speed += 0.5 and self.run_game_loop(level_speed)
            self.run_game_loop(level_speed + 0.3)
        else:
            return

class GameObject:

    def __init__(self, image_path,  x, y, width, height):
        object_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(object_image, (width, height))
         
        self.x_pos = x
        self.y_pos = y

        self.width = width
        self.height = height
        
    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))


class PlayerCharacter(GameObject):
    
    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)
    
    def move(self, direction, max_height, min_height, max_width, min_width):
        if direction == 1:
            self.y_pos -= self.SPEED
        elif direction  == -1:
            self.y_pos += self.SPEED
        elif direction == 2:
            self.x_pos += self.SPEED
        elif direction == 3:
            self.x_pos -= self.SPEED
        if self.y_pos >= max_height - 50:
            self.y_pos = max_height - 50
        if self.y_pos <= min_height:
            self.y_pos = min_height
        if self.x_pos >= max_width - 50:
            self.x_pos = max_width - 50
        if self.x_pos <= min_width:
            self.x_pos = min_width
        

    def detect_collision( self, other_body):
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False
        
        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False

        return True


class NonPlayerCharacter(GameObject):
    
    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)
    
    def move(self, max_width):
        if self.x_pos <= 1:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >= max_width - 50:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED
        

pygame.init()

new_game = Game('background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT , 0)
new_game.run_game_loop(1)

pygame.quit()
quit()

