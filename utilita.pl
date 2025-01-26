% This buffer is for notes you don't want to save.
% If you want to create a file, visit that file with C-x C-f,
% then enter the text in that file's own buffer.

% Distanza Manhattan tra due punti
distanza_manhattan((X1, Y1), (X2, Y2), D) :-
    D is abs(X1 - X2) + abs(Y1 - Y2).

% Funzione di utilità: distanza tra il nemico e il giocatore
utilita_distanza_nemico_giocatore(Nemico, Giocatore, Utilita) :-
    distanza_manhattan(Nemico, Giocatore, Utilita).

% Funzione di utilità: distanza tra il nemico e il pallino più vicino
utilita_distanza_nemico_pallino(Nemico, Pallini, DistanzaMinima) :-
    findall(Distanza, (member(Pallino, Pallini), distanza_manhattan(Nemico, Pallino, Distanza)), Distanze),%genera una lista di distanze tra il nemico e tutti i pallini
    min_list(Distanze, DistanzaMinima).%trova la distanza minima da quella lista, che rappresenta il pallino più vicino al nemico
