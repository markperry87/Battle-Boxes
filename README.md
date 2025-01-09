# Battle Boxes

A very simple arena roguelike using Python and Pygame. This game features procedurally generated enemies, player upgrades, and an increasing difficulty system. Survive as long as you can while upgrading your stats and defeating enemies.

This project started as an experiment to see if I could create a game in Python with the help of an LLM. It turned out to be surprisingly fun to play during testing and debugging. One of the core mechanics is random stat multipliers, which become more frequent as your luck stat increases. As a result, (I think) the best strategy is to prioritize luck upgrades and embrace a "greedy" playstyle.

## Features

- **Procedurally Generated Enemies**: Enemies spawn each round with a random increase to a stat (size, speed, health, count, and luck}.
- **Player Upgrades**: Upgrade your weapon size, weapon damage, movement speed, or luck at the end of each round.
- **Multiplier System**: Random chance-based multipliers boost the effectiveness of upgrades for both the player and enemies.

## Gameplay

- **Objective**: Survive and progress through as many rounds as possible by defeating all enemies in each round.
- **Upgrades**: After each round, choose one stat to upgrade. Multipliers may increase the impact of your choice.
- **Game Over**: The game ends when the player collides with an enemy.

## Controls

- **Arrow Keys**: Move the player character.
- **Space**: Activate the weapon.
- **R**: Restart the game (after game over).
