import pygame
import random
import sys
from funktionen import*


# Initialisierung von Pygame
pygame.init()

text_font = pygame.font.SysFont("Arial", 45)##Text formatierung
text_font2= pygame.font.SysFont("Arial", 20)
# Bildschirmabmessungen
WIDTH, HEIGHT = 600, 400

score= 0
anzahlrunden = 0
user_text = ''
highscore = 0
lives= 3

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#Hintergrund eigenschaften
BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 600, 400

# Spieler Eigenschaften
PLAYER_WIDTH, PLAYER_HEIGHT = 45.34, 72.356
PLAYER_SPEED = 5

# Gegner Eigenschaften
ENEMY_WIDTH, ENEMY_HEIGHT = 30, 30
ENEMY_SPEED = 3
ENEMY_INTERVAL = 60  # Intervall, in dem ein neuer Gegner erscheint

SHOT_WIDTH, SHOT_HEIGHT = 10, 30
SHOT_SPEED = -5

enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT)) #Formatieren der Graphik

player_img = pygame.image.load("leverkusen.png")
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

background_img = pygame.image.load("green.png")
background_img= pygame.transform.scale(background_img,(BACKGROUND_WIDTH, BACKGROUND_HEIGHT))

shot_img = pygame.image.load("münchen.png")
shot_img = pygame.transform.scale(shot_img,(SHOT_WIDTH,SHOT_HEIGHT))

# Initialisierung des Bildschirms
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weiche den Feinden aus")
clock = pygame.time.Clock()



#gameover screen
def gameover_screen(user_text):
    global score
    global lives
    draw_background()
    draw_text("Game Over",text_font, (139,0,0),180,170)
    draw_text("Zum weiter/nicht weiter spieln Enter/Esc",text_font2,(255,255,255),130,270)
    draw_text("Score: "+ str(score), text_font2,(255,255,255),20,20)
    highscore_name(score,user_text,anzahlrunden)
    pygame.display.flip()

    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    score =0
                    lives = 3
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False



# Funktion für die Usereingabe am Ende des Spiels
def get_end_game_input(screen, clock):
        
        global user_text
        font = pygame.font.Font(None, 32)
        input_box = pygame.Rect(10, 40, 140, 32)
        color_active = pygame.Color('black')
        color_passive = pygame.Color('black')
        color = color_passive
        user_text = ''
        active = True
        namelist.append(user_text)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            return user_text
                        elif event.key == pygame.K_BACKSPACE:
                            user_text = user_text[:-1]
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        else:
                            user_text += event.unicode

            draw_background()

            if active:
                color = color_active
            else:
                color = color_passive

            # Render den Text
            text = font.render('Gib Deinen Namen ein:', True, (255, 255, 255))

            # Position des Textes
            text_x = 10
            text_y = 10
            screen.blit(text, (text_x, text_y))

            pygame.draw.rect(screen, color, input_box)
            text_surface = font.render(user_text, True, (255, 255, 255))
            screen.blit(text_surface, (input_box.x+5, input_box.y+5))
            input_box.w = max(100, text_surface.get_width()+10)

            
            pygame.display.flip()
            clock.tick(60)

     
#Highscore und Name
def highscore_name(score,user_text,anzahlrunden):
    global highscore   
    if score >= highscore:
        highscore = score
    draw_text(str(user_text)+"'s Highscore: "+ str(highscore), text_font2,(255,255,255),20,360)


    

# Hauptspiel
def main():
    player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - 72.356, PLAYER_WIDTH, PLAYER_HEIGHT)
    enemies = []
    shots = []
    lvlup_items= []
    bonus_score=[]
    global score
    global anzahlrunden
    global lives

    running = True
    move_mouse = False
    while running:
        draw_background()
        draw_text("Score: "+ str(score), text_font2,(255,255,255),20,20)
        draw_text("lives: "+ str(lives), text_font2,(255,255,255),20,40)
        
        if anzahlrunden >= 1:
            highscore_name(score, user_text, anzahlrunden)
        else:
            draw_text("no highscore yet", text_font2, (255,255,255), 20, 360)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.MOUSEMOTION:
                move_mouse = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shots.append(create_shot(player))
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if move_mouse:
            movemouse(player)

        player.x = max(0, min(player.x, WIDTH - PLAYER_WIDTH))

        move_enemies(enemies,score)
        if random.randint(0, ENEMY_INTERVAL) == 0:
            enemies.append(create_enemy())
        
        move_lvlup(lvlup_items)
        if random.randint(0, LVLUP_ITEM_INTERVAL) == 0:
            lvlup_items.append(create_lvlup())

        # Kollisionserkennung zwischen Spieler und Gegnern
        for enemy in enemies:
            if player.colliderect(enemy):
                lives -= 1 
                enemies.remove(enemy)
                if lives == 0:
                     running = False
        
        #Kollisionserkennung zwischen levelup und Schuss
        for lvlup_item in lvlup_items:
            for shot in shots:
                if shot.colliderect(lvlup_item):
                    lvlup_items.remove(lvlup_item)
                    lives += 1

        # Kollisionserkennung zwischen Schüssen und Gegnern
        for shot in shots:
            for enemy in enemies:
                if shot.colliderect(enemy):
                    shots.remove(shot)
                    enemies.remove(enemy)

        move_shot(shots)
        draw_player(player)
        draw_enemies(enemies)
        draw_shots(shots)
        draw_lvlup(lvlup_items)
        
        score += 1
        pygame.display.flip()
        clock.tick(60)

    if anzahlrunden == 0:
        get_end_game_input(screen, clock)
    anzahlrunden += 1

    if gameover_screen(user_text):
        main()
    else:
        pygame.quit()
        sys.exit()

        

if __name__ == "__main__":
    main()