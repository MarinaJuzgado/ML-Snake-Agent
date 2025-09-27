# Snake RL Agent – Autonomous agent to play Snake using Reinforcement Learning

## Project Overview
This project was developed as part of a university coursework at **Universidad Carlos III de Madrid (UC3M)**.  
The main goal was to design and implement intelligent agents capable of playing the Snake game automatically using **Machine Learning (ML)** and **Reinforcement Learning (RL)** techniques.

The project was divided into two main assignments:
1. **Assignment 1 – Supervised Learning**: Build classification and regression models using Weka to predict moves and scores from collected game data.  
2. **Assignment 2 – Reinforcement Learning (Q-Learning)**: Implement a Q-Learning agent that learns optimal policies directly from interaction with the environment.  

The **Snake environment code** was provided by UC3M. My contribution focused on the **data pipeline, ML experimentation, agent design, and Q-learning implementation**.

---

## Assignment 1: Supervised ML Agent (Weka)

### Objectives
- Collect game instances by playing manually.  
- Train **classification models** to decide the snake’s next move (N/S/E/W).  
- Train **regression models** to predict the score of the next tick.  
- Build an autonomous agent by integrating the best model into the simulator.  

### Results
- Classification with models like J48, Random Forest, Logistic Regression improved decision-making over baseline agents.  
- Regression models achieved reasonable accuracy predicting next-tick scores.  
- The supervised agent showed improvement but was limited by mimicking human gameplay.  

See the [Assignment 1 report](Reports/assignment1_report.pdf)  
See the Assignment 1 code in the [`Codes/Automatic Agent Code - Assignment 1`](Codes/Automatic%20Agent%20Code%20-%20Assignment%201/) folder

---

## Assignment 2: Q-Learning Agent

### Phase 1: State Representation & Reward Function
- Designed compact state attributes to keep the Q-table manageable  
- Defined a reward function

### Phase 2: Q-Learning Agent
- Implemented Q-table update mechanism following the **Q-learning algorithm**.  
- Designed exploration strategy with ε-greedy policy.  
- Tuned hyperparameters (α, γ, ε) to improve learning stability.  
- Implemented persistence to save/load Q-tables across sessions.  

### Phase 3: Agent Enhancement
- Extended state representation to account for snake body collisions.  
- Evaluated across multiple board sizes (150×150 to 480×480).  
- Observed that larger boards improved performance due to lower self-collision probability.  

### Results
- The Q-learning agent consistently outperformed the supervised agent.  
- Learned natural strategies  
- Demonstrated adaptability to different board sizes and robust performance.  

See the [Assignment 2 report](Reports/assignment2_report.pdf)  
See the Assignment 2 code in the [`Codes/Automatic Agent Code - Assignment 2`](Codes/Automatic%20Agent%20Code%20-%20Assignment%202/) folder
---

## Tech Stack
- **Languages:** Python 3.9, Java  
- **Libraries:**  
  - NumPy, pandas, matplotlib  
  - `python-weka-wrapper3`, `javabridge` (for Assignment 1)  
- **ML Approaches:**  
  - Supervised Learning (classification + regression)  
  - Reinforcement Learning (Q-learning)
