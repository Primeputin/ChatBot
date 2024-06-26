:- dynamic grandparent/2.
:- dynamic not_grandparent/2.

:- dynamic grandfather/2.
:- dynamic not_grandfather/2.

:- dynamic grandmother/2.
:- dynamic not_grandmother/2.

:- dynamic genderless_side_relative/2.
:- dynamic not_genderless_side_relative/2.

:- dynamic uncle/2.
:- dynamic not_uncle/2.

:- dynamic aunt/2.
:- dynamic not_aunt/2.

:- dynamic son/2.
:- dynamic not_son/2.

:- dynamic daughter/2.
:- dynamic not_daughter/2.

:- dynamic father/2.
:- dynamic not_father/2.

:- dynamic mother/2.
:- dynamic not_mother/2.

:- dynamic brother/2.
:- dynamic not_brother/2.

:- dynamic sister/2.
:- dynamic not_sister/2.

:- dynamic parent/2.
:- dynamic not_parent/2.

:- dynamic sibling/2.
:- dynamic not_sibling/2.

:- dynamic siblings/2.
:- dynamic not_siblings/2.

:- dynamic relatives/2.
:- dynamic not_relatives/2.

:- dynamic child/2.
:- dynamic not_child/2.

:- dynamic male/1.
:- dynamic not_male/1.

:- dynamic married/2.
:- dynamic not_married/2.

:- dynamic two_parents/1.
:- dynamic one_father/1.
:- dynamic one_mother/1.
:- dynamic four_grandparents/1.
:- dynamic two_grandfather/1.
:- dynamic two_grandmother/1.

:- dynamic descendant/2.

two_parents(Person) :-
    findall(Parent, parent(Parent, Person), Parents),
    length(Parents, NumParents),
    NumParents = 2.
one_father(Person) :-
    findall(Father, father(Father, Person), Fathers),
    length(Fathers, NumFather),
    NumFather = 1.
one_mother(Person) :-
    findall(Mother, mother(Mother, Person), Mothers),
    length(Mothers, NumMother),
    NumMother = 1.

four_grandparents(Person) :-
    findall(GrandParent, grandparent(GrandParent, Person), GrandParents),
    length(GrandParents, NumGrandParents),
    NumGrandParents = 4.
two_grandfather(Person) :-
    findall(GrandFather, grandfather(GrandFather, Person), GrandFathers),
    length(GrandFathers, NumGrandFather),
    NumGrandFather = 2.
two_grandmother(Person) :-
    findall(GrandMother, grandmother(GrandMother, Person), GrandMothers),
    length(GrandMothers, NumGrandMother),
    NumGrandMother = 2.

not_child(X, Y) :- X = Y.
not_child(X, Y) :- relatives(X, Y), \+ child(X, Y), \+ (siblings(X, Z), child(Z, Y)). % \+ (siblings(X, Z), child(Z, Y)). this is included to not make it possible for him/her to have the same parent as his sibling
not_child(X, Y) :- two_parents(X), \+ child(X, Y).

% This cannot be done normally because it would cause an infinite loop with itself like child(X, Y) :- without the assertz part
% Make a person a parent of a child who has a sibling
% make_missing_children_parents(Child, Parent) :-
%     child(Child, Parent),
%     siblings(Child, Sibling),
%     \+ child(Sibling, Parent),
%     assertz(child(Sibling, Parent)).

% parent is only reliant on child since child will always be asserted not parent
parent(X, Y) :- child(Y,X).
not_parent(X, Y) :- relatives(X, Y), \+ parent(X, Y).
not_parent(X, Y) :- X = Y.
not_parent(X, Y) :- two_parents(Y), \+ parent(X, Y). % there could only be a max of two parents

% no need to check not father and mother wherein person1 = person2
not_father(X, Y) :- not_parent(X, Y).
not_father(X, _) :- not_male(X).
not_father(X, Y) :- one_father(Y), \+ father(X, Y). % max of one father
not_mother(X, Y) :- not_parent(X, Y).
not_mother(X, _) :- male(X).
not_mother(X, Y) :- one_mother(Y), \+ mother(X, Y). % max of one mother

son(X, Y) :- child(X, Y), male(X).
not_son(X, _) :- not_male(X).
not_son(X, Y) :- not_child(X, Y).
daughter(X, Y) :- child(X, Y), not_male(X).
not_daughter(X, _) :- male(X).
not_daughter(X, Y) :- not_child(X, Y).

siblings(Person1, Person2) :- sibling(Person1, Person2).
siblings(Person1, Person2) :- sibling(Person2, Person1).
siblings(Person1, Person2) :- parent(X, Person1), parent(X, Person2), Person1 \= Person2.
not_sibling(Person1, Person2) :- Person1 = Person2.
not_sibling(Person1, Person2) :- parent(Person1, Person2).
not_sibling(Person1, Person2) :- child(Person1, Person2).
not_sibling(Person1, Person2) :- grandparent(Person1, Person2); grandparent(Person2, Person1).
not_sibling(Person1, Person2) :- genderless_side_relative(Person1, Person2); genderless_side_relative(Person2, Person1).
not_sibling(Person1, Person2) :- sibling(Person1, Person), married(Person, Person2).
% I can't do this because I'm using sibling not siblings for asserting:
% not_sibling(Person1, Person2) :- relatives(Person1, Person), \+ sibling(Person, Person2).
% so type the rules itself


