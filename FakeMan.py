from pyswip import Prolog
import pygame
import re
import random
import copy

# Inizializza Pygame
pygame.init()
pygame.mixer.init()
 
 # Costanti
DIM_QUADRATO = 30         # Dimensione di un quadrato
OFFSET = 5                # Spazio tra i quadrati
RIGHE = 15                # Numero di righe
COLONNE = 20   
FPS = 60    

# Altezza finestra
LARGHEZZA_FINESTRA =  COLONNE * (DIM_QUADRATO + OFFSET)  # Larghezza adattiva finestra
ALTEZZA_FINESTRA = RIGHE * (DIM_QUADRATO + OFFSET)   # Altezza adattiva

# Colori
BIANCO = (255, 255, 255)
NERO = (0, 0, 0)
ROSSO = (255, 0, 0)
BLU = (0,0,255)
VERDE = (0,255,0)
GIALLO = (255,255,0)
AZZURRO = (0,255,255)
GRIGIO = (120,120,120)

def setInitialFlag():
#Flag
    global MONSTER_GENERATION
    global MAX_MONSTER_NUMBER 
    global NUMBER_OF_TURN_INFRA_GENERATION 
    global NUMBER_OF_PALLINI 
    global IMMORTALITY
    global SOUND_ON 
    global MUSIC_ON
        
    MONSTER_GENERATION = True
    MAX_MONSTER_NUMBER = 5
    NUMBER_OF_TURN_INFRA_GENERATION = 5
    NUMBER_OF_PALLINI = 3
    IMMORTALITY = False
    SOUND_ON = True
    MUSIC_ON = False

setInitialFlag()

#booleani per il controllo delle animazioni
playerDirection = 0 #1 is right || #0 is left
numeroMosse = 0 #contatore mosse
pallinePrese = 0
stopCondition = False
winPlayed = False
gameOverPlayer = False

#Sprite player
sprite_player = pygame.image.load("immagini/FakeMan.png")
sprite_player = pygame.transform.scale(sprite_player, (DIM_QUADRATO, DIM_QUADRATO))
sprite_player = pygame.transform.flip(sprite_player, True, False)

#Nemico 1
sprite_enemy1 = pygame.image.load("immagini/Arancione.png")
sprite_enemy1 = pygame.transform.scale(sprite_enemy1, (DIM_QUADRATO, DIM_QUADRATO))

#Nemico 2
sprite_enemy2 = pygame.image.load("immagini/Blu.png")
sprite_enemy2 = pygame.transform.scale(sprite_enemy2, (DIM_QUADRATO, DIM_QUADRATO))

sprite_enemy3 = pygame.image.load("immagini/Rosso.png")
sprite_enemy3 = pygame.transform.scale(sprite_enemy3, (DIM_QUADRATO, DIM_QUADRATO))

sprite_pallino = pygame.image.load("immagini/pallino.png")
sprite_pallino = pygame.transform.scale(sprite_pallino, (DIM_QUADRATO, DIM_QUADRATO))

