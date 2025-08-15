# Pong Game

## Overview
This project implements a classic Pong game using Python and Pygame. It allows two players to control paddles and compete to score points by bouncing a ball back and forth.

## Project Structure
```
pong-game/
├── src/
│   └── main.py          # Entry point of the game
├── env/                 # Virtual environment directory
├── pyproject.toml       # Project configuration and dependencies
└── README.md            # Project documentation
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd pong-game
   ```

2. **Create a Virtual Environment**
   To create a virtual environment named `env`, run:
   ```bash
   python -m venv env
   ```

3. **Activate the Virtual Environment**
   - On Windows:
     ```bash
     env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source env/bin/activate
     ```

4. **Install Dependencies**
   Install the required dependencies using pip:
   ```bash
   pip install pygame
   ```

## Running the Game
To run the Pong game, execute the following command:
```bash
python src/main.py
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