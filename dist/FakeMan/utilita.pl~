% This buffer is for notes you don't want to save.
% If you want to create a file, visit that file with C-x C-f,
% then enter the text in that file's own buffer.

% Distanza Manhattan tra due punti
distanza_manhattan_norm(X1/Y1, X2/Y2, D) :-
    D is (abs(X1 - X2) + abs(Y1 - Y2)) / 38.

% Funzione di utilità: distanza tra il giocatore e il pallino più vicino
distanza_giocatore_pallino(Giocatore, Pallini, PallinoPiuVicino, DistanzaMinima) :-
    findall((Distanza, Pallino), (member(Pallino, Pallini), distanza_manhattan_norm(Giocatore, Pallino, Distanza)), Coppie),%creo una lista di coppie che mi permette di conservare il riferimento al pallino che corrisponde alla distanza minima.
    sort(Coppie, [(DistanzaMinima, PallinoPiuVicino)|_]).%ordino la lista in base alla distanza e prendo il il primo elemento che rappresenta il pallino piu vicino

% Funzione di utilità: distanza tra il nemico e il pallino più vicino al giocatore
distanza_nemico_pallino(Nemico, Giocatore, Pallini, DistanzaNemicoPallino) :-
    distanza_giocatore_pallino(Giocatore, Pallini, PallinoPiuVicino, _),
    distanza_manhattan_norm(Nemico, PallinoPiuVicino, DistanzaNemicoPallino).%calcolo la distanza tra il pallino piu vicino e il nemico

% Determino i ruoli dei nemici in base alla loro distanza
ruoli_nemici(Nemico1, Nemico2, Giocatore, Inseguitore, Anticipatore) :-
    distanza_manhattan_norm(Nemico1, Giocatore, Distanza1),
    distanza_manhattan_norm(Nemico2, Giocatore, Distanza2),
    ( Distanza1 =< Distanza2 ->
        Inseguitore = Nemico1, %inseguitore e' il nemico piu vicino al giocatore
        Anticipatore = Nemico2 %anticipatore e' il nemico piu lontano dal giocatore
    ;
        Inseguitore = Nemico2,
        Anticipatore = Nemico1
    ).

% Predico la prossima posizione del giocatore verso il pallino più
% vicino
predire_mossa_giocatore(Giocatore, PallinoPiuVicino, NuovaPosizione) :-
    Giocatore = (XG, YG),
    PallinoPiuVicino = (XP, YP),
    (   XG < XP -> NuovaPosizione = (XG + 1, YG) % Muove a destra
    ;   XG > XP -> NuovaPosizione = (XG - 1, YG) % Muove a sinistra
    ;   YG < YP -> NuovaPosizione = (XG, YG + 1) % Muove in basso
    ;   YG > YP -> NuovaPosizione = (XG, YG - 1) % Muove in alto
    ).

% Utilità collaborativa: i nemici collaborano per ridurre le opzioni di fuga del giocatore
collaborazione_nemici(Nemico1, Nemico2, Giocatore, Pallini, MossaMigliore) :-
    % Inizio determinando i ruoli
    ruoli_nemici(Nemico1, Nemico2, Giocatore, Inseguitore, Anticipatore),
    % Predico la prossima posizione del giocatore verso il pallino più vicino
    distanza_giocatore_pallino(Giocatore, Pallini, PallinoPiuVicino, _),
    predire_mossa_giocatore(Giocatore, PallinoPiuVicino, PosizionePredetta),
    % Calcolo la distanza di ciascun nemico verso la posizione predetta
    distanza_manhattan_norm(Inseguitore, PosizionePredetta, DistanzaInseguitore),
    distanza_manhattan_norm(Anticipatore, PosizionePredetta, DistanzaAnticipatore),
    % Infine scelgo la mossa migliore per entrambi
    ( DistanzaInseguitore =< DistanzaAnticipatore ->
        MossaMigliore = insegui(PosizionePredetta)
    ;
        MossaMigliore = anticipa(PosizionePredetta)
    ).
