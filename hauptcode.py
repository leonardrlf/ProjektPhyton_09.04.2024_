import pygame
import random
import sys

# Initialisierung von Pygame
pygame.init()

# Bildschirmabmessungen
WIDTH, HEIGHT = 600, 400

# Erstellung Liste der Ligen
liga = ("Kreisliga", "Bezirksliga", "Landesliga", "Oberliga", "Regionalliga", "3. Liga", "2. Bundesliga", "1. Bundesliga", "Europa Conference League", "Europa League", "Championsleague")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Spieler Eigenschaften
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 20
PLAYER_SPEED = 5

# Gegner Eigenschaften
ENEMY_WIDTH, ENEMY_HEIGHT = 30, 30
ENEMY_INITIAL_SPEED = 3
ENEMY_INTERVAL = 60  # Intervall, in dem ein neuer Gegner erscheint

# Initialisierung des Bildschirms
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weiche den Feinden aus")
clock = pygame.time.Clock()

# Highscore
high_score = 0

# Bestenliste der Spieler
player_scores = {}

# Laden des Spieler- und Gegnerbildes und Anpassen der Größe
enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))

# Funktion zum Erzeugen eines neuen Gegners
def create_enemy():
    x = random.randint(0, WIDTH - ENEMY_WIDTH)
    y = 0 - ENEMY_HEIGHT
    return pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)

# Funktion zum Bewegen der Gegner
def move_enemies(enemies, speed):
    for enemy in enemies:
        enemy.y += speed





# Funktion zum Zeichnen des Spielers
def draw_player(player, player_name):
    if player_name == "stu":
        player_img = pygame.image.load("stuttgart.png")
        player_img = pygame.transform.scale(player_img, (48, 52.24))
    elif player_name == "bay":
        player_img = pygame.image.load("münchen.png")
        player_img = pygame.transform.scale(player_img, (50, 50))
    else:
        player_img = pygame.image.load("leverkusen.png")
        player_img = pygame.transform.scale(player_img, (60, 46.45))
    screen.blit(player_img, player)

# Funktion zum Zeichnen der Gegner
def draw_enemies(enemies):
    for enemy in enemies:
        screen.blit(enemy_img, enemy)

# Funktion zum Anzeigen des Highscores
def show_high_score(score):
    font = pygame.font.SysFont(None, 30)
    text = font.render("Highscore: " + str(score), True, BLACK)
    screen.blit(text, (10, 10))
    AL = int(score/100)
    ligen = liga[AL]
    text = font.render("Liga: " + str(ligen), True, BLACK)
    screen.blit(text, (10, 30))

# Funktion zum Anzeigen der Bestenliste der Spieler
def show_player_scores(scores):
    font = pygame.font.SysFont(None, 20)
    y_offset = 50
    for idx, (player, score) in enumerate(scores.items()):
        text = font.render(f"{idx + 1}. {player}: {score}", True, BLACK)
        screen.blit(text, (10, y_offset))
        y_offset += 20

# Funktion zum Neustart des Spiels
def restart_game():
    global high_score, player_scores
    high_score = 0
    player_scores = {}
    main()

# Hauptspiel
def main():
    global high_score

    player_name = input("Gib deinen Namen ein! (lev, bay, stu, ...): ")
    player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - 50, PLAYER_WIDTH, PLAYER_HEIGHT)
    enemies = []
    enemy_speed = ENEMY_INITIAL_SPEED
    score = 0

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart_game()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player.x += PLAYER_SPEED

        # Begrenze den Spieler auf den Bildschirm
        player.x = max(0, min(player.x, WIDTH - PLAYER_WIDTH))

        # Bewege die Gegner und füge neue hinzu
        move_enemies(enemies, enemy_speed)
        if random.randint(0, ENEMY_INTERVAL) == 0:
            enemies.append(create_enemy())

        # Kollisionserkennung
        for enemy in enemies:
            if player.colliderect(enemy):
                player_scores[player_name] = score
                running = False

        # Zeichne Spieler und Gegner
        draw_player(player, player_name)
        draw_enemies(enemies)

        # Zeige den Highscore
        show_high_score(high_score)

        # Aktualisiere den Bildschirm
        pygame.display.flip()
        clock.tick(60)

        # Aktualisiere den Highscore
        high_score = max(high_score, score)

        # Erhöhe die Punktzahl
        score += 1

        # Erhöhe die Geschwindigkeit der Gegner
        if score % 100 == 0:
            enemy_speed += 0.5

    # Zeige die Bestenliste der Spieler
    show_player_scores(player_scores)
    pygame.display.flip()

    font = pygame.font.SysFont(None, 60)
    text = font.render("GAME OVER", True, RED)
    screen.blit(text, (170, 150))
    pygame.display.flip()

    # Abfrage neues Spiel
    neu = input("Nochmal Spielen? (ja): ")
    if neu == "ja":
        main()
    else:
        pygame.quit()

if __name__ == "__main__":
    main()
