# Space Scavenger Game

Space Scavenger is an exciting arcade-style game where players control a spaceship to collect energy crystals while avoiding dangerous asteroids. The game features progressively increasing difficulty and an engaging score system.

## Game Features

### Core Mechanics
- Dynamic spaceship controls
- Randomly spawning asteroids and energy crystals
- Progressive difficulty system
- Score tracking
- Background music and sound effects
- Game over state with restart option

### Progressive Difficulty
- Asteroids gradually increase in speed as the game progresses
- More frequent obstacle spawns over time
- Requires increasing player skill to survive longer

### Scoring System
- Each collected crystal awards 10 points
- Score is displayed in real-time at the top of the screen
- No maximum score limit

## How to Play

### Controls
- **Left Arrow Key**: Move spaceship left
- **Right Arrow Key**: Move spaceship right
- **R Key**: Restart game after game over / won
- **Close Window**: Exit game

### Gameplay Objectives
**Winning Condition**: Achieve a score of 30 and survive for 30 seconds 
- Collect as many energy crystals as possible
- Avoid colliding with asteroids
- Try to achieve the highest score possible

### Game Flow
1. Game starts with a displayed instruction screen.
2. Press any key to start the game
3. Player navigates the spaceship to collect crystals while avoiding asteroids.
4. Game continues until player has scored 30 points and has played continuously for 30 seconds **or** collides with an asteroid
5. Final score and restart prompt are displayed.
6. Player can restart or exit the game

## Setup and Installation

### Requirements
- Python 3.x
- Pygame library

### Required Files
- main.py (main game script)
- assets:
    - spaceship.png (player sprite)
    - asteroid.png (obstacle sprite)
    - energy_crystal.png (collectible sprite)
    - clash_sound.wav (collision sound effect)
    - background_music.wav (game background music)

### Installation Steps
1. Make sure Python is installed on your system
2. Install Pygame by running: `pip install pygame`
3. Place all game assets in the `asstes` directory
4. Run the game using: `python main.py`