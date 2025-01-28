from pyswip import Prolog
import pygame
import re


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

sprite_player = pygame.image.load("immagini/FakeMan.png")
sprite_player = pygame.transform.scale(sprite_player, (DIM_QUADRATO, DIM_QUADRATO))
sprite_player = pygame.transform.flip(sprite_player, True, False)

# Crea la finestra
schermo = pygame.display.set_mode((LARGHEZZA_FINESTRA, ALTEZZA_FINESTRA))
pygame.display.set_caption("Griglia con player")

# Posizione iniziale del player
player_pos = [14,19]  # Riga, Colonna
enemy_pos = [0,1]
enemy2_pos = [0,19]
enemy3_pos = [13,0]

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


# Funzione per disegnare la griglia
def disegna_griglia():
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
            elif [riga, colonna] == enemy_pos:
                colore = BLU
            elif [riga,colonna] == enemy2_pos:
                colore = VERDE
            elif [riga,colonna] == enemy3_pos:
                colore = AZZURRO
            
                
            
            
def aggiorna_posizione_nemico(enemyStart, enemyEnd):
    start = f"{enemyStart}/{enemyEnd}"
    goal = f"{player_pos[0]}/{player_pos[1]}"
    query = f"a_star_prima_mossa({start}, {goal}, NextMove)"
    
    result = list(prolog.query(query))
    
    risultato = estrai_numeri(str(result))
    [prologX, prologY] = risultato  
    return [prologX,prologY]
    
    
  
                       
def estrai_numeri(stringa):
    numeri = re.findall(r'\d+', stringa)  # Trova tutti i numeri (sequenze di cifre)
    return [int(n) for n in numeri]

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
    if keys[pygame.K_UP] and not up_pressed and player_pos[0] > 0 and labirinto[player_pos[0]-1][player_pos[1]] != 1:
        player_pos[0] -= 1
        up_pressed = True  # Set flag per evitare il movimento continuo
        enemy_pos = aggiorna_posizione_nemico(enemy_pos[0],enemy_pos[1])
        enemy2_pos = aggiorna_posizione_nemico(enemy2_pos[0],enemy2_pos[1])
        enemy3_pos = aggiorna_posizione_nemico(enemy3_pos[0],enemy3_pos[1])
        
    if keys[pygame.K_DOWN] and not down_pressed and player_pos[0] < RIGHE - 1 and labirinto[player_pos[0]+1][player_pos[1]] != 1:
        player_pos[0] += 1
        down_pressed = True  # Set flag per evitare il movimento continuo
        enemy_pos = aggiorna_posizione_nemico(enemy_pos[0],enemy_pos[1])
        enemy2_pos = aggiorna_posizione_nemico(enemy2_pos[0],enemy2_pos[1])
        enemy3_pos = aggiorna_posizione_nemico(enemy3_pos[0],enemy3_pos[1])
        
    if keys[pygame.K_LEFT] and not left_pressed and player_pos[1] > 0 and labirinto[player_pos[0]][player_pos[1]-1] != 1:
        player_pos[1] -= 1
        left_pressed = True  # Set flag per evitare il movimento continuo
        enemy_pos = aggiorna_posizione_nemico(enemy_pos[0],enemy_pos[1])
        enemy2_pos = aggiorna_posizione_nemico(enemy2_pos[0],enemy2_pos[1])
        enemy3_pos = aggiorna_posizione_nemico(enemy3_pos[0],enemy3_pos[1])
        
    if keys[pygame.K_RIGHT] and not right_pressed and player_pos[1] < COLONNE - 1 and labirinto[player_pos[0]][player_pos[1]+1] != 1:
        player_pos[1] += 1
        right_pressed = True  # Set flag per evitare il movimento continuo
        enemy_pos = aggiorna_posizione_nemico(enemy_pos[0],enemy_pos[1])
        enemy2_pos = aggiorna_posizione_nemico(enemy2_pos[0],enemy2_pos[1])
        enemy3_pos = aggiorna_posizione_nemico(enemy3_pos[0],enemy3_pos[1])
        

    # Se il tasto viene rilasciato, resettare il flag
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
    
