import csv
import pygame
import sys

# Funktion für die Usereingabe am Ende des Spiels
def get_end_game_input(screen, clock):
        font = pygame.font.Font(None, 32)
        input_box = pygame.Rect(10, 40, 140, 32)
        color_active = pygame.Color('black')
        color_passive = pygame.Color('black')
        color = color_passive
        user_text = ''
        active = True
        
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
                        else:
                            user_text += event.unicode

            screen.fill((255, 255, 255))

            if active:
                color = color_active
            else:
                color = color_passive

            # Render den Text
            text = font.render('Gib Deinen Namen ein:', True, (0, 0, 0))

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


# Funktion zum Schreiben der Werte eines Array als Zeilen in eine csv-Datei
def write_to_csv(array, filename):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(array)

# Funktion zum Lesen der Zeilen einer csv-Datei und speichern in einem Array
def read_from_csv(filename):
    array = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            array.append(row)
    return array

# Beispiel-Arrays für die Demonstration
example_array = [
    ["Julia", 200],
    ["Chris", 6000],
    ["Marie", 8000]
]

# Test der Funktionen
write_to_csv(example_array, 'highscore.csv')
loaded_array = read_from_csv('highscore.csv')

# Ausgabe der Werte
print("Original Array:")
for row in example_array:
    print(row)

print("\nGeladenes Array aus der CSV-Datei:")
for row in loaded_array:
    print(row)


