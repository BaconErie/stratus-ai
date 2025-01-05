# Features that the AI is trained on

Each data point is one minute from one of the data sets.

- Mean mouse x pos
- Mean mouse y pos
- Stdev of mouse x pos
- Stdev of mouse y pos
- Percentage of time held for
  - Left mouse
  - Middle mouse
  - Right mouse
- Number of mouseups per minute for
  - Left mouse
  - Middle mouse
  - Right mouse
- How many keys make up 25% of all the time keys were held
  - Justification: Active work is more uniform, so more keys make up 25%
  - If 100% uniform, 25% of the top most held keys would make up 25% of all keys
    that detected input
  - How many keys make up 25% of all the key up counts
  - Justification: Active work is more uniform, so more keys make up 25%
- How many keys make up 25% of all the key up counts ONLY LETTERS

  - Justification: Active work is more uniform, so more keys make up 25%
  - Only letters because if we look on the active work graph, only letters is
    pretty uniform, unlike games

- Movement keys to Non-movement keys hold time ratio
  - Justification: A measure of how much WASD, space, shift, and arrow keys are
    held compared to other keys. These keys are most used in games for movement,
    and so these keys are likely most held compared to other keys. This does not
    work for text based games or games that don't use a mouse.

# Might work?? But from the preliminary examination won't work

- Average percentage of time a key was held
- Key up counts per minute

# Problems:

- We have a lot of FPS games, or movement games. Not a lot of minesweeper, text
  based games, etc.

- A lot of games compared to work.

clean key up counts, use new cleaned one

also use cleaned key time held sum in the alnum keys
