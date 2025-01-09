# Battle Boxes

A very simple arena roguelike using Python and Pygame. This game features procedurally generated enemies, player upgrades, and an increasing difficulty system. Survive as long as you can while upgrading your stats and defeating enemies.

This was an experiment to see if I could build a game in Python (with LLM support). I found it surprisingly fun to play while testing/debugging it. There are random stat multipliers, which you are more likely to receive as your luck stat increases, so the main strategy is to be greedy and always take luck.

## Features

- **Procedurally Generated Enemies**: Enemies spawn each round with increasing difficulty based on size, speed, health, count, and luck.
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
