import pygame
import random
import sys
import csv
# Initialisierung von Pygame
pygame.init()

text_font = pygame.font.SysFont("Arial", 45)##Text formatierung
text_font2= pygame.font.SysFont("Arial", 20)

# Bildschirmabmessungen
WIDTH, HEIGHT = 600, 400

# Initialisierung des Bildschirms
screen = pygame.display.set_mode((WIDTH, HEIGHT))

score= 0
anzahlrunden = 0
user_text =''
highscore = 0
namelist =[]

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#Hintergrund eigenschaften
BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 600, 400

# Spieler Eigenschaften
PLAYER_WIDTH, PLAYER_HEIGHT = 60, 46.45
PLAYER_SPEED = 5

# Gegner Eigenschaften
ENEMY_WIDTH, ENEMY_HEIGHT = 64, 46.55
ENEMY_SPEED = 3
ENEMY_INTERVAL = 60  # Intervall, in dem ein neuer Gegner erscheint

LVLUP_ITEM_WIDTH,LVLUP_ITEM_HEIGHT = 30, 32.65
LVLUP_ITEM_SPEED = 4
LVLUP_ITEM_INTERVAL = 600

SHOT_WIDTH, SHOT_HEIGHT = 15, 15
SHOT_SPEED = -5

BONUSSCORE_WIDTH,BONUSSCORE_HEIGHT = 30,30
BONUSSCORE_SPEED = 3
BONUSSCORE_INTERVAL = 1000

enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT)) #Formatieren der Graphik

player_img = pygame.image.load("leverkusen.png")
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

background_img = pygame.image.load("green.png")
background_img= pygame.transform.scale(background_img,(BACKGROUND_WIDTH, BACKGROUND_HEIGHT))

shot_img = pygame.image.load("münchen.png")
shot_img = pygame.transform.scale(shot_img,(SHOT_WIDTH,SHOT_HEIGHT))

lvlup_item_img = pygame.image.load("stuttgart.png")
lvlup_item_img = pygame.transform.scale(lvlup_item_img,(LVLUP_ITEM_WIDTH,LVLUP_ITEM_HEIGHT))

bonusscore_img = pygame.image.load("köln.png")
bonusscore_img = pygame.transform.scale(bonusscore_img,(BONUSSCORE_WIDTH,BONUSSCORE_HEIGHT) )


#################################################
###           Funktionen                      ###
#################################################

#Bewegen mit Mauszeiger
def movemouse(player):
    mousepos = pygame.mouse.get_pos()
    player.x = max(0, min(mousepos[0], WIDTH - PLAYER_WIDTH))
    player.y = max(HEIGHT // 2, min(mousepos[1], HEIGHT - PLAYER_HEIGHT))
    move_mouse = False

def highscore_name(score,user_text,anzahlrunden):
    global highscore   
    if score >= highscore:
        highscore = score
    draw_text("Highscore von "+str(user_text)+": "+ str(highscore), text_font2,(255,255,255),20,360)

#gameover screen
def gameover_screen():
    global score

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
                    lives= 3
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False




#Ausgabe des textes
def draw_text(text, font, text_col, x, y):
            img = font.render(text, True, text_col)
            screen.blit(img, (x, y))
            
#Funktion zum Zeichenen des Hintergrunds
def draw_background():
     screen.blit(background_img,(0,0))


# Funktion zum Bewegen der Gegner
def create_enemy():
    x = random.randint(0, WIDTH - ENEMY_WIDTH)
    y = 0 - ENEMY_HEIGHT
    return pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)

def move_enemies(enemies,score):
    for enemy in enemies:
        if score <= 250 :
            enemy.y += ENEMY_SPEED
        elif 250<= score <=1000 :
            enemy.y += 2* ENEMY_SPEED
        elif 3000>=score >= 1000:
            enemy.y += 3*ENEMY_SPEED
        elif 10000>=score>= 3000:
            enemy.y+=4*ENEMY_SPEED
            ENEMY_INTERVAL =- 15
        elif score>=10000:
            enemy.y += 5*ENEMY_SPEED 
        
        

# Funktion zum Zeichnen der Gegner
def draw_enemies(enemies):
    for enemy in enemies:
        screen.blit(enemy_img, enemy)
        if enemy.y >= 400:
            enemies.remove(enemy)

# Funktion zum Zeichnen des Spielers
def draw_player(player):
    screen.blit(player_img, player)

#Funkton zum zeichen des Schusses
def draw_shots(shots):
    for shot in shots:
        screen.blit(shot_img,shot)
        if shot.y<=0:
            shots.remove(shot)

#Funktion zum erzeucgen eines Schusses
def create_shot(player):
    x = player.x +19
    y = player.y
    return pygame.Rect(x, y, SHOT_WIDTH, SHOT_HEIGHT)

#Funktion zum bewegwn des Schusses
def move_shot(shots):
    for shot in shots:
        shot.y+= SHOT_SPEED

#Funktion zum erstellen der Leben
def create_lvlup():
    x = random.randint(0, WIDTH - LVLUP_ITEM_WIDTH)
    y = 0 - LVLUP_ITEM_HEIGHT
    return pygame.Rect(x, y, LVLUP_ITEM_WIDTH, LVLUP_ITEM_HEIGHT)

#Funktion zum malen von Leben
def draw_lvlup(lvlup_items):
    for lvlup_item in lvlup_items:
        screen.blit(lvlup_item_img,lvlup_item)
        if lvlup_item.y>=400:
            lvlup_items.remove(lvlup_item)

#Funktion zum bewegwn des Leben
def move_lvlup(lvlup_items):
    for lvlup_item in lvlup_items:
        lvlup_item.y+= LVLUP_ITEM_SPEED

def create_bonusscore():
    x = random.randint(0, WIDTH - BONUSSCORE_WIDTH)
    y = 0 - BONUSSCORE_HEIGHT
    return pygame.Rect(x, y, BONUSSCORE_WIDTH, BONUSSCORE_HEIGHT)

#Funktion zum Malen von Bonusscore
def draw_bonusscore(bonus_score):
    for bonusscore in bonus_score:
        screen.blit(bonusscore_img,bonusscore)
        if bonusscore.y>=400:
            bonus_score.remove(bonusscore)

# Funktion zum Schreiben der Werte eines Array als Zeilen in eine csv-Datei
def write_to_csv(namelist, filename):
    with open("highscore.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(namelist)
        return namelist

def move_lvlup(bonus_score):
    for bonusscore in bonus_score:
        bonusscore.y+= BONUSSCORE_SPEED

# Funktion zum Lesen der Zeilen einer csv-Datei und speichern in einem Array
def read_from_csv(highscore):
    global namelist
    with open(highscore, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            namelist.append(row)
    return namelist

# Beispiel-Arrays für die Demonstration


# Test der Funktionen
write_to_csv(namelist, 'highscore.csv')
loaded_array = read_from_csv('highscore.csv')

# Ausgabe der Werte
print("Original Array:")
for row in namelist:
    print(row)

print("\nGeladenes Array aus der CSV-Datei:")
for row in loaded_array:
    print(row)