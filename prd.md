# Product Requirements Document (PRD)

***Project Name***: Simple Pong Game in Python  
***Version***: 1.0  
***Author***: Robert Boivin (with ChatGPT assistance)  
***Date***: 2025-08-15  

## 1. Purpose

The purpose of this project is to create a classic Pong game implemented in Python.  
The game will allow two players to control paddles and bounce a ball back and forth. The first player to reach the winning score is declared the winner.

## 2. Scope

The game will run locally on a computer.  
Implemented using Pygame for rendering, input handling, and game loop.  
Support two-player mode only (no AI opponent in version 1.0).  
Focus on simple, responsive gameplay and clear visuals.  

## 3. Features & Requirements  

### 3.1 Core Gameplay
- ***Ball Movement***: The ball moves automatically at a set speed, bouncing off walls and paddles.
- ***Paddle Movement***:  
-- Player 1 controls: W (up), S (down)
-- Player 2 controls: UP ARROW (up), DOWN ARROW (down)

- ***Scoring***:  
A player scores when the opponent misses the ball.
Display the score at the top center of the screen.

- ***Winning Condition***:  
-- First player to reach a configurable winning score (default: 5 points) wins.  
-- Display "Player X Wins!" message and stop gameplay.

### 3.2 Visual Design  
- ***Screen Dimensions***: 800x600 pixels.
- ***Background***: Black.
- ***Paddles***: White rectangles (width: 10px, height: 100px).
- ***Ball***: White square (10x10 pixels).
- ***Score Text***: White, large font, centered at the top.

### 3.3 Controls
| Player | Move Up | Move Down |
|--------|---------|-----------|
| P1     | W       | S         |
| P2     | ↑       | ↓         |

### 3.4 Game States
***Start Screen***: Shows "Press SPACE to Start", show controls, player 1 name entry, player two name entry.  
***In-Game***:Ball and paddles are active; score is updated.  
***Game Over***: Shows winner message and "Press R to Restart", saves both player names and their score, if player name exists, update only the score.  

## 4. Technical Requirements
***Language***: Python 3.8+  
***Library***: Pygame (latest stable version)  
***Graphics***: Programmatically drawn 2D shapes using Pygame’s built-in drawing functions (pygame.draw.rect, pygame.draw.line, etc.); no external image files or sprites.  
***Visual Style***: Minimalist, retro Pong-style, solid-color paddles, ball, and background.  
***Frame Rate***: 30 FPS  
***Code Structure***:  
-- main.py — game entry point  
-- Functions for initialization, game loop, rendering, collision detection, and input handling  
-- Constants for colors, dimensions, and speeds 

## 5. Non-Functional Requirements
***Performance***: Must run at 30 FPS without stuttering.  
***Simplicity***: Easy for beginners to read and modify the code.  
***Cross-Platform***: Runs on Windows, macOS, Linux (given Python + Pygame installed).  

## 6. Out of Scope (v1.0)  
- AI-controlled paddles  
- Sound effects or background music  
- Power-ups or special ball mechanics  
- Online multiplayer  

## 7. Success Criteria  
- The game starts from a start screen.  
- Both players can control their paddles smoothly independently from each other.  
- Ball bounces correctly off walls and paddles.  
- Scoring updates correctly.  
- Winner is displayed when score limit is reached.  
- Restarting works without crashing.  

