This is my attempt at writing a chess engine. Still very much in progress, though it is somewhat functional.

Current limitations:

- can't en passant
- can't castle
- can't promote pawns
- it thinks the goal of the game is to capture the enemy king

Other stuff to work on:

- move pruning
- better board evaluation (currently evaluates based on piece value and available space)
- integrate with some kind of api so it can be run on a chess site instead of just in a command line

Running

- main.py sets up a won position for the engine (as white) and you can fight against it winning
- type your move in full notation (e.g. Pe2e4)
