from pyswip import Prolog
import pygame
import re
import random


# Inizializza Pygame
pygame.init()

 
 # Costanti
DIM_QUADRATO = 30         # Dimensione di un quadrato
OFFSET = 5                # Spazio tra i quadrati
RIGHE = 15                # Numero di righe
COLONNE = 20       

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

#Flag
MONSTER_GENERATION = False
MAX_MONSTER_NUMBER = 5
NUMBER_OF_TURN_INFRA_GENERATION = 7
NUMBER_OF_PALLINI = 1
IMMORTALITY = True

#booleani per il controllo delle animazioni
playerDirection = 0 #1 is right || #0 is left
numeroMosse = 0 #contatore mosse
pallinePrese = 0
stopCondition = False

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


# Crea la finestra
schermo = pygame.display.set_mode((LARGHEZZA_FINESTRA, ALTEZZA_FINESTRA))
pygame.display.set_caption("Griglia con player")

# Posizione iniziale del player
player_pos = [14,19]  # Riga, Colonna

nemici = [
    {"pos": [0, 1], "sprite": sprite_enemy1, "direction": 0},
    {"pos": [0, 19], "sprite": sprite_enemy2, "direction": 0},
    {"pos": [13, 0], "sprite": sprite_enemy3, "direction": 0}
]

prolog = Prolog()
prolog.consult("movimentoPupi2.pl")

# Flag per evitare il movimento continuo
up_pressed = False
down_pressed = False
left_pressed = False
right_pressed = False

a_pressed = False
s_pressed = False
w_pressed = False
d_pressed = False

f_pressed = False
g_pressed = False
h_pressed = False
t_pressed = False

labirinto = [[0 for colonne in range(COLONNE)] for righe in range(RIGHE)]


with open("labirinto.txt", "r") as file:
     
     for riga in file:
          riga = riga.strip()
          x, y = map(int, riga.strip().split(","))
          labirinto[x][y] = 1

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
       
        
                
# Funzione per disegnare la griglia
def disegna_griglia():
    global pallinePrese
    global stopCondition
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
                        
                        
    if pallinePrese == NUMBER_OF_PALLINI:
        stopCondition = True
        x = (LARGHEZZA_FINESTRA - sprite_win.get_width()) // 2
        y = (ALTEZZA_FINESTRA - sprite_win.get_height()) // 2
        schermo.blit(sprite_win, (x, y))
    
    for nemico in nemici:
        if nemico["pos"] == player_pos:
            if IMMORTALITY == False:
                stopCondition = True
                x = (LARGHEZZA_FINESTRA - sprite_lose.get_width()) // 2
                y = (ALTEZZA_FINESTRA - sprite_lose.get_height()) // 2
                schermo.blit(sprite_lose, (x, y))
             
        
                            
            
#Funzione per aggiornare il movimento del nemico
def aggiorna_posizione_nemico(numMosse):
    
    for nemico in nemici:
        nemico_pos = nemico["pos"]
        nemico_sprite = nemico["sprite"]
        nemico_dir = nemico["direction"]
        
        # Calcolo della futura direzione e posizione
        start = f"{nemico_pos[0]}/{nemico_pos[1]}"
        goal = f"{player_pos[0]}/{player_pos[1]}"
        query = f"a_star_prima_mossa({start}, {goal}, NextMove)"
        
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
    if len(nemici)<= MAX_MONSTER_NUMBER:
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

