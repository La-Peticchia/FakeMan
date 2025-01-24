

:-use_module(library(pce)).
:-[mappaprolog].

adiacente(X1/Y,X2/Y,1) :- X2 is X1 + 1. % verso EST
adiacente(X/Y1,X/Y2,1) :- Y2 is Y1 - 1. % verso SUD
adiacente(X1/Y,X2/Y,1) :- X2 is X1 - 1. % verso OVEST
adiacente(X/Y1,X/Y2,1) :- Y2 is Y1 + 1. % verso NORD

:- use_module(library(pce)).

% Disegna la mappa in base ai predicati p/1 (celle valide)
disegna_pianta(Finestra, Nome) :-
    new(Finestra, picture(Nome)),
    send(Finestra, open),  % apre la finestra grafica

    % Disegna lo sfondo nero
    new(Sfondo, box(400, 400)),
    send(Sfondo, fill_pattern, colour(black)),
    send(Finestra, display, Sfondo, point(0, 0)),

    % Disegna le celle (p/1) valide
    forall(p(X/Y), (
        GX is X * 20,
        GY is Y * 20,
        new(M, box(20, 20)),
        send(M, fill_pattern, colour(white)),
        send(Finestra, display, M, point(GY, GX))
    )).

