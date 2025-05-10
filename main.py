import pygame
import os
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Loading spaceship image
SPACESHIP_IMAGE = pygame.image.load(os.path.join("spaceship.png")).convert_alpha()
SPACESHIP = pygame.transform.scale(SPACESHIP_IMAGE, (60, 60))

# Loading heart icon 
HEART_ICON = pygame.image.load(os.path.join("heart.png")).convert_alpha()
HEART_ICON = pygame.transform.scale(HEART_ICON, (25, 25))

# Fonts
font = pygame.font.SysFont('comicsans', 24)
title_font = pygame.font.SysFont('comicsans', 40)

# Bullet settings
BULLET_WIDTH, BULLET_HEIGHT = 4, 10
BULLET_VELOCITY = 5
MAX_BULLETS = 3

# Enemy settings
ENEMY_WIDTH, ENEMY_HEIGHT = 50, 50
ENEMY_VELOCITY = 2

# Explosion settings
EXPLOSION_SIZE = 15

# Game variables
score = 0
lives = 5
x, y = WIDTH // 2 - 30, HEIGHT - 100
VELOCITY = 5
bullets = []
enemies = []
explosions = []


clock = pygame.time.Clock()

def adjust_difficulty(score):
    global ENEMY_VELOCITY, BULLET_VELOCITY, MAX_BULLETS
    if score < 20:
        ENEMY_VELOCITY = 2
        BULLET_VELOCITY = 5
        MAX_BULLETS = 3
    elif score < 60:
        ENEMY_VELOCITY = 2.5
        BULLET_VELOCITY = 5.5
        MAX_BULLETS = 4
    elif score < 100:
        ENEMY_VELOCITY = 3
        BULLET_VELOCITY = 6
        MAX_BULLETS = 5
    else:
        ENEMY_VELOCITY = 4
        BULLET_VELOCITY = 7
        MAX_BULLETS = 6

