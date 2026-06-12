# 2026-FIFA-World-Cup-Simulator

- Predict all 104 matches, simulate the entire tournament, or choose a hybrid mode to have both options throughout the World Cup.

- The simulator accurately follows the official FIFA World Cup format, including group standings, 3rd place qualification, knockout bracket generation, and realistic match simulations.

## Features

- Full 48 team 2026 FIFA World Cup format
- All groups, dates, locations, and match numbers correctly scheduled
- Accurate group stage standings and tiebreaker calculations
- Automatic qualification of the 8 best third-place teams
- Correct round of 32 bracket generation based on third-place combinations
- Complete knockout stage bracket
- Realistic match simulations using current FIFA rankings and World Cup odds
- Realistic scorelines based on historical World Cup scoring data
- Realistic penalty shootout outcomes using FIFA conversion rates
- Match results displayed after each round
- Final Top 3 podium display (Champion, Runner-up, Third Place)

## Set Up & Running the Program
- Select Code and then download ZIP
- On VS Code, open downloaded folder
- Open VS Code terminal and enter:
- cd tournament-engine-main
- python3 main.py

## Game Modes

### 1. Manual Tournament
- Predict the scores of all 104 matches.

### 2. Simulate Entire Tournament
- Automatically simulates the entire World Cup.

### 3. Hybrid Mode
Before each match, choose whether to:
- Predict the score manually
- Simulate the current match
- Simulate the remaining matches of the current round

## Knockout Match Predictions

When predicting knockout round matches, you can choose how the match is decided.
1. Full Time
2. After Extra Time
3. Penalties

For Full Time & After Extra Time:
- The user entered score cannot end in a draw

For Penalties:
- The user will enter two separate scores
1. The 1st score will be the regular match result (result must end in a draw)
2. The 2nd score will be the penalty shootout result (result cannot end in a draw)
