# Importing modules: Pygame for actual game, sys for managing system, random to determine where the coin will appear, time for the in-game timer
import pygame
import sys
import random
import time

# Initializing Pygame
pygame.init()

# Setting up score
score = 0

# Setting up screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Setting up game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car game")


# Grass on outside
screen.fill('#00FF00')

# Set up text
game_font = pygame.font.SysFont('arial', 16)

# Set up timer
start_time = time.time()
elapsed_time = 0



# Set Up Road (just a gray rectangle)
road_width = 600
road_color = '#787878'
road = pygame.Rect(SCREEN_WIDTH/2 - road_width/2, 0, road_width, SCREEN_HEIGHT)


# Set up coin
coin_height = 25
coin_width = 25
coin_speed = 5
coin_color = '#FFFF00'
coin = pygame.Rect(SCREEN_WIDTH/2, 0 - coin_height, coin_width, coin_height)

# Set up car
car = pygame.transform.scale(pygame.transform.rotate(pygame.image.load("car.png"), -90), (50, 100)) # I had to make the car smaller and rotate it 90 degrees to the left
car_rect = car.get_rect(midbottom=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 50))
car_speed = 5

# Set Up FPS timer
clock = pygame.time.Clock()

running = True

# Game Loop
while running:
    # Update timer
    current_time = time.time()
    elapsed_time = current_time - start_time
    time_left = 60 - elapsed_time
    
    # Check if user pressed the red X on top-right
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Text
    score_text = game_font.render(f'Score: {score} \n Time: {round(time_left)}', True, 'white', 'orange')
    gameover_text = game_font.render('Game Over!', True, 'black', 'red')
    
    # Render Surfaces
    pygame.draw.rect(screen, road_color, road)
    pygame.draw.ellipse(screen, coin_color, coin)
    screen.blit(car, car_rect)
    screen.blit(score_text,(SCREEN_HEIGHT/2,10))
    pygame.display.update()

    # Get User Input w/o car moving offscreen
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_rect.x - car_speed >= 100:
        car_rect.x -= car_speed
    
    if keys[pygame.K_RIGHT] and car_rect.x + car_speed - car_rect.width <= 600:
        car_rect.x += car_speed
    
    
    # Coin Code
    coin.y += coin_speed
    if coin.top > SCREEN_HEIGHT:
        coin.y = 0 - coin_height
        coin.x = random.randint(100, 600)
    
    # Checking if coin hits car and adding 1 point if so
    if coin.colliderect(car_rect):
        coin.y = 0 - coin_height
        coin.x = random.randint(100, 600)
        score += 1
        if coin_speed + 0.3 < 10:
            coin_speed += 0.3
    
    # Ending the game when out of time
    if time_left <= 0.1:
        screen.blit(gameover_text, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        pygame.time.delay(4000)
        
        # Exiting the game and printing score on console
        running = False
        print('\n'*100)
        print(f'You got {score} points!')
    
    
    # Setting framerate + updating the display
    clock.tick(60)
    pygame.display.flip()


# Ending the game at the end
pygame.quit()
sys.exit()
