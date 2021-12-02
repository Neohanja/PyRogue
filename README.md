# PyRogue
File: Python Rogue

Author: George Hall

Final Project : CS 120

# File List:
Main.py (Main) - Contains the Main Method to run the program

Game_Manager.py - Contains the game loop and all necissary data for controlling game elements

AIManager.py - Controls all AI operations, such as town/dungeon populations, player actions and actor interaction

Actor.py - Abstract; Base class for all entities (NPC/Player/Monster)
- Player.py - Player Class
- Monster.py - Describes all the monsters of the world, Includes subclass Boss for boss entities
- NPC.py - Builds and interacts all NPCs (town folk) for the player. Simple demo, no full AI.

Stats.py - Character Statistic operations for the actors, to include xp, level, gold, and potions (no inventory system yet)

FSM.py - Finite State Machine for Monster AI. Determines if the monster is idling, wandering or chasing/attacking the player.

State.py - Works with FSM, determines the actions, conditions of transitioning, and entering different states (ie: wandering)

Screens.py - Creates borders and UI elements, includes character input for names and seeds

Map.py - Builds and draws the map to the screen

MathFun.py - Math Functions needed to make the game and world work properly

AStar.py - Pathfinding, used for AI movement and ensuring terrain features are reachable by the player

ColorPallet.py - Color information for the different aspects of the world, built into an easy to use library

Messenger.py - Messenger system for displaying the player information, such as damage done or environmental interaction

SaveGame.py - Save and Load operations for file manipulation, parses lines through to determine if something is an AI or Map Data

## Noise and Map Building functions for world Building
DungeonGen.py - For placing dungeons in the overworld and generating each dungeon.

TownGen.py - For placing towns in the overworld and generating each town.

Noise.py - Distorted Gradient noise based loosely on Ken Perlin's Improved Noise Function of 2002

NameGen.py - Generates Town, Dungeon and Villager/Boss names

# Files made using tutorials from rogueliketutorials.com, meant for input processing:
Input_Handlers.py - Handles key input and what action should be attached to specific keys

Action.py - The action subclass that tells the system what to do based on keys pressed

# Other Python code from Class
Loadpng.py - Problem Set 10, Image Manipulation (For title screen)

png.py - Problem Set 10, MIT *.png Loading

# Additional Files:
terminal12x12_gs_ro.png (font file; tcod github repository; https://github.com/libtcod/python-tcod/tree/master/fonts/libtcod)

Title.png - Picture taken at Forest Park, Springfield, MA. Downscaled for screen size