"""
Snake Eater Environment
Made with PyGame
Last modification in April 2024 by José Luis Perán
Machine Learning Classes - University Carlos III of Madrid
"""
import numpy as np
import random

class SnakeGameEnv:
    def __init__(self, frame_size_x=150, frame_size_y=150, growing_body=True):
        # Initializes the environment with default values
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        self.growing_body = growing_body
        self.reset()

    def reset(self):
        # Resets the environment with default values
        self.snake_pos = [50, 50]
        self.snake_body = [[50, 50], [60, 50], [70, 50]]
        self.food_pos = [random.randrange(1, (self.frame_size_x // 10)) * 10, random.randrange(1, (self.frame_size_y // 10)) * 10]
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.score = 0
        self.game_over = False
        return self.get_state()

    def step(self, action):
        # Implements the logic to change the snake's direction based on action
        # Update the snake's head position based on the direction
        # Check for collision with food, walls, or self
        # Update the score and reset food as necessary
        # Determine if the game is over
        state = self.get_state()
        self.update_snake_position(action)
        reward = self.calculate_reward()
        self.update_food_position()
        next_state = self.get_state()
        self.game_over = self.check_game_over()
        if self.game_over:
            next_state = None
        return state, next_state, reward, self.game_over

    def get_state(self):
        head_x, head_y = self.snake_pos # Snake head position
        food_x, food_y = self.food_pos  # Food position

        # --- Relative position ---
        if self.food_pos[0] <= self.snake_pos[0] and self.food_pos[1] <= self.snake_pos[1]:
            relative_pos = "0"
        if self.food_pos[0] <= self.snake_pos[0] and self.food_pos[1] > self.snake_pos[1]:
            relative_pos = "2"
        if self.food_pos[0] > self.snake_pos[0] and self.food_pos[1] <= self.snake_pos[1]:
            relative_pos = "1"
        if self.food_pos[0] > self.snake_pos[0] and self.food_pos[1] > self.snake_pos[1]:
            relative_pos = "3"

        # --- Danger attributes ---
        #Predict next positions for the four directions
        left_pos = [head_x - 10, head_y]
        right_pos = [head_x + 10, head_y]
        up_pos = [head_x, head_y - 10]
        down_pos = [head_x, head_y + 10]

        #Check if there are walls or if there is the snake body
        wall_left = (left_pos[0] < 0)
        wall_right = (right_pos[0] >= self.frame_size_x)
        #Use frame_size as in the statement it is said it must play in any board
        wall_up = (up_pos[1] < 0)
        wall_down = (down_pos[1] >= self.frame_size_y)

        body_left = left_pos in self.snake_body
        body_right = right_pos in self.snake_body
        body_up = up_pos in self.snake_body
        body_down = down_pos in self.snake_body

        #Define dangers
        danger_left = wall_left or body_left
        danger_right = wall_right or body_right
        danger_up = wall_up or body_up
        danger_down = wall_down or body_down

        #Current direction
        current_dir = self.direction

        #Return state
        state = (relative_pos, danger_right, danger_left, danger_up, danger_down, current_dir)
        return state

    def get_body(self):
    	return self.snake_body

    def get_food(self):
    	return self.food_pos

    def calculate_reward(self):
        reward = 0
        # 1. Check if snake eats the food
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            reward += 100  # Positive reward for eating food
        # 2. Check if snake collides
        if self.check_game_over(): #As when it collides the game is over
            reward -= 300  # Large negative reward for game over
        # 3. Small negative reward for each move to encourage efficient movement
        reward -= 1

        return reward
        
    def check_game_over(self):
        # Return True if the game is over, else False
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x-10:
            return True
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y-10:
            return True
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                return True
                
        return False

    def update_snake_position(self, action):
        # Updates the snake's position based on the action
        # Map action to direction
        change_to = ''
        direction = self.direction
        if action == 0:
            change_to = 'UP'
        elif action == 1:
            change_to = 'DOWN'
        elif action == 2:
            change_to = 'LEFT'
        elif action == 3:
            change_to = 'RIGHT'
    
        # Move the snake
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
    
        if direction == 'UP':
            self.snake_pos[1] -= 10
        elif direction == 'DOWN':
            self.snake_pos[1] += 10
        elif direction == 'LEFT':
            self.snake_pos[0] -= 10
        elif direction == 'RIGHT':
            self.snake_pos[0] += 10
            
        self.direction = direction
        
        
        self.snake_body.insert(0, list(self.snake_pos))
        
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 10
            self.food_spawn = False
            # If the snake is not growing
            if not self.growing_body:
                self.snake_body.pop()
        else:
            self.snake_body.pop()
    
    def update_food_position(self):
        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (self.frame_size_x//10)) * 10, random.randrange(1, (self.frame_size_x//10)) * 10]
        self.food_spawn = True
        
        

