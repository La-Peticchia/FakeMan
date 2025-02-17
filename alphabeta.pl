

% alfabeta(+Pos,+Alfa,+Beta,+Depth,-MigliorPosSucc,-Val)
% ===================== Minimax con potatura alfa-beta
alfabeta(Pos,Alfa,Beta,Depth,MigliorPosSucc,Val) :-% Pos ha MigliorPosSucc se
  Depth > 0,
  NewDepth is Depth -1,
  bagof(PosSucc, mossa(Pos, PosSucc), ListaPosSucc),         % ha mosse
  !,                                                  % e la migliore è
  migliore(ListaPosSucc,Alfa,Beta,NewDepth,MigliorPosSucc,Val)  % MigliorPosSucc
  ;                                                        % altrimenti
  payoff(Pos,Val).  % Pos è terminale e restituisce l'utilità come Val

% migliore(+Lista,+Alfa,+Beta,+Depth,-MigliorPosSucc,-Val)
% =================== restituisce MigliorPosSucc da una Lista di
% possibili successori ed il suo Val rimanendo sempre dentro i limiti
% Alfa e Beta
migliore([Pos|AltrePos],Alfa,Beta,Depth,MigliorPosSucc,MigliorVal) :-
  alfabeta(Pos,Alfa,Beta,Depth, _,Val),       % determina Val associato a Pos
  pota(AltrePos,Alfa,Beta,Depth,Pos,Val,MigliorPosSucc,MigliorVal).

% miglioreDi(+Pos0, +Val0, +Pos1, +Val1, -Pos, -Val) ==================
% restituisce la migliore coppia Pos Val fra le due considerate
miglioreDi(Pos,Val,_,Val1,Pos,Val) :-           % Pos0 è meglio di Pos1
    tocca_a_MIN(Pos),                   % se in Pos0 deve muovere MIN e
    Val > Val1, !                      % MAX sceglie il valore maggiore
    ;                                                          % oppure
    tocca_a_MAX(Pos),                      % se in Pos0 deve muovere  e
    Val < Val1, !.                       % MIN sceglie il valore minore
miglioreDi(_,_,Pos,Val,Pos,Val).     % altrimenti Pos1 è meglio di Pos0

% potato(+Lista,+Alfa,+Beta,Pos,Val,PosGiaBuona,ValGiaBuono) ==========
pota([],_,_,_,Pos,Val,Pos,Val) :- !.        % non ci sono altre posizioni
pota(_,Alfa,Beta,_,Pos,Val,Pos,Val) :-
  tocca_a_MIN(Pos), Val > Beta, !                           % beta test
  ;
  tocca_a_MAX(Pos), Val < Alfa, !.                          % alfa test
pota(ListaPos,Alfa,Beta,Depth,Pos,Val,PosGiaBuona,ValGiaBuono)  :-
  aggiornaAlfaBeta(Alfa,Beta,Pos,Val,NAlfa,NBeta),     % stringe limiti
  migliore(ListaPos,NAlfa,NBeta,Depth,Pos1,Val1),
  miglioreDi(Pos,Val,Pos1,Val1,PosGiaBuona,ValGiaBuono).

% aggiornaAlfaBeta(Alfa,Beta,Pos,Val,NAlfa,NBeta) =====================
aggiornaAlfaBeta(Alfa,Beta,Pos,Val,Val,Beta)  :-
  tocca_a_MIN(Pos),                                         % gioca MIN
  Val > Alfa, !.                                         % aumenta Alfa
aggiornaAlfaBeta(Alfa,Beta,Pos,Val,Alfa,Val)  :-
  tocca_a_MAX(Pos),                                         % gioca MAX
  Val < Beta, !.                                      % diminuisce Beta
aggiornaAlfaBeta(Alfa,Beta,_,_,Alfa,Beta).       % nessun aggiornamento

