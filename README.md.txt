# Tetris Game Project

## Project Overview
This project is a Tetris game implemented in Python using Pygame. The game includes multiple components:
- **Game Logic:** Handles shape creation, movement, collision detection, line clearing, scoring, and level progression.
- **Board Management:** Represents the Tetris board, draws the grid, places shapes, and checks for valid movements.
- **User Interface:** Displays score, level, lines, and menu buttons for starting or exiting the game.
- **Home/Menu Screen:** A welcoming screen with interactive buttons and icons.

---

## Project Structure
The project is organized into four main Python files:

1. **Game.py** – Contains the main game loop, game logic, and integration of all components.  
2. **Board.py** – Handles the board grid, drawing, placing shapes, and UI elements.  
3. **Shape.py** – Defines the Tetris shapes, movement, and shape generation logic.  
4. **Home.py** – Implements the main menu screen with buttons, title, and icons.

Additional resources:
- **font/** – Contains the game font file (`Audiowide-Regular.ttf`) used for text rendering.  
- **images/** – Contains the game icons used in the home/menu screen.  
- **Doxygen HTML** – Documentation generated using Doxygen (optional, if included in the repository).

---

## How to Run the Game
1. Make sure Python 3.x and Pygame are installed on your system.
2. Clone or download the repository.
3. Ensure all folders (`font/`, `images/`) and files (`Game.py`, `Board.py`, `Shape.py`, `Home.py`) are in the same directory.
4. Open a terminal in the project folder and run:

```bash
python Home.py
```

## Documentation
This project includes in-line comments and Doxygen documentation for better understanding of classes, methods, and functions.

- All functions, classes, and important variables have `@brief`, `@param`, and `@return` descriptions in the code.
- The Doxygen HTML output can be viewed in a browser for detailed documentation of the project.