disegna_Pallini()
# Loop principale
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controllo degli input per spostare il player
    keys = pygame.key.get_pressed()
    
    #PLAYER1

    # Gestione del movimento quando i tasti sono premuti
    if keys[pygame.K_UP] and not up_pressed and player_pos[0] > 0 and labirinto[player_pos[0]-1][player_pos[1]] != 1 and stopCondition==False:
        player_pos[0] -= 1
        up_pressed = True  # Set flag per evitare il movimento continuo
        numeroMosse = aggiorna_posizione_nemico(numeroMosse)
        if MONSTER_GENERATION  and numeroMosse % NUMBER_OF_TURN_INFRA_GENERATION == 0:
            aggiungi_nemico()
            
    if keys[pygame.K_DOWN] and not down_pressed and player_pos[0] < RIGHE - 1 and labirinto[player_pos[0]+1][player_pos[1]] != 1 and stopCondition==False:
        player_pos[0] += 1
        down_pressed = True  # Set flag per evitare il movimento continuo
        numeroMosse = aggiorna_posizione_nemico(numeroMosse)
        if MONSTER_GENERATION  and numeroMosse % NUMBER_OF_TURN_INFRA_GENERATION == 0:
            aggiungi_nemico()
            
    if keys[pygame.K_LEFT] and not left_pressed and player_pos[1] > 0 and labirinto[player_pos[0]][player_pos[1]-1] != 1 and stopCondition==False:
        player_pos[1] -= 1
        left_pressed = True  # Set flag per evitare il movimento continuo
        numeroMosse = aggiorna_posizione_nemico(numeroMosse)
        if MONSTER_GENERATION  and numeroMosse % NUMBER_OF_TURN_INFRA_GENERATION == 0:
            aggiungi_nemico()
        #Gira lo sprite seguendo la direzione
        if playerDirection==1:
            sprite_player = pygame.transform.flip(sprite_player, True, False)
            playerDirection = 0
        
    if keys[pygame.K_RIGHT] and not right_pressed and player_pos[1] < COLONNE - 1 and labirinto[player_pos[0]][player_pos[1]+1] != 1 and stopCondition==False:
        player_pos[1] += 1
        right_pressed = True  # Set flag per evitare il movimento continuo
        numeroMosse = aggiorna_posizione_nemico(numeroMosse)
        if MONSTER_GENERATION  and numeroMosse % NUMBER_OF_TURN_INFRA_GENERATION == 0:
            aggiungi_nemico()
            
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

# Chiudi Pygame
pygame.quit()



""" 
    if keys[pygame.K_w] and not w_pressed and enemy_pos[0] > 0 and labirinto[enemy_pos[0]-1][enemy_pos[1]] != 1: 
        enemy_pos[0] -= 1
        w_pressed = True  # Set flag per evitare il movimento continuo
    if keys[pygame.K_s] and not s_pressed and enemy_pos[0] < RIGHE - 1 and labirinto[enemy_pos[0]+1][enemy_pos[1]] != 1:
        enemy_pos[0] += 1
        s_pressed = True  # Set flag per evitare il movimento continuo
    if keys[pygame.K_a] and not a_pressed and enemy_pos[1] > 0 and labirinto[enemy_pos[0]][enemy_pos[1]-1] != 1:
        enemy_pos[1] -= 1
        a_pressed = True  # Set flag per evitare il movimento continuo
    if keys[pygame.K_d] and not d_pressed and enemy_pos[1] < COLONNE - 1 and labirinto[enemy_pos[0]][enemy_pos[1]+1] != 1:
        enemy_pos[1] += 1
        d_pressed = True  # Set flag per evitare il movimento continuo

    # Se il tasto viene rilasciato, resettare il flag
    if not keys[pygame.K_w]:
        w_pressed = False
    if not keys[pygame.K_s]:
        s_pressed = False
    if not keys[pygame.K_a]:
        a_pressed = False
    if not keys[pygame.K_d]:
        d_pressed = False   
        
    #ENEMY2
    
    if keys[pygame.K_t] and not t_pressed and enemy2_pos[0] > 0 and labirinto[enemy2_pos[0]-1][enemy2_pos[1]] != 1: 
        enemy2_pos[0] -= 1
        t_pressed = True  # Set flag per evitare il movimento continuo
    if keys[pygame.K_g] and not g_pressed and enemy2_pos[0] < RIGHE - 1 and labirinto[enemy2_pos[0]+1][enemy2_pos[1]] != 1:
        enemy2_pos[0] += 1
        g_pressed = True  # Set flag per evitare il movimento continuo
    if keys[pygame.K_f] and not f_pressed and enemy2_pos[1] > 0 and labirinto[enemy2_pos[0]][enemy2_pos[1]-1] != 1:
        enemy2_pos[1] -= 1
        f_pressed = True  # Set flag per evitare il movimento continuo
    if keys[pygame.K_h] and not h_pressed and enemy2_pos[1] < COLONNE - 1 and labirinto[enemy2_pos[0]][enemy2_pos[1]+1] != 1:
        enemy2_pos[1] += 1
        h_pressed = True  # Set flag per evitare il movimento continuo

    # Se il tasto viene rilasciato, resettare il flag
    if not keys[pygame.K_t]:
        t_pressed = False
    if not keys[pygame.K_g]:
        g_pressed = False
    if not keys[pygame.K_f]:
        f_pressed = False
    if not keys[pygame.K_h]:
        h_pressed = False   
    """
    
