# Pong Game

## Overview
This project implements a classic Pong game using Python and Pygame. It allows two players to control paddles and compete to score points by bouncing a ball back and forth.

## Project Structure
```
pong-game/
├── pong/
│   ├── __init__.py      # Required to have a package
│   └── main.py          # Entry point of the game
├── env/                 # Virtual environment directory
├── pyproject.toml       # Project configuration and dependencies
└── README.md            # Project documentation
```

## Setup Instructions
0. **Make sure poetry is installed**
   ```bash
   pip install poetry
   ```
If you get a path warning add the python scripts path to your computer path envirnment variables.

1. **Clone the Repository**
   ```bash
   git clone https://github.com/poivronjaune/vibecoding-pong.git
   cd pong-game
   ```

2. **Create a Virtual Environment**
   To create a virtual environment named `env`, run:
   ```bash
   poetry install
   ```


## Running the Game
To run the Pong game, execute the following command:
```bash
poetry run python -m pong.main
```

## Controls
- Player 1: 
  - Move Up: W
  - Move Down: S
- Player 2:
  - Move Up: UP ARROW
  - Move Down: DOWN ARROW

## Game Objective
The objective of the game is to score points by getting the ball past the opponent's paddle. The first player to reach the winning score (default: 5 points) wins the game.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.