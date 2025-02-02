%:-use_module(library(pce)).
:-[mappaprolog].
:- use_module(library(random)).

% Disegna la mappa in base ai predicati p/1 (celle valide)
disegna_pianta(Finestra, Nome, PlayerPosX/PlayerPosY, EnemyPosX/EnemyPosY) :-
    new(Finestra, picture(Nome)),
    send(Finestra, size, size(400, 300)),
    send(Finestra, open),  % apre la finestra grafica

    % Disegna lo sfondo nero
    new(Sfondo, box(800,800)),
    send(Sfondo, fill_pattern, colour(black)),
    send(Finestra, display, Sfondo, point(0, 0)),

    % Disegna le celle (p/1) valide
    forall(p(X/Y), (
        GX is X * 20,
        GY is Y * 20,
        new(M, box(20, 20)),
        send(M, fill_pattern, colour(white)),
        send(Finestra, display, M, point(GY, GX))
    )),

    % Disegna un quadrato rosso player
    PosizionePX = PlayerPosX,
    PosizionePY =PlayerPosY,
    GX_Player is PosizionePX * 20,
    GY_Player is PosizionePY * 20,
    new(Rosso, box(20, 20)),
    send(Rosso, fill_pattern, colour(red)),
    send(Finestra, display, Rosso, point(GY_Player, GX_Player)),


 % Disegna un quadrato verde nemico
    PosizioneEX = EnemyPosX,
    PosizioneEY =EnemyPosY,
    GX_Enemy is PosizioneEX * 20,
    GY_Enemy is PosizioneEY * 20,
    new(Verde, box(20, 20)),
    send(Verde, fill_pattern, colour(green)),
    send(Finestra, display, Verde, point(GY_Enemy, GX_Enemy)).

% Euristica: distanza Manhattan
heuristic(X1/Y1, X2/Y2, H) :-
    H is abs(X1 - X2) + abs(Y1 - Y2).

% Trova la prima mossa valida con A*
a_star_prima_mossa(Start, Goal, NextMove) :-
    a_star_search_prima_mossa([node(Start, 0, 0, [])], [], Goal, NextMove).

% Modifica l'algoritmo A* per fermarsi al primo passo
a_star_search_prima_mossa([node(Pos, _, _, Path)|_], _, Pos, NextMove) :-
    reverse([Pos|Path], [_, NextMove|_]). % Ritorna solo il primo passo dopo la posizione iniziale
a_star_search_prima_mossa([node(Pos, G, _, Path)|Open], Closed, Goal, NextMove) :-
    findall(
        node(Next, GNew, F, [Pos|Path]),
        (   adiacente(Pos, Next, 1),        % Trova i vicini
            \+ member(node(Next, _, _, _), Closed), % Non deve essere nei chiusi
            \+ member(node(Next, _, _, _), Open),   % Non deve essere negli aperti
            GNew is G + 1,                          % Incrementa il costo
            heuristic(Next, Goal, H),               % Calcola l'euristica
            F is GNew + H                           % Calcola il costo totale
        ),
        Neighbors
    ),
    append(Open, Neighbors, NewOpen),
    sort(2, @=<, NewOpen, SortedOpen), % Ordina per F (minore è meglio)
    a_star_search_prima_mossa(SortedOpen, [node(Pos, G, _, Path)|Closed], Goal, NextMove).



% Adiacenze
adiacente(X/Y, X1/Y, 1) :- X1 is X + 1, p(X1/Y).
adiacente(X/Y, X/Y1, 1) :- Y1 is Y + 1, p(X/Y1).
adiacente(X/Y, X1/Y, 1) :- X1 is X - 1, p(X1/Y).
adiacente(X/Y, X/Y1, 1) :- Y1 is Y - 1, p(X/Y1).


% Movimento casuale del nemico
nemico_vaga(PosizioneCorrente, NuovaPosizione) :-
    findall(Adiacente, adiacente(PosizioneCorrente, Adiacente, 1), MossePossibili),
    random_member(NuovaPosizione, MossePossibili).

% Verifica se il nemico vede il giocatore sulla stessa riga o colonna (senza ostacoli)
vede_giocatore(NemicoPos, GiocatorePos) :-
    NemicoPos = X/Y,
    GiocatorePos = X/YG,  % stessa colonna
    percorso_libero_verticale(Y, YG, X).

vede_giocatore(NemicoPos, GiocatorePos) :-
    NemicoPos = X/Y,
    GiocatorePos = XG/Y,  % stessa riga
    percorso_libero_orizzontale(X, XG, Y).

% Percorso libero verticalmente
percorso_libero_verticale(Y1, Y2, X) :-
    MinY is min(Y1, Y2),
    MaxY is max(Y1, Y2),
    forall(between(MinY, MaxY, Y), p(X/Y)).

% Percorso libero orizzontalmente
percorso_libero_orizzontale(X1, X2, Y) :-
    MinX is min(X1, X2),
    MaxX is max(X1, X2),
    forall(between(MinX, MaxX, X), p(X/Y)).

% Comportamento del nemico: vaga o insegue il giocatore
muovi_nemico(NemicoPos, GiocatorePos, NuovaPosizione) :-
    (   vede_giocatore(NemicoPos, GiocatorePos) -> % se il nemico vede il giocatore allora lo insegue con A* senno continua a vagare
        a_star_prima_mossa(NemicoPos, GiocatorePos, NuovaPosizione)
    ;   nemico_vaga(NemicoPos, NuovaPosizione)
    ).
