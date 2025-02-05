import pygame
import sys

# Impostazioni iniziali
WIDTH, HEIGHT = 800, 600
FPS = 60

# Inizializzazione di pygame
pygame.init()

# Creazione della finestra
schermo = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Iniziale")

# Definizione dei colori
BIANCO = (255, 255, 255)
AZZURRO = (0, 255, 255)
VERDE = (0, 255, 0)
ROSSO = (255, 0, 0)
GRIGIO = (169, 169, 169)
GIALLO = (255, 255, 0)
NERO = (0, 0, 0)
GRIGIO = (100,100,100)

# Font
font = pygame.font.Font(None, 36)

# Variabili globali del menu
NUMBER_OF_PALLINI = "2"
MAX_MONSTER_NUMBER = "3"
NUMBER_OF_TURN_INFRA_GENERATION = "5"
MONSTER_GENERATION = True
SOUND_ON = True
MUSIC_ON = True
IMMORTALITY = False

# Definizione dei rettangoli dei pulsanti
inizia_rect = pygame.Rect(100, 100, 200, 50)
esci_rect = pygame.Rect(100, 200, 200, 50)
monster_flag_rect = pygame.Rect(100, 300, 250, 50)
sound_flag_rect = pygame.Rect(100, 400, 250, 50)
music_flag_rect = pygame.Rect(100, 500, 250, 50)
immortality_flag_rect = pygame.Rect(100, 600, 250, 50)

# Input box per i numeri
input_pallini_rect = pygame.Rect(600, 100, 100, 40)
input_monster_rect = pygame.Rect(600, 200, 100, 40)
input_turns_rect = pygame.Rect(600, 300, 100, 40)

# Funzione per scrivere il testo centrato
def scrivi_testo(testo, dimensione, colore, rettangolo):
    testo_render = font.render(testo, True, colore)
    testo_rect = testo_render.get_rect(center=rettangolo.center)
    schermo.blit(testo_render, testo_rect)

# Funzione per disegnare un toggle box
def disegna_toggle_box(rect, stato, descrizione):
    colore = VERDE if stato else ROSSO
    pygame.draw.rect(schermo, colore, rect)
    scrivi_testo(descrizione, 30, NERO, rect)

# Funzione per disegnare un input box
def disegna_input_box(rect, valore):
    pygame.draw.rect(schermo, NERO, rect, 2)
    scrivi_testo(valore, 30, NERO, rect)

# Funzione per il menu
def mostra_menu():
    global MONSTER_GENERATION, SOUND_ON, MUSIC_ON, IMMORTALITY, NUMBER_OF_PALLINI, MAX_MONSTER_NUMBER, NUMBER_OF_TURN_INFRA_GENERATION
    menu_iniziale = True
    while menu_iniziale:
        schermo.fill(GRIGIO)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if inizia_rect.collidepoint(pos):
                    menu_iniziale = False
                    return NUMBER_OF_PALLINI, MAX_MONSTER_NUMBER, NUMBER_OF_TURN_INFRA_GENERATION, MONSTER_GENERATION, SOUND_ON, MUSIC_ON, IMMORTALITY
                
                if esci_rect.collidepoint(pos):
                    pygame.quit()
                    sys.exit()

                if monster_flag_rect.collidepoint(pos):
                    MONSTER_GENERATION = not MONSTER_GENERATION
                if sound_flag_rect.collidepoint(pos):
                    SOUND_ON = not SOUND_ON
                if music_flag_rect.collidepoint(pos):
                    MUSIC_ON = not MUSIC_ON
                if immortality_flag_rect.collidepoint(pos):
                    IMMORTALITY = not IMMORTALITY

            if event.type == pygame.KEYDOWN:
                if input_pallini_rect.collidepoint(pygame.mouse.get_pos()):
                    if event.key == pygame.K_BACKSPACE:
                        NUMBER_OF_PALLINI = NUMBER_OF_PALLINI[:-1]
                    else:
                        NUMBER_OF_PALLINI += event.unicode

                if input_monster_rect.collidepoint(pygame.mouse.get_pos()):
                    if event.key == pygame.K_BACKSPACE:
                        MAX_MONSTER_NUMBER = MAX_MONSTER_NUMBER[:-1]
                    else:
                        MAX_MONSTER_NUMBER += event.unicode

                if input_turns_rect.collidepoint(pygame.mouse.get_pos()):
                    if event.key == pygame.K_BACKSPACE:
                        NUMBER_OF_TURN_INFRA_GENERATION = NUMBER_OF_TURN_INFRA_GENERATION[:-1]
                    else:
                        NUMBER_OF_TURN_INFRA_GENERATION += event.unicode

        pygame.draw.rect(schermo, AZZURRO, inizia_rect)
        pygame.draw.rect(schermo, AZZURRO, esci_rect)

        disegna_toggle_box(monster_flag_rect, MONSTER_GENERATION, "Generazione Mostri")
        disegna_toggle_box(sound_flag_rect, SOUND_ON, "Suoni")
        disegna_toggle_box(music_flag_rect, MUSIC_ON, "Musica")
        disegna_toggle_box(immortality_flag_rect, IMMORTALITY, "Immortalità")

        disegna_input_box(input_pallini_rect, NUMBER_OF_PALLINI)
        scrivi_testo("Pallini:", 30, NERO, pygame.Rect(input_pallini_rect.left - 170, input_pallini_rect.top, 150, 40))
        if MONSTER_GENERATION:
            disegna_input_box(input_monster_rect, MAX_MONSTER_NUMBER)
            scrivi_testo("Mostri Max:", 30, NERO, pygame.Rect(input_monster_rect.left - 170, input_monster_rect.top, 150, 40))
            disegna_input_box(input_turns_rect, NUMBER_OF_TURN_INFRA_GENERATION)
            scrivi_testo("Turni Mostri:", 30, NERO, pygame.Rect(input_turns_rect.left - 170, input_turns_rect.top, 150, 40))

        scrivi_testo("Inizia", 30, NERO, inizia_rect)
        scrivi_testo("Esci", 30, NERO, esci_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

# Funzione principale
def main():
    mostra_menu()

if __name__ == "__main__":
    main()
