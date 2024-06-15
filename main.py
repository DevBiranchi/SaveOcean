import pygame
import random
import math

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ocean Invader")
icon = pygame.image.load('fish.png')
pygame.display.set_icon(icon)

# Load and scale background image
background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (800, 600))

# Load images
player_img = pygame.image.load('boat.png')
fish_img = pygame.image.load('fish.png')
enemy_img = pygame.image.load('garbage.png')
enemy1_img = pygame.image.load('garbage-bag.png')
bullet_img = pygame.image.load('bullet.png')
bullet_img = pygame.transform.rotate(bullet_img, -90)  # Rotate the bullet to face right

# Font for score display
font = pygame.font.Font('freesansbold.ttf', 32)
game_over_font = pygame.font.Font('freesansbold.ttf', 64)
button_font = pygame.font.Font('freesansbold.ttf', 32)
loading_font = pygame.font.Font('freesansbold.ttf', 48)
guide_font = pygame.font.Font('freesansbold.ttf', 24)

# Player variables
playerX = 190
playerY = 270
playerY_change = 0

# Bullet variables
bullets = []

# Enemy variables
num_enemies = 5
enemies = []
for _ in range(num_enemies):
    enemyX = random.randint(550, 720)
    enemyY = random.randint(10, 550)
    enemies.append([enemyX, enemyY])

# Score variables
score = 0
high_score = 0

# Game Over variable
game_over = False


# Fish class
class Fish:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.y_change = 0.3

    def move(self):
        self.y += self.y_change
        if self.y <= 0 or self.y >= 550:
            self.y_change *= -1

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))


# Create multiple fishes
num_fishes = 15
fishes = []
for i in range(num_fishes):
    fish_x = random.randint(10, 100)
    fish_y = random.randint(10, 500)
    fishes.append(Fish(fish_x, fish_y, fish_img))


# Player function
def player(x, y):
    screen.blit(player_img, (x, y))


def draw_enemy(enemy):
    screen.blit(enemy_img, (enemy[0], enemy[1]))


def fire_bullet(x, y):
    bullets.append([x, y])


def draw_bullet(x, y):
    screen.blit(bullet_img, (x, y))


def is_collision(obj1X, obj1Y, obj2X, obj2Y):
    distance = math.sqrt(math.pow(obj1X - obj2X, 2) + math.pow(obj1Y - obj2Y, 2))
    return distance < 27


def show_score(x, y):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    screen.blit(score_text, (x, y))
    screen.blit(high_score_text, (x, y + 40))


def respawn_enemy(enemy):
    enemy[0] = random.randint(550, 720)
    enemy[1] = random.randint(10, 550)


def show_game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 150))

    restart_text = button_font.render("Restart", True, (0, 0, 0))
    restart_rect = pygame.Rect(350, 300, 150, 50)  # Adjusted size for the white box
    pygame.draw.rect(screen, (255, 255, 255), restart_rect)
    text_rect = restart_text.get_rect(center=restart_rect.center)  # Center the text in the box
    screen.blit(restart_text, text_rect.topleft)

    return restart_rect


def show_loading_screen():
    loading_text = loading_font.render("PROTECT THE FISHES!", True, (255, 255, 255))
    screen.blit(loading_text, (80, 200))

    start_text = button_font.render("Start", True, (0, 0, 0))
    start_rect = pygame.Rect(325, 350, 150, 50)  # Adjusted size for the white box
    pygame.draw.rect(screen, (255, 255, 255), start_rect)
    text_rect = start_text.get_rect(center=start_rect.center)  # Center the text in the box
    screen.blit(start_text, text_rect.topleft)

    # Add game instructions
    guide_text_1 = guide_font.render("Press SPACE to shoot", True, (255, 255, 255))
    guide_text_2 = guide_font.render("Press UP ARROW to move up", True, (255, 255, 255))
    guide_text_3 = guide_font.render("Press DOWN ARROW to move down", True, (255, 255, 255))
    screen.blit(guide_text_1, (250, 420))
    screen.blit(guide_text_2, (250, 450))
    screen.blit(guide_text_3, (250, 480))

    return start_rect


# Game loop
running = True
in_loading_screen = True

while running:
    screen.fill((0, 157, 196))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if in_loading_screen:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if start_rect.collidepoint(mouse_pos):
                    in_loading_screen = False

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                    playerY_change = -3
                if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                    playerY_change = 3
                if event.key == pygame.K_SPACE:
                    fire_bullet(playerX + player_img.get_width(),
                                playerY + player_img.get_height() // 2 - bullet_img.get_height() // 2)

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    playerY_change = 0

            if game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if restart_rect.collidepoint(mouse_pos):
                    # Reset game
                    game_over = False
                    score = 0
                    playerY = 270
                    bullets.clear()
                    enemies.clear()
                    for _ in range(num_enemies):
                        enemyX = random.randint(550, 720)
                        enemyY = random.randint(10, 550)
                        enemies.append([enemyX, enemyY])

    if in_loading_screen:
        start_rect = show_loading_screen()
    else:
        if not game_over:
            playerY += playerY_change
            playerY = max(15, min(playerY, 520))

            for bullet in bullets:
                bullet[0] += 25
                if bullet[0] > 800:
                    bullets.remove(bullet)

            for enemy in enemies:
                enemy[0] -= 2  # Move left towards the player
                enemy[1] += (playerY - enemy[1]) * 0.02  # Move vertically towards the player

                # Check for collision with player
                if is_collision(enemy[0], enemy[1], playerX, playerY):
                    game_over = True
                    break

            for bullet in bullets:
                for enemy in enemies:
                    if is_collision(enemy[0], enemy[1], bullet[0], bullet[1]):
                        bullets.remove(bullet)
                        respawn_enemy(enemy)
                        score += 1
                        if score > high_score:
                            high_score = score
                        break

            for fish in fishes:
                fish.move()
                fish.draw(screen)

            player(playerX, playerY)

            for enemy in enemies:
                draw_enemy(enemy)

            for bullet in bullets:
                draw_bullet(bullet[0], bullet[1])

            show_score(10, 10)

        else:
            restart_rect = show_game_over()
            show_score(10, 10)

    pygame.display.update()
