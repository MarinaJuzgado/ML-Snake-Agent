import numpy as np
import random


class SnakeAgent:
    def __init__(self, n_states, n_actions, alpha=0.1, epsilon=0.1, discount=0.9, q_table_file="q_table.txt"):
        self.n_states = n_states
        self.n_actions = n_actions
        self.alpha = alpha  # Learning rate
        self.epsilon = epsilon  # Exploration probability
        self.discount = discount  # Discount factor
        self.q_table_file = q_table_file

        try: #In case q-table file exists, load it and if not create it
            self.q_table = np.loadtxt(self.q_table_file)
            if self.q_table.shape != (n_states, n_actions):
                raise ValueError("Invalid Q-table shape, reinitializing.")
        except:
            self.q_table = np.zeros((n_states, n_actions))

    def save_q_table(self): #Save to a txt file
        np.savetxt(self.q_table_file, self.q_table)

    def encode_state(self, state):
        #Encode into a single integer among the possible states (256 possible, from 0 to 255)
        relative_pos, danger_right, danger_left, danger_up, danger_down, current_dir = state

        # Map the relative_pos
        rel = int(relative_pos)  # already a string "0", "1", "2", "3", so int() is ok

        # Map the dangers: True = 1, False = 0
        dr = int(danger_right)
        dl = int(danger_left)
        du = int(danger_up)
        dd = int(danger_down)

        # Map the current direction
        dir_map = {"UP": 0, "DOWN": 1, "LEFT": 2, "RIGHT": 3}
        cd = dir_map[current_dir]

        # Combine all into a unique number
        index = rel
        index = index * 2 + dr
        index = index * 2 + dl
        index = index * 2 + du
        index = index * 2 + dd
        index = index * 4 + cd

        return index

    def get_q_value(self, state, action): #Get state and action and find the q-value in the table
        state_idx = self.encode_state(state)
        return self.q_table[state_idx, action]

    def get_action(self, state): #decide wwhat action it is better to take now
        if np.random.uniform(0, 1) < self.epsilon:
            return random.randint(0, self.n_actions - 1)  # Random action with p epsilon
        else:
            state_idx = self.encode_state(state)
            return np.argmax(self.q_table[state_idx]) # Choose best action

    def update(self, state, action, next_state, reward): #Update q-table
        state_idx = self.encode_state(state)
        next_state_idx = self.encode_state(next_state)

        predict = self.q_table[state_idx, action] #current q-value of the state
        target = reward + self.discount * np.max(self.q_table[next_state_idx]) #q-learning rule

        self.q_table[state_idx, action] = (1 - self.alpha) * predict + self.alpha * target #update
