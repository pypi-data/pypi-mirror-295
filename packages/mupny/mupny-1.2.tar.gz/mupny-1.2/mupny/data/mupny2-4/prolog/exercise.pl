parent(rich,ned).
parent(rich,brandon).
parent(rich,lyanna).
parent(ned,arya).
parent(ned,sansa).

ancestor(X,Y):-
    parent(X,Y).
ancestor(X,Y):-
	parent(X,Z),
	ancestor(Z,Y).

grandparent(Nonn, Nipote):-
	parent(Nonn, Genitore),
	parent(Genitore, Nipote).

location(desk,office).
location(computer,office).
location(flashlight,desk).
location(envelope,desk).
location(stamp,envelope).
location(key,envelope).

is_contained_in(X,Y):-
    location(X,Y).
is_contained_in(X,Y):-
    location(X,Z),
    is_contained_in(Z,Y).

fact(0,1).
fact(N,X):-
    N1 is N-1,
	fact(N1,X1),
    X is X1 * N.

even(0).
even(N):-
    N1 is N - 2,
    N1 >= 0,
    even(N1).

odd(1).
odd(N):-
    N1 is N - 2,
    N1 >= 1,
    odd(N1).

divide(N,Ans):- Ans is N / 2.


power(_,0,1).
power(X,1,X).
power(X,Y,Ans):-
	Y1 is Y - 1,
    power(X,Y1,Z1),
    Ans is Z1 * X.

% MEMBER OF A LIST
% ?- member(2, [1,2,3,4]).

member(N, [N|_]).
member(N, [_|T]):-
    member(N, T).

% APPEND A LIST INTO ANOTHER LIST
%?- append ([1,2],[3,4],X)
append([],L,L).
append([H|T],L2,[H|T2]):-
    append(T,L2,T2).

% ADD AN ELEMENT TO A LIST
%As the first element
% ?- add_first([1,2,3],0,L).
add_first(L,X,[X|L]).
% add_end()
add_end([],X,[X]).
add_end([H|T],X,[H|T2]):-
    add_end(T,X,T2).

% REMOVE AN ELEMENT FROM LIST
% ?- remove(1,[1,2,3],X)
removeMio(H, [H|T], T).
removeMio(X, [H|T], L2):-
    L2 = [H|T2],
    removeMio(X, T, T2).
remove(H, [H|T], T):-!.
remove(X, [H|T], [H|T2]):-
    remove(X, T, T2).

% REMOVE ALL OCCURENCE OF AN ELEMENT FROM THE LIST
% ?- remove_all(2, [1,2,3,2],[1,3])
remove_all(_, [], []).
remove_all(E, [E|T], L):-
    !,
    remove_all(E, T, L).
remove_all(E, [HS|TS], [HS|TD]):-
    remove_all(E, TS, TD).


% RETURN THE SUCCESSORS OF THE SPECIFIED ELEMENT
% ?- successors(1,[1,2,3],2)
succ(E,[E|T],HT):-
    [HT|_] = T.
succ(E, [_|T],T2):-
    succ(E, T, T2).

% SPLIT A LIST
% ?- divide(List,Element, L1, L2)
divide(E,[E|T],[E],T).
divide(E,[H|T],[H|T1],T2):-
    divide(E,T,T1,T2).

% SUM ELEMENT OF LIST
% ?- sum(L,Sum)
% sum([H|[]],H).
sum([],0).
sum([H|T], SUM):-
    sum(T, S),
    SUM is H + S.

% COUNT THE ELEMENT OF THE LIST
% ?-
count([],0).
count([_|T],COUNT):-count(T,C), COUNT is C + 1.

% ALL EQUAL: CHECK IF ALL ELEMENT OF LIST ARE EQUAL
% in questa modalità confrontiamo il primo elemento con il secondo, il secondo con il terzo, ecc...
all_equals( [ _ | [] ] ).
all_equals( [ H | [H|[]] ] ).
all_equals( [ H | [H|T] ] ):-
    all_equals([H|T]), !.
% in questa modalità confrontiamo il primo elemento con tutti i successivi.
all_equals_slide([H|T]):-
    equals(H,T).
equals(_,[]).
equals(E,[E|T]):-
    equals(E,T).

% ALL DIFFERENT
all_different([]).
all_different([H|T]):-
    different(H,T),
    all_different(T).
different0(_, []):-!.
different(E, [H|T]):-
    E =\= H, %not(E=H)
    different(E,T).

% print elements in list
printAll([]).
printAll([H|T]):-
    write(H),
    nl, %newline
    printAll(T).


% is_a_pokemon
pokemon(bulbasaur).
is_a_pokemon:-
    write("Write the name of the pokemon"),
    read(Pokemon),
    pokemon(Pokemon),
    write("Yes,"),
    tab(5),
    write(Pokemon),
    write(" is a pokemon").

% find_all
foo(a,b,c).
foo(a,b,d).
foo(a,b,e).
% ?- findall(C, foo(A,B,C), Cs)
% @return Cs = [c,d,e]

% ?- bagof(C, foo(A,B,C), Cs)  -- setof == bagof senza ripetizioni
% @return
% A = a,
% B = b,
% Cs = [c, d, e]


% IMPLEMETATION TEST AI 30-01-2024
sum2([], 0).
sum2([H|T], S):-
    sum2(T, S1),
    S is H + S1.

tuple2list((K,V), [K|[V]]).


% DATA UNA THRESHOLD, VERIFICARE CHE NELLA LISTA SIA PRESENTE
% ALMENO UN VALORE INFERIORE A QUELLA SOGLIA
check_threshold(M, [H|_]):-
    H < M, !.
check_threshold(M, [H|T]):-
    H >= M,
    check_threshold(M, T).

% ESTRARRE DA UNA LISTA DI TUPLE UNA LISTA DI SOLO VALORI
% ?- tuple2val([(K1,V1),(K2,V2)],[V1,V2])
% ?- tupla2val( [(1,2), (2,3), (5,6)], ListOfValues ).
% ?- findall(V, tupla(K,V), ListOfValues).
tupla(1,2).
tupla(3,4).
tupla2val([], []).
tupla2val([H|T], L):-
    (_,V) = H,
    write("append: "),
    tab(1),
    write(V),
    write(" to the list."),
    nl,
    tupla2val(T, L1),
    L = [V | L1].


