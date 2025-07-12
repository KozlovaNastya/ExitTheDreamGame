# Exit the Dream

**Exit the Dream** is a 2D platformer built with Python using the PyQt library. The main idea of the game is to complete five levels of increasing difficulty by controlling gravity and dodging obstacles. The player's goal is to escape from a dream by overcoming all challenges without losing all lives.

The game was developed by a team of two using Git for version control and a GitHub repository. The main code was maintained in a stable branch, with two additional branches used to develop separate game modules in parallel.

## Project Structure

```
ExitTheDream/
├── Game/
│   ├── assets/
│   │   ├── background/
│   │   └── buttons/
│   ├── gam/
│   │   ├── levels/
│   │   ├── constants.py
│   │   └── main_menu.py
│   ├── start.py
│   └── main.py
```

## How to Run the Game

1. Navigate to the `Game/` directory and start the game:

```
python start.py
```

## Controls

- Default:
  - Movement: ← ↑ → ↓
  - Jump: Space
  - Change gravity:
    - 1 — down
    - 2 — up
    - 3 — left
    - 4 — right

- Controls can be changed in the settings menu.

## Levels

The game has 5 levels:

1. Level 1 — movement, jump, basic obstacles
2. Level 2 — adds up/down gravity shift, spikes
3. Level 3 — full gravity control in all directions
4. Level 4 — moving platforms
5. Level 5 — all mechanics + disappearing platforms

The player has 3 lives for the entire game. After losing them all, the game restarts.

## Leaderboard

- Stores up to 10 best results
- Top 3 are highlighted (gold/silver/bronze)
- Stored in `.json` format
- Supports entering player name and saving progress

## Interface

- Main menu: Start, Continue, Settings, Leaderboard, Exit
- Win / Game Over dialogs
- Settings: Controls, Graphics, Sound
- Leaderboard screen

## Technologies

- Language: Python
- GUI: PyQt
- Data format: JSON
- Version control: Git & GitHub

## Team Development

- Work managed through GitHub
- Branches:
  - main — stable code
  - nastya — levels
  - alina — interface

## Summary

- Fully developed 2D game with gravity mechanic
- Customizable interface and controls
- Progress saving and leaderboard
- Team collaboration with Git, structured project architecture
