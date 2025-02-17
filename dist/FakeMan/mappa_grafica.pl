

disegna_pianta(Finestra, Nome) :-
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
    )).
