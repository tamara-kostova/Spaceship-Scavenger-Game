import pygame
import random
import sys
from pygame.locals import *

pygame.init()
pygame.mixer.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PLAYER_SPEED = 5
ASTEROID_SPEED = 3
CRYSTAL_SPEED = 2
ASTEROID_SPAWN_RATE = 2000

global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
BASICFONT = pygame.font.Font(None, 36)
BIGFONT = pygame.font.Font(None, 48)

player = None
asteroids = []
crystals = []
score = 0
game_over = False
last_asteroid_spawn = 0
current_speed = ASTEROID_SPEED

WINNING_SCORE = 30
MIN_SURVIVAL_TIME = 30000 
start_time = 0
game_won = False

def load_game():
    global spaceship_img, asteroid_img, crystal_img, clash_sound, background_music
    
    spaceship_img = pygame.image.load("assets/spaceship.png").convert_alpha()
    asteroid_img = pygame.image.load("assets/asteroid.png").convert_alpha()
    crystal_img = pygame.image.load("assets/energy_crystal.png").convert_alpha()
    
    spaceship_img = pygame.transform.scale(spaceship_img, (50, 50))
    asteroid_img = pygame.transform.scale(asteroid_img, (40, 40))
    crystal_img = pygame.transform.scale(crystal_img, (30, 30))
    
    clash_sound = pygame.mixer.Sound("assets/clash_sound.wav")
    background_music = pygame.mixer.Sound("assets/background_music.wav")
    background_music.play(-1)

def init_game():
    global player, asteroids, crystals, score, game_over, last_asteroid_spawn, current_speed
    global current_speed, start_time, game_won
    player = pygame.Rect(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 70, 50, 50)
    asteroids = []
    crystals = []
    score = 0
    game_over = False
    game_won = False
    current_speed = ASTEROID_SPEED
    last_asteroid_spawn = pygame.time.get_ticks()
    start_time = pygame.time.get_ticks()
    background_music.play(-1)

def spawn_asteroid():
    global current_speed
    base_size = 40
    size_increase = int(min((current_speed - ASTEROID_SPEED) * 5, 40))
    current_size = base_size + size_increase
    x = random.randint(0, WINDOW_WIDTH - current_size)
    asteroid = pygame.Rect(x, -50, current_size, current_size)
    scaled_asteroid_img = pygame.transform.scale(asteroid_img, (current_size, current_size))
    asteroids.append((asteroid, scaled_asteroid_img))

def spawn_crystal():
    if random.random() < 0.3:
        x = random.randint(0, WINDOW_WIDTH - 30)
        crystal = pygame.Rect(x, -50, 30, 30)
        crystals.append(crystal)

def handle_input():
    global player
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and player.left > 0:
        player.x -= PLAYER_SPEED
    if keys[K_RIGHT] and player.right < WINDOW_WIDTH:
        player.x += PLAYER_SPEED

def update_game():
    global game_over, game_won, score, current_speed, last_asteroid_spawn
    
    if game_over or game_won:
        return

    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time

    if score >= WINNING_SCORE and elapsed_time >= MIN_SURVIVAL_TIME:
        game_won = True
        background_music.stop()
        return
    
    if current_time - last_asteroid_spawn > ASTEROID_SPAWN_RATE:
        spawn_asteroid()
        spawn_crystal()
        last_asteroid_spawn = current_time

    for asteroid_tuple in asteroids[:]:
        asteroid, _ = asteroid_tuple
        asteroid.y += current_speed
        if asteroid.top > WINDOW_HEIGHT:
            asteroids.remove(asteroid_tuple)
        elif asteroid.colliderect(player):
            clash_sound.play()
            game_over = True
            background_music.stop()

    for crystal in crystals[:]:
        crystal.y += CRYSTAL_SPEED
        if crystal.top > WINDOW_HEIGHT:
            crystals.remove(crystal)
        elif crystal.colliderect(player):
            crystals.remove(crystal)
            score += 10

    current_speed += 0.01

def draw_game():
    DISPLAYSURF.fill(BLACK)
    
    DISPLAYSURF.blit(spaceship_img, player)
    
    for asteroid, asteroid_surface in asteroids:
        DISPLAYSURF.blit(asteroid_surface, asteroid)
    
    for crystal in crystals:
        DISPLAYSURF.blit(crystal_img, crystal)

    score_text = BASICFONT.render(f'Score: {score}', True, WHITE)
    DISPLAYSURF.blit(score_text, (10, 10))

    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Convert to seconds
    time_text = BASICFONT.render(f'Time: {elapsed_time}s', True, WHITE)
    DISPLAYSURF.blit(time_text, (10, 50))

    if game_won:
        win_text = BIGFONT.render('You Won! Press R to play again', True, WHITE)
        text_rect = win_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        DISPLAYSURF.blit(win_text, text_rect)
    elif game_over:
        game_over_text = BIGFONT.render('Game Over! Press R to restart', True, WHITE)
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        DISPLAYSURF.blit(game_over_text, text_rect)

    pygame.display.flip()

def display_instructions():
    instructions = [
        "Welcome to Space Scavenger!",
        "Instructions:",
        "- Use LEFT and RIGHT arrow keys to move your spaceship.",
        "- Avoid the asteroids.",
        "- Collect energy crystals to increase your score.",
        "- Survive long enough and reach a score of 30 to win.",
        "- Press 'R' to restart if you lose or win.",
        "Press any key to start the game!"
    ]

    DISPLAYSURF.fill(BLACK)

    for i, line in enumerate(instructions):
        text = BASICFONT.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 100 + i * 40))
        DISPLAYSURF.blit(text, text_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                waiting = False

def main():
    global game_over, game_won
    
    pygame.display.set_caption('Space Scavenger')
    
    load_game()
    display_instructions()
    init_game()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_r and (game_over or game_won):
                    init_game()

        handle_input()
        update_game()
        draw_game()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()