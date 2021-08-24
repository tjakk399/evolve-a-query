#!/usr/bin/env swipl

:- set_prolog_flag(verbose, silent).
:- initialization(main, main).

main :-
  current_prolog_flag(argv, _),
  run,
  halt(0).
main :-
  halt(1).

% Let it fail until all outputs are generated, then hit true.
run :- phrase(s,L), atomic_list_concat(L,' ',S), write(S), nl, fail.
run :- true.

s --> a, a, n, v, adv.

art --> ["the"].
art --> ["a"].

v --> ["sleep"].
v --> ["return"].
v --> ["survive"].
v --> ["think"].
v --> ["crash"].

adv --> ["furiously"].
adv --> ["reluctantly"].
adv --> ["brutally"].
adv --> ["comfortably"].
adv --> ["comfortably"].

a --> ["colorless"].
a --> ["green"].
a --> ["red"].
a --> ["blue"].
a --> ["tasty"].
a --> ["convincing"].
a --> ["large"].

n --> ["dogs"].
n --> ["cats"].
n --> ["ideas"].
n --> ["cars"].
n --> ["societies"].
