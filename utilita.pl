% This buffer is for notes you don't want to save.
% If you want to create a file, visit that file with C-x C-f,
% then enter the text in that file's own buffer.

% Distanza Manhattan tra due punti
distanza_manhattan((X1, Y1), (X2, Y2), D) :-
    D is abs(X1 - X2) + abs(Y1 - Y2).

% Funzione di utilit�: distanza tra il nemico e il giocatore
utilita_distanza_nemico_giocatore(Nemico, Giocatore, Utilita) :-
    distanza_manhattan(Nemico, Giocatore, Utilita).

% Funzione di utilit�: distanza tra il giocatore e il pallino pi� vicino
utilita_distanza_giocatore_pallino(Giocatore, Pallini, PallinoPiuVicino, DistanzaMinima) :-
    findall((Distanza, Pallino), (member(Pallino, Pallini), distanza_manhattan(Giocatore, Pallino, Distanza)), Coppie),%creo una lista di coppie che mi permette di conservare il riferimento al pallino che corrisponde alla distanza minima.
    sort(Coppie, [(DistanzaMinima, PallinoPiuVicino)|_]).%ordino la lista in base alla distanza e prendo il il primo elemento che rappresenta il pallino piu vicino

% Funzione di utilit�: distanza tra il nemico e il pallino pi� vicino al giocatore
utilita_distanza_nemico_pallino(Nemico, Giocatore, Pallini, DistanzaNemicoPallino) :-
    utilita_distanza_giocatore_pallino(Giocatore, Pallini, PallinoPiuVicino, _),
    distanza_manhattan(Nemico, PallinoPiuVicino, DistanzaNemicoPallino).%calcolo la distanza tra il pallino piu vicino e il nemico
