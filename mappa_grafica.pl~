/*
 copyright Aldo Franco Dragoni
 october 31 2018

11 ******************
10 * INGRESSO *   C *
 9 *              U *
 8 ************   C *
 7 * BAGNO        I *
 6 *	          N *
 5 ************   A *
 4 * CAMERA   *     *
 3 *	      *	    *
 2 *		    *
 1 *		    *a
 0 ******************
   012345678901234567
*/

%:- new(@p1, picture('Il piccolo esploratore Tobia')), send(@p1, open).

disegna_pianta(Finestra, Nome) :-
    new(Finestra, picture(Nome)),
    send(Finestra, open),                    % apre la finestra grafica
    (   between(11, 18, X),                      % disegna il corridoio
        between(1, 18, Y),
            GX is X * 20,
            GY is Y * 20,
            new(M,box(20,20)),
            send(Finestra, display, M, point(GX,GY)),
        fail ; true
    ),
    (   between(1, 10, X),                      % disegna stanza gialla
        between(1, 4, Y),
            GX is X * 20,
            GY is Y * 20,
            new(M,box(20,20)),
            send(M, fill_pattern, colour(yellow)),
            send(Finestra, display, M, point(GX,GY)),
        fail ; true
    ),
    (   between(1, 10, X),                        % disegnastanza verde
        between(6, 10, Y),
            GX is X * 20,
            GY is Y * 20,
            new(M,box(20,20)),
            send(M, fill_pattern, colour(green)),
            send(Finestra, display, M, point(GX,GY)),
        fail ; true
    ),
    (   between(1, 10, X),                      % disegna stanza grigia
        between(12,18, Y),
            GX is X * 20,
            GY is Y * 20,
            new(M,box(20,20)),
            send(M, fill_pattern, colour(gray)),
            send(Finestra, display, M, point(GX,GY)),
        fail ; true
    ),
    (   between(0, 19, X),                        % disegna parete nord
            GX is X * 20,
            new(M, box(20,20)),
            send(M, fill_pattern, colour(black)),
            send(Finestra,display,M,point(GX,0)) ,
        fail ; true
    ) ,

    (   between(0, 19, Y),                       % disegna parete ovest
            GY is Y * 20,
            new(M, box(20,20)),
            send(M, fill_pattern, colour(black)),
            send(Finestra,display,M,point(0,GY)) ,
        fail ; true
    ) ,

    (   between(0, 19, X),                         % disegna parete sud
            GX is X * 20,
            new(M, box(20,20)),
            send(M, fill_pattern, colour(black)),
            send(Finestra,display,M,point(GX,380)) ,
        fail ; true
    ) ,
    (   between(0, 19, Y),                         % disegna parete est
            GY is Y * 20,
            new(M, box(20,20)),
            send(M, fill_pattern, colour(black)),
            send(Finestra,display,M,point(380,GY)) ,
        fail ; true
    ) ,
    (   between(1, 10, X),             % disegna divisorio giallo-verde
            GX is X * 20,
            new(M, box(20,20)),
            send(M, fill_pattern, colour(black)),
            send(Finestra,display,M,point(GX,100)) ,
        fail ; true
    ) ,
    (   between(1, 10, X),             % disegna divisorio verde-grigio
            GX is X * 20,
            new(M, box(20,20)),
            send(M, fill_pattern, colour(black)),
            send(Finestra,display,M,point(GX,220)) ,
        fail ; true
    ),
    new(M1, box(20,20)),                             % disegna ingresso
            send(M1, fill_pattern, colour(white)),
            send(Finestra,display,M1,point(0,40)),
    new(M2, box(20,20)),
            send(M2, fill_pattern, colour(white)),
            send(Finestra,display,M2,point(0,60)),
    new(M3, box(20,20)),              % disegna divisorio giallo-bianco
            send(M3, fill_pattern, colour(black)),
            send(Finestra,display,M3,point(200,20)),
    new(M4, box(20,20)),
            send(M4, fill_pattern, colour(black)),
            send(Finestra,display,M4,point(200,80)),
    new(M5, box(20,20)),               % disegna divisorio verde-bianco
            send(M5, fill_pattern, colour(black)),
            send(Finestra,display,M5,point(200,120)),
    new(M6, box(20,20)),
            send(M6, fill_pattern, colour(black)),
            send(Finestra,display,M6,point(200,200)),
    new(M7, box(20,20)),              % disegna divisorio grigio-bianco
            send(M7, fill_pattern, colour(black)),
            send(Finestra,display,M7,point(200,240)),
    new(M8, box(20,20)),
            send(M8, fill_pattern, colour(black)),
            send(Finestra,display,M8,point(200,360)).

