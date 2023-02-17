import pygame
import random
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set the width and height of the screen [width, height]
WIDTH = 700
HEIGHT = 500
FPS = 60

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Game")

# Define the tank class
class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.direction = "down"
        self.lives = 3
        self.bullets = pygame.sprite.Group()

    def update(self, obstacles):
        # Update the tank's position
        if self.direction == "left":
            self.rect.x -= self.speed
            if self.rect.x < 0:
                self.rect.x = 0
        elif self.direction == "right":
            self.rect.x += self.speed
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
        elif self.direction == "up":
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.rect.y = 0
        elif self.direction == "down":
            self.rect.y += self.speed
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT

        # Check for collisions with obstacles
        obstacle_collisions = pygame.sprite.spritecollide(self, obstacles, False)
        for obstacle in obstacle_collisions:
            if self.direction == "left":
                self.rect.left = obstacle.rect.right
            elif self.direction == "right":
                self.rect.right = obstacle.rect.left
            elif self.direction == "up":
                self.rect.top = obstacle.rect.bottom
            elif self.direction == "down":
                self.rect.bottom = obstacle.rect.top

        # Update the tank's bullets
        self.bullets.update(obstacles)

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
        self.bullets.add(bullet)

# Define the enemy tank class
class EnemyTank(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3
        self.player = player
        self.bullets = pygame.sprite.Group()

    def update(self, obstacles):
        # Move towards the player
        self.move_towards_player()

        # Update the enemy tank's bullets
        self.bullets.update(obstacles)

    def move_towards_player(self):
        dx = self.player.rect.x - self.rect.x
        dy = self.player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx = dx / dist
            dy = dy / dist
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def shoot(self):
        if pygame.time.get_ticks() - self.last_shot_time > self.shot_cooldown:
            # Reset the cooldown timer
            self.last_shot_time = pygame.time.get_ticks()

            # Create a new bullet object
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)

            # Add the bullet to the appropriate group
            all_sprites.add(bullet)
            bullets.add(bullet)

            # Play the shooting sound effect
            shooting_sound.play()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()

        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.direction = direction
        self.speed = 10

    def update(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        # Remove the bullet if it goes off the screen
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

class EnemyTank(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()

        self.image = pygame.Surface((TANK_WIDTH, TANK_HEIGHT))
        self.image.fill(ENEMY_TANK_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = ENEMY_TANK_SPEED
        self.player = player
        self.direction = "down"
        self.last_shot_time = 0
        self.shot_cooldown = ENEMY_SHOT_COOLDOWN

    def move_towards_player(self):
        if self.player.rect.centerx < self.rect.centerx:
            self.rect.x -= self.speed
            self.direction = "left"
        elif self.player.rect.centerx > self.rect.centerx:
            self.rect.x += self.speed
            self.direction = "right"

        if self.player.rect.centery < self.rect.centery:
            self.rect.y -= self.speed
            self.direction = "up"
        elif self.player.rect.centery > self.rect.centery:
            self.rect.y += self.speed
            self.direction = "down"

    def shoot(self):
        if pygame.time.get_ticks() - self.last_shot_time > self.shot_cooldown:
            # Reset the cooldown timer
            self.last_shot_time = pygame.time.get_ticks()

            # Create a new bullet object
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery, self.direction)

            # Add the bullet to the appropriate group
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)

            # Play the shooting sound effect
            shooting_sound.play()

    def update(self):
        self.move_towards_player()

        # Randomly shoot at the player
        if random.random() < ENEMY_SHOOT_CHANCE:
            self.shoot()

        # Wrap the tank around the screen
        if self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()

        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.direction = direction
        self.speed = PLAYER_SPEED / 2

    def update(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        # Remove the bullet if it goes off the screen
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()


#----------------------------------------------------------------------------------------------------------

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, max_health):
        super().__init__()
        self.max_health = max_health
        self.current_health = max_health
        self.image = pygame.Surface((50, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()

    def update(self, current_health):
        self.current_health = current_health
        health_ratio = self.current_health / self.max_health
        self.image = pygame.Surface((50, 10))
        if health_ratio > 0.6:
            self.image.fill((0, 255, 0))
        elif health_ratio > 0.3:
            self.image.fill((255, 255, 0))
        else:
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()


class Tank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.width = 40
        self.height = 40
        self.direction = "up"
        self.health = 100
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, keys, bullets):
        dx = 0
        dy = 0
        if keys[pygame.K_w]:
            dy = -self.speed
            self.direction = "up"
        elif keys[pygame.K_s]:
            dy = self.speed
            self.direction = "down"
        elif keys[pygame.K_a]:
            dx = -self.speed
            self.direction = "left"
        elif keys[pygame.K_d]:
            dx = self.speed
            self.direction = "right"

        self.x += dx
        self.y += dy
        self.rect.center = (self.x, self.y)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        if keys[pygame.K_SPACE]:
            self.shoot(bullets)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def shoot(self, bullets):
        bullet = Bullet(self.x, self.y, self.direction)
        bullets.add(bullet)


class HealthBar:
    def __init__(self, x, y, width, height, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.health = max_health
        self.border_color = (255, 255, 255)
        self.health_color = (0, 255, 0)
        self.border_rect = pygame.Rect(x, y, width, height)
        self.health_rect = pygame.Rect(x, y, width, height)

    def update(self, health):
        self.health = health
        if self.health < 0:
            self.health = 0
        health_width = int((self.health / self.max_health) * self.width)
        self.health_rect.width = health_width

    def draw(self, surface):
        pygame.draw.rect(surface, self.border_color, self.border_rect, 2)
        pygame.draw.rect(surface, self.health_color, self.health_rect)



#------------------------------------------------------------------------------------------------------

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tank Game")

        self.tank = Tank()
        self.enemy = EnemyTank()
        self.obstacles = [
            Obstacle(150, 150),
            Obstacle(450, 350)
        ]

        self.pause_button = Button((SCREEN_WIDTH - 100, 10), "Pause", self.pause_game)
        self.resume_button = Button((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50), "Resume", self.resume_game)
        self.quit_button = Button((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50), "Quit", self.quit_game)

        self.font = pygame.font.SysFont(None, 30)
        self.pause_text = self.font.render("Paused", True, WHITE)
        self.pause_rect = self.pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self.paused = False
        self.game_over = False

        self.lives = 3
        self.health_bar = Healthbar((10, 10), self.lives)

    def pause_game(self):
        self.paused = True

    def resume_game(self):
        self.paused = False

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def check_collisions(self):
        for obstacle in self.obstacles:
            if self.tank.collides_with(obstacle):
                self.tank.undo_collision()
            if self.enemy.collides_with(obstacle):
                self.enemy.undo_collision()

        if self.tank.collides_with(self.enemy):
            self.tank.undo_collision()
            self.lives -= 1
            self.health_bar = Healthbar((10, 10), self.lives)

        if self.enemy.is_shot_by(self.tank):
            self.enemy.reset()
            self.tank.bullets.pop()

    def game_loop(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused

                    if not self.paused:
                        if event.key == pygame.K_w:
                            self.tank.move_up()
                        elif event.key == pygame.K_s:
                            self.tank.move_down()
                        elif event.key == pygame.K_a:
                            self.tank.move_left()
                        elif event.key == pygame.K_d:
                            self.tank.move_right()
                        elif event.key == pygame.K_SPACE:
                            self.tank.shoot()

            if not self.paused:
                self.screen.fill(BLACK)

                for obstacle in self.obstacles:
                    obstacle.draw(self.screen)

                self.tank.draw(self.screen)
                self.tank.update()

                self.enemy.draw(self.screen)
                self.enemy.update(self.tank)

                self.check_collisions()

                self.pause_button.draw(self.screen)
                if self.paused:
                    pygame.draw.rect(self.screen, BLACK, self.pause_rect)
                    self.screen.blit(self.pause_text, self.pause_rect)
                    self.resume_button.draw(self.screen)
                    self.quit_button.draw(self.screen)

                self.health_bar.draw(self.screen)

            pygame.display.update()
            clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.game_loop()