not_siblings(Person1, Person2) :- not_sibling(Person1, Person2).
not_siblings(Person1, Person2) :- not_sibling(Person2, Person1).
not_brother(Person1, Person2) :- not_siblings(Person1, Person2).
not_brother(Person1, _) :- not_male(Person1).
not_sister(Person1, Person2) :- not_siblings(Person1, Person2).
not_sister(Person1, _) :- male(Person1).


father(Person1, Person2) :-
    male(Person1),          % Check if Person1 is a male
    Person1 \= Person2,     % Check if Person1 and Person2 are not the same
    parent(Person1, Person2).  
mother(Person1, Person2) :-
    not_male(Person1),          % Check if Person1 is a female
    Person1 \= Person2,     % Check if Person1 and Person2 are not the same
    parent(Person1, Person2).  
brother(Person1, Person2) :-
    male(Person1),          % Check if Person1 is a male
    Person1 \= Person2,     % Check if Person1 and Person2 are not the same
    siblings(Person1, Person2). % Check if they are siblings 
sister(Person1, Person2) :-
    not_male(Person1),          % Check if Person1 is a female
    Person1 \= Person2,     % Check if Person1 and Person2 are not the same
    siblings(Person1, Person2). % Check if they are siblings  

grandparent(Person1, Person2) :- parent(Person1, Person), parent(Person, Person2), Person1 \= Person2.
not_grandparent(Person1, Person2) :- relatives(Person1, Person2), \+ grandparent(Person1, Person2).
not_grandparent(Person1, Person2) :- Person1 = Person2.
not_grandparent(Person1, Person2) :- four_grandparents(Person2), \+ grandparent(Person1, Person2). % there could only be a max of two grand parents


% no need to check not grandfather and grandmother wherein person1 = person2
grandfather(Person1, Person2) :- 
    male(Person1),
    Person1 \= Person2,
    grandparent(Person1, Person2).
not_grandfather(Person1, _) :- not_male(Person1).
not_grandfather(Person1, Person2) :- not_grandparent(Person1, Person2).
not_grandfather(Person1, Person2) :- two_grandfather(Person2), \+ grandfather(Person1, Person2).
grandmother(Person1, Person2) :- 
    not_male(Person1),
    Person1 \= Person2,
    grandparent(Person1, Person2).
not_grandmother(Person1, _) :- male(Person1).
not_grandmother(Person1, Person2) :- not_grandparent(Person1, Person2).
not_grandmother(Person1, Person2) :- two_grandmother(Person2), \+ grandmother(Person1, Person2).
 
genderless_side_relative(Person1, Person2) :- siblings(Person1, Person), parent(Person, Person2), Person1 \= Person2.
genderless_side_relative(Person1, Person2) :- siblings(Person1, Person), parent(Person, Child), siblings(Child, Person2), Person1 \= Person2.
genderless_side_relative(Person1, Person2) :- married(Person1, Spouse), siblings(Spouse, Sibling), parent(Sibling, Person2), Person1 \= Person2.
not_genderless_side_relative(Person1, Person2) :- relatives(Person1, Person2), \+ genderless_side_relative(Person1, Person2).
not_genderless_side_relative(Person1, Person2) :- Person1 = Person2.

 % for some reason, can't use brother/2
uncle(Person1, Person2) :- male(Person1), genderless_side_relative(Person1, Person2).
not_uncle(Person1, _) :- not_male(Person1).
not_uncle(Person1, Person2) :- not_genderless_side_relative(Person1, Person2).

% for some reason, can't use sister/2
aunt(Person1, Person2) :- not_male(Person1), genderless_side_relative(Person1, Person2).
not_aunt(Person1, _) :- male(Person1).
not_aunt(Person1, Person2) :- not_genderless_side_relative(Person1, Person2).

married(Person1, Person2) :- parent(Person1, Person), parent(Person2, Person),  Person1 \= Person2.
not_married(Person1, _) :- \+ married(Person1, _).

% Define a rule to check if X is a descendant of Y
descendant(X, Y) :-
    parent(Y, X). % X is a direct child of Y

descendant(X, Y) :-
    parent(Z, X), % X has a parent Z
    descendant(Z, Y). % Z is a descendant of Y

relatives(Person1, Person2) :- siblings(Person1, Person2).
relatives(Person1, Person2) :- grandparent(Person1, Person2); grandparent(Person2, Person1).
relatives(Person1, Person2) :- genderless_side_relative(Person1, Person2); genderless_side_relative(Person2, Person1).
relatives(Person1, Person2) :- parent(Person1, Person2).
relatives(Person1, Person2) :- child(Person1, Person2).
relatives(Person1, Person2) :- married(Person1, Person2).
relatives(Person1, Person2) :- siblings(Person1, Person), married(Person, Person2).
relatives(Person1, Person2) :- descendant(Person1, Person2); descendant(Person2, Person1).
relatives(Person1, Person2) :- genderless_side_relative(Person1, Person), descendant(Person, Person2). 
relatives(Person2, Person1) :- genderless_side_relative(Person1, Person), descendant(Person, Person2).
not_relatives(Person1, Person2) :- Person1 = Person2.