sprite_win = pygame.image.load("immagini/YouWin.png")
sprite_win = pygame.transform.scale(sprite_win,(ALTEZZA_FINESTRA//2, LARGHEZZA_FINESTRA//2))

sprite_lose = pygame.image.load("immagini/GameOver.png")
sprite_lose = pygame.transform.scale(sprite_lose,(ALTEZZA_FINESTRA, LARGHEZZA_FINESTRA))

#Gruppo per la selezione random degli sprite
spriteGroup = [sprite_enemy1, sprite_enemy2, sprite_enemy3]
posGroup = [[0,1],[0,19],[13,0]]
validCellGroup = []   #######################
cellWithPallino = []

#Caricamento Suoni
Coin_Sound = pygame.mixer.Sound("Sounds/Coin.mp3")
Win_sound = pygame.mixer.Sound("Sounds/Win.mp3")
GameOver_Sound = pygame.mixer.Sound("Sounds/GameOver.mp3")
Move_Sound = pygame.mixer.Sound("Sounds/Move.mp3")

#Caricamento Canzoni
if MUSIC_ON:
    GameSounds = [pygame.mixer.Sound(f"Sounds/MusicGame{i}.mp3") for i in range(1, 10)]


# Crea la finestra
schermo = pygame.display.set_mode((LARGHEZZA_FINESTRA, ALTEZZA_FINESTRA))
pygame.display.set_caption("Griglia con player")

# Posizione iniziale del player
player_pos = [14,19]  # Riga, Colonna
player_pos_memory = player_pos.copy()

nemici = [
    {"pos": [0, 1], "sprite": sprite_enemy1, "direction": 0},
    {"pos": [0, 19], "sprite": sprite_enemy2, "direction": 0}
    #{"pos": [13, 0], "sprite": sprite_enemy3, "direction": 0}
]

nemici_memory = [{"pos": enemy["pos"][:],  # Copia la posizione (nuova lista)
                  "sprite": enemy["sprite"],  # Mantiene lo stesso sprite
                  "direction": enemy["direction"]}  # Copia la direzione
                 for enemy in nemici]

prolog = Prolog()
prolog.consult("camper_Utilities.pl")

# Flag per evitare il movimento continuo
up_pressed = False
down_pressed = False
left_pressed = False
right_pressed = False


labirinto = [[0 for colonne in range(COLONNE)] for righe in range(RIGHE)]


with open("PiastrelleNere.txt", "r") as file:
     
     for riga in file:
          riga = riga.strip()
          x, y = map(int, riga.strip().split(","))
          labirinto[x][y] = 1
          

#Funzioni di gestione della griglia 

def disegna_Pallini():
    for riga in range(RIGHE):
        for colonna in range(COLONNE):
            if labirinto[riga][colonna] == 0:
                valideCell = [riga,colonna]
                validCellGroup.append(valideCell)
    for i in range(NUMBER_OF_PALLINI):
        cell = random.choice(validCellGroup)
        if cell not in cellWithPallino:  # Controlla che il pallino non sia già stato aggiunto
            
            cellWithPallino.append(cell)
            #print(cellWithPallino[0])
       
            
       
        
                
# Funzione per disegnare la griglia
def disegna_griglia():
    global pallinePrese
    global stopCondition
    global winPlayed
    global gameOverPlayer
    
    
    for riga in range(RIGHE):
        for colonna in range(COLONNE):
            x = colonna * (DIM_QUADRATO + OFFSET)
            y = riga * (DIM_QUADRATO + OFFSET)
            if labirinto[riga][colonna] == 1:
                colore = NERO
                pygame.draw.rect(schermo, colore, (x, y, DIM_QUADRATO, DIM_QUADRATO))
            
            else:
                colore = BIANCO
                pygame.draw.rect(schermo, colore, (x, y, DIM_QUADRATO, DIM_QUADRATO))    
                
            if [riga, colonna] == player_pos:
                schermo.blit(sprite_player, (x, y))
                
                
              # Disegna tutti i nemici
            for nemico in nemici:
                if [riga, colonna] == nemico["pos"]:
                    schermo.blit(nemico["sprite"], (x, y))
                    
                    
                    
            for cella in cellWithPallino:
                if[riga,colonna] == cella:
                    schermo.blit(sprite_pallino, (x, y))
                    if cella == player_pos:
                        cellWithPallino.remove(cella)
                        pallinePrese = pallinePrese + 1
                        if SOUND_ON and pallinePrese < NUMBER_OF_PALLINI:    
                            Coin_Sound.play()
                        
                        
    if pallinePrese == NUMBER_OF_PALLINI:
        stopCondition = True
        x = (LARGHEZZA_FINESTRA - sprite_win.get_width()) // 2
        y = (ALTEZZA_FINESTRA - sprite_win.get_height()) // 2
        schermo.blit(sprite_win, (x, y))
        if winPlayed == False and SOUND_ON:
            Win_sound.play()
            winPlayed = True
            if MUSIC_ON:
                music.stop()
        
    
    else:
        for nemico in nemici:
            if nemico["pos"] == player_pos:
                if IMMORTALITY == False:
                    stopCondition = True
                    x = (LARGHEZZA_FINESTRA - sprite_lose.get_width()) // 2
                    y = (ALTEZZA_FINESTRA - sprite_lose.get_height()) // 2
                    schermo.blit(sprite_lose, (x, y))
                    if gameOverPlayer == False and SOUND_ON:
                        GameOver_Sound.play()
                        gameOverPlayer = True
                        if MUSIC_ON:
                            music.stop()
        
                            
            
#Funzione per aggiornare il movimento del nemico
def aggiorna_posizione_nemico(numMosse):
    global cellWithPallino
    listaPallini = convertiProlog(cellWithPallino)
    for nemico in nemici:
        nemico_pos = nemico["pos"]
        nemico_sprite = nemico["sprite"]
        nemico_dir = nemico["direction"]
        
        # Calcolo della futura direzione e posizione
        start = f"{nemico_pos[0]}/{nemico_pos[1]}"
        goal = f"{player_pos[0]}/{player_pos[1]}"
        query = f"move_camper({start}, {goal},{listaPallini}, NextPos)"
        
        result = list(prolog.query(query))
        risultato = estrai_numeri(str(result))
        [prologX, prologY] = risultato

        # Calcolo direzione per lo sprite
        if nemico_pos[1] > prologY and nemico_dir == 0:
            nemico["sprite"] = pygame.transform.flip(nemico_sprite, True, False)
            nemico["direction"] = 1
        elif nemico_pos[1] < prologY and nemico_dir == 1:
            nemico["sprite"] = pygame.transform.flip(nemico_sprite, True, False)
            nemico["direction"] = 0
        
        # Aggiorna la posizione del nemico
        nemico["pos"] = [prologX, prologY]
        
    numMosse = numMosse +1
    print(numMosse)
    return numMosse 

def aggiungi_nemico():
    global nemici
    if len(nemici)< MAX_MONSTER_NUMBER:
        nuovo_nemico = {
            "pos" : random.choice(posGroup),
            "sprite" : random.choice(spriteGroup),
            "direction" : 0
            
        }
        nemici.append(nuovo_nemico)
        
  
#Funzione per estrarre numeri dalla stringa
def estrai_numeri(stringa):
    numeri = re.findall(r'\d+', stringa)  # Trova tutti i numeri (sequenze di cifre)
    return [int(n) for n in numeri]

def musica_casuale():
    global GameSounds
    global music
    music = random.choice(GameSounds)
    music.set_volume(0.5)
    music.play()
    
if MUSIC_ON:
    musica_casuale()
disegna_Pallini()
# Loop principale
running = True

def restart():
    global gameOverPlayer
    global stopCondition
    global player_pos
    global nemici
    global winPlayed
    global pallinePrese
    global player_pos_memory
    global nemici_memory
    
    player_pos = player_pos_memory
    nemici = nemici_memory
    stopCondition = False
    
    gameOverPlayer = True
    winPlayed = True
    
    pallinePrese = 0
    
    disegna_Pallini()
    disegna_griglia()
    setInitialFlag()

def convertiProlog(lista):
    nuova_lista = [f"{x}/{y}" for x, y in lista]
    return nuova_lista

    
    
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Controllo degli input per spostare il player
        keys = pygame.key.get_pressed()
        
        if stopCondition and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()

        # Gestione del movimento quando i tasti sono premuti
        if keys[pygame.K_UP] and not up_pressed and player_pos[0] > 0 and labirinto[player_pos[0]-1][player_pos[1]] != 1 and stopCondition==False:
            player_pos[0] -= 1
            up_pressed = True  # Set flag per evitare il movimento continuo
            numeroMosse = aggiorna_posizione_nemico(numeroMosse)
            if MONSTER_GENERATION  and numeroMosse % NUMBER_OF_TURN_INFRA_GENERATION == 0 and len(nemici)<= MAX_MONSTER_NUMBER:
                aggiungi_nemico()
            if SOUND_ON:
                Move_Sound.play() 
            print(player_pos)
            
        if keys[pygame.K_DOWN] and not down_pressed and player_pos[0] < RIGHE - 1 and labirinto[player_pos[0]+1][player_pos[1]] != 1 and stopCondition==False:
            player_pos[0] += 1
            down_pressed = True  # Set flag per evitare il movimento continuo
            numeroMosse = aggiorna_posizione_nemico(numeroMosse)
            if MONSTER_GENERATION  and numeroMosse % NUMBER_OF_TURN_INFRA_GENERATION == 0 and len(nemici)<= MAX_MONSTER_NUMBER:
                aggiungi_nemico()
            if SOUND_ON:
                Move_Sound.play()     
            print(player_pos)
            
        if keys[pygame.K_LEFT] and not left_pressed and player_pos[1] > 0 and labirinto[player_pos[0]][player_pos[1]-1] != 1 and stopCondition==False:
            player_pos[1] -= 1
            left_pressed = True  # Set flag per evitare il movimento continuo
            numeroMosse = aggiorna_posizione_nemico(numeroMosse)
            if MONSTER_GENERATION  and numeroMosse % NUMBER_OF_TURN_INFRA_GENERATION == 0 and len(nemici)<= MAX_MONSTER_NUMBER:
                aggiungi_nemico()
            #Gira lo sprite seguendo la direzione
            if playerDirection==1:
                sprite_player = pygame.transform.flip(sprite_player, True, False)
                playerDirection = 0
            if SOUND_ON:
                Move_Sound.play() 
            print(player_pos)
            
            
            
        if keys[pygame.K_RIGHT] and not right_pressed and player_pos[1] < COLONNE - 1 and labirinto[player_pos[0]][player_pos[1]+1] != 1 and stopCondition==False:
            player_pos[1] += 1
            right_pressed = True  # Set flag per evitare il movimento continuo
            numeroMosse = aggiorna_posizione_nemico(numeroMosse)
            if MONSTER_GENERATION  and numeroMosse % NUMBER_OF_TURN_INFRA_GENERATION == 0 and len(nemici)<= MAX_MONSTER_NUMBER:
                aggiungi_nemico()
            if SOUND_ON:
                Move_Sound.play()
            print(player_pos)
            
            #Gira lo sprite seguendo la direzione
            if playerDirection==0:
                sprite_player = pygame.transform.flip(sprite_player, True, False)
                playerDirection = 1

        # Se il tasto viene rilasciato, resettare il flag per il movimento "a casella singola"
        if not keys[pygame.K_UP]:
            up_pressed = False
        if not keys[pygame.K_DOWN]:
            down_pressed = False
        if not keys[pygame.K_LEFT]:
            left_pressed = False
        if not keys[pygame.K_RIGHT]:
            right_pressed = False
            
        
            
        #ENEMY1
            
        
        # Riempie lo schermo con il colore di sfondo
        schermo.fill(NERO)
        #print(player_pos)
        #print(enemy_pos)
        # Disegna la griglia
        disegna_griglia()
        
        # Aggiorna il display
    pygame.display.flip()
    pygame.time.Clock().tick(FPS)
# Chiudi Pygame
pygame.quit()