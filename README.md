# Game5000

# The 5000 Game 🎲

This project is an online version of the dice game 5000, played with 6 dice.
The objective is to reach 5000 points by combining different dice compositions and following the game’s rules.

# Project Overview 😁

The purpose of this project was to practice and explore:

Building and managing a graphical user interface (GUI).

Implementing real-time interactions between players.

Setting up and managing a server to synchronize game states.

Learning the fundamentals of deploying an online multiplayer game.

# Gameplay & Rules

The game is played with 6 dice.
Players take turns rolling the dice and accumulate points based on valid scoring combinations.

The first player to reach 5000 points wins.

Scoring
Single 1 → 100 points
Single 5 → 50 points
Three of a kind (x) → x × 100 points (Exception: Three 1’s = 700 points)
Three distinct pairs → 1000 points
Straight (1–2–3–4–5–6) → 1500 points

Points must be validated before being kept. Validation is done by setting aside a scoring die (usually a 1 or a 5).

Special Cases
- Full Hand: when all 6 dice score, you may roll again.
- Obligation to Play: after scoring a Full Hand or a Three of a kind without extra points, you must roll again.
- Starting Threshold: you must score at least 750 points in a single turn before officially entering the game.

# Illustrations
![Game Screenshot](screenshots/screenshot1.png)

