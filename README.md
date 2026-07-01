#  3D Dungeon Escape

A simple 3D dungeon adventure game built using **Python**, **PyOpenGL**, and **GLUT**. The player must explore a maze, collect keys, avoid enemies, gather useful items, and find the exit portal to progress through increasingly difficult levels.

This project was developed as part of our academic coursework to demonstrate concepts of **computer graphics**, **3D rendering**, **game mechanics**, collision detection, object animation, and interactive gameplay using OpenGL.

---

##  Game Overview

In **3D Dungeon Escape**, the player starts inside a maze and must:

* Collect all required keys
* Avoid or defeat enemies
* Pick up coins and treasures to increase score
* Use shields and health potions strategically
* Reach the exit portal to advance to the next level

The game contains **three levels**, each introducing more challenges and stronger enemy presence.

---

##  Features

###  Progressive Level System

* 3 playable levels
* Increasing number of keys required
* More enemies in higher levels
* Difficulty scaling through enemy distribution and speed

###  Enemy AI

* Randomized maze navigation
* Zone-based enemy movement in advanced levels
* Collision-based player damage
* Special freeze mechanic in Level 3

###  Collectibles

* Keys (required for level completion)
* Coins
* Treasure chests
* Health potions
* Protective shields
* Flashlights for visual effects

###  Multiple Camera Modes

* First-person view
* Third-person view
* Switch dynamically during gameplay

###  HUD System

* Health bar
* Current score
* Level information
* Timer
* Shield status
* Key collection progress

###  3D Graphics

* OpenGL-based rendering
* Animated player model
* Rotating collectibles
* Dynamic enemy animations
* Visual portal effects
* Maze environment with textured color themes per level

---

##  Technologies Used

* Python 3.x
* PyOpenGL
* GLUT (OpenGL Utility Toolkit)
* OpenGL
* GLU
* Math Library
* Random Library

---

##  Project Structure

```text
project_final.py
│
├── Game Initialization
├── Maze Generation & Management
├── Player Movement System
├── Enemy AI System
├── Collision Detection
├── Collectible Management
├── Camera Control
├── HUD Rendering
├── Level Progression
├── Animation System
└── OpenGL Rendering Loop
```

---

##  Game Mechanics

### Health System

* Player starts with 100 HP.
* Enemy collisions reduce health.
* Health potions restore HP.
* Game ends when health reaches zero.

### Shield System

* Shields provide temporary protection.
* A shield can destroy one enemy upon contact.
* The shield is consumed after use.

### Scoring System

Points are awarded for:

| Action                   | Points |
| ------------------------ | ------ |
| Collect Key              | +50    |
| Collect Coin             | +15    |
| Collect Treasure         | +100   |
| Collect Shield           | +50    |
| Defeat Enemy with Shield | +50    |

Additional bonuses:

* Remaining health bonus
* Time completion bonus
* Coin collection bonus

---

##  Controls

| Key                | Action                         |
| ------------------ | ------------------------------ |
| W                  | Move Forward                   |
| S                  | Move Backward                  |
| A                  | Move Left                      |
| D                  | Move Right                     |
| ←                  | Rotate Left                    |
| →                  | Rotate Right                   |
| V                  | Toggle Camera View             |
| R                  | Restart Game (after game over) |
| Right Mouse Button | Freeze Enemies (Level 3 only)  |

---

##  Levels

### Level 1

* 1 key required
* 5 free-roaming enemies
* Beginner difficulty

### Level 2

* 2 keys required
* 7 enemies
* Zone-based enemy placement

### Level 3

* 3 keys required
* 8 enemies
* Special freeze-cheat ability
* Highest difficulty

---

##  Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/3D-Dungeon-Escape.git
cd 3D-Dungeon-Escape
```

### 2. Install Dependencies

```bash
pip install PyOpenGL PyOpenGL_accelerate
```

### 3. Run the Game

```bash
python project_final.py
```

---

##  Screenshots

Add screenshots of:

* Main gameplay
* First-person mode
* Third-person mode
* Enemy encounters
* Victory screen

Example:

```markdown
![Gameplay](images/gameplay.png)
```

---

## 🎓 Learning Outcomes

This project helped us gain practical experience in:

* Computer Graphics
* OpenGL Programming
* 3D Object Rendering
* Animation Techniques
* Collision Detection
* Event Handling
* Game State Management
* Interactive User Interfaces

---

## 🔮 Future Improvements

* Sound effects and background music
* Better enemy pathfinding (A*)
* Procedural maze generation
* Additional enemy types
* Improved textures and lighting
* Multiplayer support
