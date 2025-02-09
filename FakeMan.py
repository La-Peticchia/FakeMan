from pyswip import Prolog
import pygame
import re
import random

# Inizializza Pygame
pygame.init()

# Inizializza mixer per i suoni
pygame.mixer.init()
 
# Costanti
DIM_QUADRATO = 30         # Dimensione di un quadrato
OFFSET = 5                # Spazio tra i quadrati
RIGHE = 15                # Numero di righe
COLONNE = 20              #colonne    

# Altezza e larghezza finestra
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

# Font
font = pygame.font.Font(None, 50)

#funzione che setta i parametri iniziali di configurazione
def setInitialFlag():
    global MONSTER_GENERATION
    global MAX_MONSTER_NUMBER 
    global NUMBER_OF_TURN_INFRA_GENERATION 
    global NUMBER_OF_PALLINI 
    global IMMORTALITY
    global SOUND_ON 
    global MUSIC_ON
        
    MONSTER_GENERATION = True
    MAX_MONSTER_NUMBER = 4
    NUMBER_OF_TURN_INFRA_GENERATION = 5
    NUMBER_OF_PALLINI = 3
    IMMORTALITY = False
    SOUND_ON = True
    MUSIC_ON = True

setInitialFlag()

#booleani per il controllo delle animazioni
playerDirection = 0     #1 is right || #0 is left
numeroMosse = 0         #contatore mosse
pallinePrese = 0        #contatore delle palline collezionate 
stopCondition = False   #flag per fermare il gioco 
winPlayed = False       #stato di vittoria
gameOverPlayer = False  #stato di sconfitta

#Loading dello sprite player
sprite_player = pygame.image.load("immagini/FakeMan.png")
sprite_player = pygame.transform.scale(sprite_player, (DIM_QUADRATO, DIM_QUADRATO))
sprite_player = pygame.transform.flip(sprite_player, True, False)

#Sprite Nemico 1
sprite_enemy1 = pygame.image.load("immagini/Arancione.png")
sprite_enemy1 = pygame.transform.scale(sprite_enemy1, (DIM_QUADRATO, DIM_QUADRATO))

#Sprite Nemico 2
sprite_enemy2 = pygame.image.load("immagini/Blu.png")
sprite_enemy2 = pygame.transform.scale(sprite_enemy2, (DIM_QUADRATO, DIM_QUADRATO))

#Sprite Nemico 3
sprite_enemy3 = pygame.image.load("immagini/Rosso.png")
sprite_enemy3 = pygame.transform.scale(sprite_enemy3, (DIM_QUADRATO, DIM_QUADRATO))

#Sprite pallino
sprite_pallino = pygame.image.load("immagini/pallino.png")
sprite_pallino = pygame.transform.scale(sprite_pallino, (DIM_QUADRATO, DIM_QUADRATO))