def draw_explosion(x, y):
    explosion_surface = pygame.Surface((EXPLOSION_SIZE, EXPLOSION_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(explosion_surface, (255, 165, 0), (EXPLOSION_SIZE // 2, EXPLOSION_SIZE // 2), EXPLOSION_SIZE // 2)
    WIN.blit(explosion_surface, (x - EXPLOSION_SIZE // 2, y - EXPLOSION_SIZE // 2))

def draw_stars(stars):
    for star in stars:
        star[1] += star[2]
        if star[1] > HEIGHT:
            star[0] = random.randint(0, WIDTH)
            star[1] = 0
        pygame.draw.circle(WIN, (255, 255, 255), (star[0], star[1]), 2)

def draw_spaceship(x, y):
    WIN.blit(SPACESHIP, (x, y))

def draw_enemies(enemies):
    for enemy in enemies:
        pygame.draw.rect(WIN, (0, 0, 255), (enemy[0], enemy[1], ENEMY_WIDTH, ENEMY_HEIGHT))

def draw_hearts(lives):
    for i in range(lives):
        WIN.blit(HEART_ICON, (WIDTH - 30 - (i * 30), 10))

# Collision check
def is_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def main_menu():
    run = True
    while run:
        WIN.fill((0, 0, 0))
        title = title_font.render("Space Shooter", True, (255, 255, 255))
        start_button = font.render("Start Game", True, (0, 255, 0))

        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        WIN.blit(start_button, (WIDTH // 2 - start_button.get_width() // 2, HEIGHT // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if WIDTH // 2 - start_button.get_width() // 2 <= mouse_x <= WIDTH // 2 + start_button.get_width() // 2 and HEIGHT // 2 <= mouse_y <= HEIGHT // 2 + start_button.get_height():
                    run = False

    main()

# Game over screen
def game_over_screen():
    global score
    run = True
    while run:
        WIN.fill((0, 0, 0))
        game_over_text = title_font.render("GAME OVER", True, (255, 0, 0))
        WIN.blit(game_over_text, (WIDTH // 3, HEIGHT // 3))

        score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        WIN.blit(score_text, (WIDTH // 3, HEIGHT // 2))

        restart_button = font.render("Restart", True, (0, 255, 0))
        quit_button = font.render("Quit", True, (255, 0, 0))

        WIN.blit(restart_button, (WIDTH // 3, HEIGHT // 2 + 40))
        WIN.blit(quit_button, (WIDTH // 3, HEIGHT // 2 + 80))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if WIDTH // 3 <= mouse_x <= WIDTH // 3 + restart_button.get_width() and HEIGHT // 2 + 40 <= mouse_y <= HEIGHT // 2 + 40 + restart_button.get_height():
                    main()
                elif WIDTH // 3 <= mouse_x <= WIDTH // 3 + quit_button.get_width() and HEIGHT // 2 + 80 <= mouse_y <= HEIGHT // 2 + 80 + quit_button.get_height():
                    pygame.quit()
                    exit()

# Main game loop
def main():
    global x, y, score, lives, bullets, enemies, explosions
    stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)] for _ in range(30)]

    score = 0
    lives = 5
    bullets = []
    enemies = []
    explosions = []
    x, y = WIDTH // 2 - 30, HEIGHT - 100

    run = True
    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))
        draw_stars(stars)
        adjust_difficulty(score)

        for bullet in bullets[:]:
            bullet[1] -= BULLET_VELOCITY
            if bullet[1] < 0:
                bullets.remove(bullet)
            else:
                pygame.draw.rect(WIN, (255, 0, 0), (bullet[0], bullet[1], BULLET_WIDTH, BULLET_HEIGHT))

        for i, enemy in enumerate(enemies[:]):
            enemy[1] += ENEMY_VELOCITY
            if enemy[1] > HEIGHT:
                enemy[0] = random.randint(0, WIDTH - ENEMY_WIDTH)
                enemy[1] = random.randint(-100, -40)

            enemy_rect = pygame.Rect(enemy[0], enemy[1], ENEMY_WIDTH, ENEMY_HEIGHT)

            for bullet in bullets[:]:
                bullet_rect = pygame.Rect(bullet[0], bullet[1], BULLET_WIDTH, BULLET_HEIGHT)
                if is_collision(bullet_rect, enemy_rect):
                    bullets.remove(bullet)
                    enemies[i] = [random.randint(0, WIDTH - ENEMY_WIDTH), random.randint(-100, -40)]
                    score += 1
                    explosions.append([enemy[0], enemy[1]])

            if is_collision(pygame.Rect(x, y, 60, 60), enemy_rect):
                enemies[i] = [random.randint(0, WIDTH - ENEMY_WIDTH), random.randint(-100, -40)]
                lives -= 1
                if lives == 0:
                    game_over_screen()

        for explosion in explosions[:]:
            draw_explosion(explosion[0], explosion[1])
            explosions.remove(explosion)

        draw_spaceship(x, y)
        draw_enemies(enemies)
        draw_hearts(lives)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        WIN.blit(score_text, (10, 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x - VELOCITY > 0:
            x -= VELOCITY
        if keys[pygame.K_RIGHT] and x + VELOCITY + 60 < WIDTH:
            x += VELOCITY
        if keys[pygame.K_UP] and y - VELOCITY > 0:
            y -= VELOCITY
        if keys[pygame.K_DOWN] and y + VELOCITY + 60 < HEIGHT:
            y += VELOCITY

        if keys[pygame.K_SPACE]:
            if len(bullets) < MAX_BULLETS:
                bullet_x = x + 30 - BULLET_WIDTH // 2
                bullet_y = y
                bullets.append([bullet_x, bullet_y])

        if random.random() < 0.02:
            enemies.append([random.randint(0, WIDTH - ENEMY_WIDTH), random.randint(-100, -40)])

    pygame.quit()

if __name__ == "__main__":
    main_menu()
