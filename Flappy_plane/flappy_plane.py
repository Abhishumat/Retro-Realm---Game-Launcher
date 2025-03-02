import pygame
import random
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
BG = (255, 255, 255)
BLACK = (0, 0, 0)

# Gravity
GRAVITY = 0.25

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Airplane')

# Load images
airplane_img = pygame.image.load('real.png') 
airplane_img = pygame.transform.scale(airplane_img, (50, 50))
building_top_img = pygame.image.load('building.jpg')
building_bottom_img = pygame.image.load('building.jpg')
crash_img = pygame.image.load('image-removebg-preview.png')  
crash_img = pygame.transform.scale(crash_img, (50, 50))
post_crash_img = pygame.image.load('lol.png')
post_crash_img = pygame.transform.scale(post_crash_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Clock object to control FPS
clock = pygame.time.Clock()

# Scoreboard variables
scor1 = score = 0
font = pygame.font.Font(None, 36)  # Default font with size 36

class Airplane:
    def __init__(self):
        self.rect = pygame.Rect(100, SCREEN_HEIGHT // 2, 50, 50)
        self.speed = 0

    def update(self):
        self.speed += GRAVITY
        self.rect.y += self.speed

        # Prevent airplane from falling off the screen
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.speed = 0

        # Prevent airplane from going above the screen
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed = 0

    def jump(self):
        self.speed = -5

class Building:
    def __init__(self, x):
        self.width = 70
        self.gap_height = 200
        self.top_height = random.randint(50, SCREEN_HEIGHT - self.gap_height - 50)
        self.bottom_height = SCREEN_HEIGHT - self.top_height - self.gap_height
        self.top_rect = pygame.Rect(x, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(x, SCREEN_HEIGHT - self.bottom_height, self.width, self.bottom_height)

    def update(self):
        self.top_rect.x -= 2
        self.bottom_rect.x -= 2

    def draw(self):
        screen.blit(pygame.transform.scale(building_top_img, (self.width, self.top_height)), self.top_rect)
        screen.blit(pygame.transform.scale(building_bottom_img, (self.width, self.bottom_height)), self.bottom_rect)

airplane = Airplane()
buildings = [Building(400)]

running = True
crashed = False
crash_timer = 0
OK = pygame.image.load('sky.jpg')
while running:
    screen.blit(pygame.transform.scale(pygame.image.load('sky.jpg'),(400,600)),(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                airplane.jump()

    if not crashed:
        airplane.update()
        for building in buildings:
            building.update()
            building.draw()

        # Draw airplane
        screen.blit(airplane_img, (airplane.rect.x, airplane.rect.y))

        # Check for collision
        for building in buildings:
            if airplane.rect.colliderect(building.top_rect) or airplane.rect.colliderect(building.bottom_rect):
                crashed = True
                crash_timer = pygame.time.get_ticks()
                screen.blit(crash_img, (airplane.rect.x, airplane.rect.y))  # Show crash image
            elif building.top_rect.x + building.width < airplane.rect.x and not crashed:
                scor1 += 0.03
                score = int(scor1)

        # Add new buildings
        if buildings[-1].top_rect.x < SCREEN_WIDTH - 200:
            buildings.append(Building(SCREEN_WIDTH))

        # Remove off-screen buildings
        if buildings[0].top_rect.x < -buildings[0].width:
            buildings.pop(0)
    else:
        # Draw crash image
        screen.blit(crash_img, (airplane.rect.x, airplane.rect.y))
        if pygame.time.get_ticks() - crash_timer > 1000:  # Show crash image for 1 second
            # Display "You Lost" message
            lost_text = font.render('You Lost!', True, BLACK)
            screen.blit(lost_text, (SCREEN_WIDTH // 2 - lost_text.get_width() // 2, SCREEN_HEIGHT // 2 - lost_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(2000)  # Display the message for 2 seconds
            running = False

    # Render the score
    score_text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