#Sprite Scritta win
sprite_win = pygame.image.load("immagini/YouWin.png")
sprite_win = pygame.transform.scale(sprite_win,(ALTEZZA_FINESTRA//2, LARGHEZZA_FINESTRA//2))

#Sprite Scritta lose
sprite_lose = pygame.image.load("immagini/GameOver.png")
sprite_lose = pygame.transform.scale(sprite_lose,(ALTEZZA_FINESTRA, LARGHEZZA_FINESTRA))

#Array per contenere le variabili di gioco
spriteGroup = [sprite_enemy1, sprite_enemy2, sprite_enemy3] #contiene gli sprite per il random
posGroup = [[0,1],[0,19],[13,0]]    #contiene le posizioni di spawn dei nemici
validCellGroup = []   #contiene le celle in cui può spawnare il pallino
cellWithPallino = []  #contiene le celle in cui effettivamente sarà presente il pallino

#Caricamento Suoni
Coin_Sound = pygame.mixer.Sound("Sounds/Coin.mp3")  #preso il pallino
Win_sound = pygame.mixer.Sound("Sounds/Win.mp3")    #vittoria
GameOver_Sound = pygame.mixer.Sound("Sounds/GameOver.mp3") #sconfitta
Move_Sound = pygame.mixer.Sound("Sounds/Move.mp3")      #pop di movimento

#Caricamento Canzoni per il random
if MUSIC_ON:
    GameSounds = [pygame.mixer.Sound(f"Sounds/MusicGame{i}.mp3") for i in range(1, 10)]


# Crea la finestra, nome e icona
schermo = pygame.display.set_mode((LARGHEZZA_FINESTRA, ALTEZZA_FINESTRA))
pygame.display.set_caption("FakeMan")
pygame.display.set_icon(sprite_player)

# Posizione iniziale del player
player_pos = [14,19]  # Riga, Colonna
player_pos_memory = player_pos.copy() #copia delle posizioni iniziali

#array che contiene tutti i dati dei nemici iniziali (e quelli futuri)
nemici = [
    {"pos": [0, 1], "sprite": sprite_enemy1, "direction": 0, "role": 0}, #0 camper. 1 follower 
    {"pos": [0, 19], "sprite": sprite_enemy2, "direction": 0, "role": 1}
    #{"pos": [13, 0], "sprite": sprite_enemy3, "direction": 0}
]

#Copia backup per restart
nemici_memory = [{"pos": enemy["pos"][:],  # Copia la posizione (nuova lista)
                  "sprite": enemy["sprite"],  # Mantiene lo stesso sprite
                  "direction": enemy["direction"], # Copia la direzione
                  "role": enemy["role"]}  #Copia il ruolo
                 for enemy in nemici]

#caricamento file prolog
prolog = Prolog()
prolog.consult("camper_Utilities.pl")
prolog.consult("follower_Utilities.pl")

# Flag per evitare il movimento continuo
up_pressed = False
down_pressed = False
left_pressed = False
right_pressed = False

#Genero una matrice di 0 per creare il campo da gioco
labirinto = [[0 for colonne in range(COLONNE)] for righe in range(RIGHE)]

#Carico il file che contiene le caselle nere
with open("PiastrelleNere.txt", "r") as file:
    
    #Leggo il file e genero 1 nella matrice dove si trova una parete 
    for riga in file:
        riga = riga.strip() #leggo riga per riga
        x, y = map(int, riga.strip().split(",")) #divido i termini che sono separati da una virgola "," (formato x,y )
        labirinto[x][y] = 1
          

########################### Funzioni di gestione della griglia ##############################################################

#Funzione della generazione randomica dei pallini
def disegna_Pallini():
    prolog.retractall(f"ballPos(_)")
    for riga in range(RIGHE):
        for colonna in range(COLONNE): #due if anniadati
            if labirinto[riga][colonna] == 0: #valuto dove posso spawnare pallini
                valideCell = [riga,colonna]
                validCellGroup.append(valideCell)
    for i in range(NUMBER_OF_PALLINI):
        cell = random.choice(validCellGroup)
        if cell not in cellWithPallino:  # Controlla che il pallino non sia già stato aggiunto
            cellWithPallino.append(cell)
            cellString = f"{cell[0]}/{cell[1]}"
            prolog.assertz(f"ballPos({cellString})")

            
#Disegno la scritta di restart
def draw_restart_message():
    text = font.render("Press R to restart", True, ROSSO)
    text_rect = text.get_rect(center=(LARGHEZZA_FINESTRA // 2, ALTEZZA_FINESTRA - 55))
    schermo.blit(text, text_rect)             
               
                
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
                            Coin_Sound.set_volume(0.5)    
                            Coin_Sound.play()
                                             
    if pallinePrese == NUMBER_OF_PALLINI:
        stopCondition = True
        x = (LARGHEZZA_FINESTRA - sprite_win.get_width()) // 2
        y = (ALTEZZA_FINESTRA - sprite_win.get_height()) // 2
        schermo.blit(sprite_win, (x, y))
        draw_restart_message()
        if winPlayed == False and SOUND_ON:
            Win_sound.set_volume(0.5)
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
                    draw_restart_message()
                    if gameOverPlayer == False and SOUND_ON:
                        GameOver_Sound.set_volume(0.1)
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
        nemico_role = nemico["role"]
        
        # Calcolo della futura direzione e posizione
        start = f"{nemico_pos[0]}/{nemico_pos[1]}"
        goal = f"{player_pos[0]}/{player_pos[1]}"
        
        queryCamper = f"move_camper({start}, {goal}, NextPos)"
        queryFollow = f"move_follower({start}, {goal}, NuovaPosizione)"
        
        
        # Aggiorna la posizione del nemico
        if nemico_role == 0:
            risultatoCamper = estrai_numeri(str(list(prolog.query(queryCamper))))
       
            #catturo l'eccezione che viene generata nell'eccessiva velocità del gioco
            try:
                [prologXCamper, prologYCamper] = risultatoCamper
            except Exception as e:
                [prologXCamper, prologYCamper] = [risultatoCamper[0],risultatoCamper[1]]

            nemico["pos"] = [prologXCamper, prologYCamper]
            print("^ Camper ^")            
        else:
            [prologXFollow, prologYFollow] = estrai_numeri(str(list(prolog.query(queryFollow))))  
            nemico["pos"] = [prologXFollow, prologYFollow]
            print("^ Follower ^")

        # Calcolo direzione per lo sprite
        if nemico_pos[1] > prologYCamper and nemico_dir == 0:
            nemico["sprite"] = pygame.transform.flip(nemico_sprite, True, False)
            nemico["direction"] = 1
        elif nemico_pos[1] < prologYCamper and nemico_dir == 1:
            nemico["sprite"] = pygame.transform.flip(nemico_sprite, True, False)
            nemico["direction"] = 0
        
        
    numMosse = numMosse +1
    
    return numMosse 

def aggiungi_nemico():
    global nemici
    role = random.sample([0,1],1)[0]
    if len(nemici)< MAX_MONSTER_NUMBER:
        nuovo_nemico = {
            "pos" : random.choice(posGroup),
            "sprite" : random.choice(spriteGroup),
            "direction" : 0,
            "role" : role
            
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
    global numeroMosse
    
    player_pos = player_pos_memory.copy()
    
    nemici = [{"pos": enemy["pos"][:],  # Copia la posizione (nuova lista)
                  "sprite": enemy["sprite"],  # Mantiene lo stesso sprite
                  "direction": enemy["direction"], # Copia la direzione
                  "role": enemy["role"]}  #Copia il ruolo
                 for enemy in nemici_memory]
    
    stopCondition = False
    gameOverPlayer = True
    winPlayed = True
    numeroMosse = 0
    pallinePrese = 0
    if cellWithPallino:
        cellWithPallino.clear()
    disegna_Pallini()
    disegna_griglia()
    setInitialFlag()
    if MUSIC_ON:
        musica_casuale()

#Funzione di supporto 
def convertiProlog(lista):
    nuova_lista = [f"{x}/{y}" for x, y in lista]
    return nuova_lista

############################################### Inizio Loop di gioco ############################################################################    
    
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
               
        if keys[pygame.K_DOWN] and not down_pressed and player_pos[0] < RIGHE - 1 and labirinto[player_pos[0]+1][player_pos[1]] != 1 and stopCondition==False:
            player_pos[0] += 1
            down_pressed = True  # Set flag per evitare il movimento continuo 
            numeroMosse = aggiorna_posizione_nemico(numeroMosse)
            if MONSTER_GENERATION  and numeroMosse % NUMBER_OF_TURN_INFRA_GENERATION == 0 and len(nemici)<= MAX_MONSTER_NUMBER:
                aggiungi_nemico()
            if SOUND_ON:
                Move_Sound.play()     
                
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
             
        if keys[pygame.K_RIGHT] and not right_pressed and player_pos[1] < COLONNE - 1 and labirinto[player_pos[0]][player_pos[1]+1] != 1 and stopCondition==False:
            player_pos[1] += 1
            right_pressed = True  # Set flag per evitare il movimento continuo
            
            numeroMosse = aggiorna_posizione_nemico(numeroMosse)
            if MONSTER_GENERATION  and numeroMosse % NUMBER_OF_TURN_INFRA_GENERATION == 0 and len(nemici)<= MAX_MONSTER_NUMBER:
                aggiungi_nemico()
            if SOUND_ON:
                Move_Sound.play()
            
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
                   
        # Riempie lo schermo con il colore di sfondo
        schermo.fill(NERO)
      
        # Disegna la griglia
        disegna_griglia()
        
        # Aggiorna il display
    pygame.display.flip()
    
# Chiudi Pygame
pygame.quit()