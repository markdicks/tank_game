import pygame

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TANK_WIDTH = 32
TANK_HEIGHT = 32
OBSTACLE_WIDTH = 64
OBSTACLE_HEIGHT = 64
ENEMY_TANK_WIDTH = 32
ENEMY_TANK_HEIGHT = 32
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank Game")

# Create the tank sprite
class Tank(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((TANK_WIDTH, TANK_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH / 2 - TANK_WIDTH / 2
        self.rect.y = SCREEN_HEIGHT - TANK_HEIGHT - 10
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

# Create the obstacle sprite
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create the enemy tank sprite
class EnemyTank(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((ENEMY_TANK_WIDTH, ENEMY_TANK_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH / 2 - ENEMY_TANK_WIDTH / 2
        self.rect.y = 10

    def update(self):
        self.rect.y += 1

# Create the groups for the sprites
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# Create the player's tank and add it to the all_sprites group
player_tank = Tank()
all_sprites.add(player_tank)

# Create the obstacles and add them to the all_sprites and obstacles groups
obstacle1 = Obstacle(SCREEN_WIDTH / 2 - OBSTACLE_WIDTH / 2, SCREEN_HEIGHT / 2 - OBSTACLE_HEIGHT / 2)
obstacle2 = Obstacle(100, 100)
all_sprites.add(obstacle1, obstacle2)
obstacles.add(obstacle1, obstacle2)

# Create the enemy tank and add it to the all_sprites group
enemy_tank = EnemyTank()
all_sprites.add(enemy_tank)

# Create the font for the pause menu
font = pygame.font.SysFont(None, 50)

# Create the game loop
clock = pygame.time.Clock()
running = True
paused = False
# Game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused

    # If the game is paused, skip everything else in the loop
    if paused:
        continue

    # Get the keys currently pressed
    keys = pygame.key.get_pressed()

    # Update the tank based on the keys pressed
    player_tank.update(keys)

    # Update the enemy tank
    enemy_tank.update()

    # Check for collisions between the player tank and obstacles
    collisions = pygame.sprite.spritecollide(player_tank, obstacles, False)
    if collisions:
        player_tank.rect.clamp_ip(collisions[0].rect)

    # Draw everything to the screen
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Draw the pause menu if the game is paused
    if paused:
        pause_text = font.render("Paused", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(pause_text, pause_rect)

    # Flip the display
    pygame.display.flip()

    # Wait for the next frame
    clock.tick(FPS)

# Clean up Pygame
pygame.quit()
