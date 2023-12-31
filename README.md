# Overview

This project focuses on building an Artificial Intelligence Checker bot using various machine learning techniques. The primary methods employed include Simple Heuristics, Alpha-Beta Pruning, Monte-Carlo Tree Search, and suggestions for further improvement of the resulting AI.

## I. Development Process

To enhance the intelligence of our Final AI agent, we adopted the following strategies:

### 1. Simple Heuristic Strategy
We initially prioritized jumps and preventing the opponent from jumping. While effective against RandomAI, it resulted in more ties than wins.

### 2. AlphaBeta Pruning
Following lectures, we implemented AlphaBeta pruning, detecting possible jumps in the next moves, significantly improving performance against RandomAI. However, it proved time-consuming with increased depth.

### 3. Alternative Heuristic
Recognizing limitations, we explored an alternative heuristic, focusing on the sheer number of our checkers versus the opponent's. This adjustment demonstrated better efficacy with increased depth.

### 4. Monte Carlo Tree Search (MCTS)
To speed up processing, we adopted MCTS, developing two distinct models trained on separate datasets. However, a slow learning curve emerged, prompting the search for a student model capable of defeating Average AI within a limited training range.

### 5. Seed Monte Carlo Tree
To reduce tie movements, we pitted two Average AI agents against each other in 300 runs, refining our AI agents further over 10,000 iterations.

![Seed Monte Carlo Tree](https://github.com/jpyoo/Checkers-AI/assets/58375171/ba08f873-3629-4bd7-8ef8-37647dc25254)
![image](https://github.com/jpyoo/Checkers-AI/assets/58375171/76615a6e-f944-4774-9864-b952abc1c1c2)
## II. Problems Resolutions

To tackle time issues, the team transitioned to the Monte Carlo Tree Search algorithm, providing a balanced trade-off between computation time and decision accuracy. Learning curve issues were addressed by adjusting opponent levels during testing.

Challenges in determining the Exploration vs Exploitation rate were mitigated by implementing a cutoff Monte Carlo value. This adjustment improved decision-making efficiency while maintaining exploration.

### Key Implementations:
- Cutoff Monte Carlo Value: 1
- Try statements to address data corruption issues.
- Ongoing exploration for more efficient data structures or database usage.

## III. Suggestions for Improving This Project

1. **Temporal Difference for Learning:**
   Apply temporal difference methods to enhance adaptability and responsiveness, especially in conditions where reaching the end of the game is limited.

2. **Combination of AlphaBeta Pruning with MCTS:**
   Explore a combination of AlphaBeta pruning and MCTS to enhance decision-making speed and explore deeper depths within time limits.

3. **Setting Search Depth within Time Constraints:**
   Dynamically set search depth based on available time to optimize decision-making within time constraints. This adaptive approach ensures the AI makes the most informed decisions possible within the given time frame.
