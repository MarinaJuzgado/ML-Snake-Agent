"""
Snake Eater
Made with PyGame
Last modification in January 2024 by José Carlos Pulido
Machine Learning Classes - University Carlos III of Madrid
"""
from gettext import install


import pygame, sys, time, random, os
from wekaI import Weka


"""
File with ONLY the move_tutorial 1 implemented
"""

# DIFFICULTY settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
DIFFICULTY = 10

# Inicializar la JVM
weka = Weka()
weka.start_jvm()

# Window size
FRAME_SIZE_X = 480
FRAME_SIZE_Y = 480

# Colors (R, G, B)
BLACK = pygame.Color(51, 51, 51)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(204, 51, 0)
GREEN = pygame.Color(204, 255, 153)
BLUE = pygame.Color(0, 51, 102)

# GAME STATE CLASS
class GameState:
    def __init__(self, FRAME_SIZE):
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
        self.food_pos = [random.randrange(1, (FRAME_SIZE[0]//10)) * 10, random.randrange(1, (FRAME_SIZE[1]//10)) * 10]
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0

# Game Over
def game_over(game):
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, WHITE)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (FRAME_SIZE_X/2, FRAME_SIZE_Y/4)
    game_window.fill(BLUE)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(game, 0, WHITE, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

# Score
def show_score(game, choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(game.score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (FRAME_SIZE_X/8, 15)
    else:
        score_rect.midtop = (FRAME_SIZE_X/2, FRAME_SIZE_Y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()

# Move the snake
def move_keyboard(game, event):
    # Whenever a key is pressed down
    change_to = game.direction
    if event.type == pygame.KEYDOWN:
        # W -> Up; S -> Down; A -> Left; D -> Right
        if (event.key == pygame.K_UP or event.key == ord('w')) and game.direction != 'DOWN':
            change_to = 'UP'
        if (event.key == pygame.K_DOWN or event.key == ord('s')) and game.direction != 'UP':
            change_to = 'DOWN'
        if (event.key == pygame.K_LEFT or event.key == ord('a')) and game.direction != 'RIGHT':
            change_to = 'LEFT'
        if (event.key == pygame.K_RIGHT or event.key == ord('d')) and game.direction != 'LEFT':
            change_to = 'RIGHT'
    return change_to

# TODO: IMPLEMENT HERE THE NEW INTELLIGENT METHOD
def move_snake(game):
    snake_length = len(game.snake_body)
    # Generalise the coordinates of food and snake:
    if game.snake_pos[0] <= 240:
        snake_x = "WEST"
    if game.snake_pos[0] > 240:
        snake_x = "EAST"
    if game.snake_pos[1] <= 240:
        snake_y = "NORTH"
    if game.snake_pos[1] > 240:
        snake_y = "SOUTH"

    if game.food_pos[0] <= 240:
        food_x = "WEST"
    if game.food_pos[0] > 240:
        food_x = "EAST"
    if game.food_pos[1] <= 240:
        food_y = "NORTH"
    if game.food_pos[1] > 240:
        food_y = "SOUTH"

    if game.food_pos[0] <= game.snake_pos[0] and game.food_pos[1] <= game.snake_pos[1]:
        rel_pos = "0"
    if game.food_pos[0] <= game.snake_pos[0] and game.food_pos[1] > game.snake_pos[1]:
        rel_pos = "2"
    if game.food_pos[0] > game.snake_pos[0] and game.food_pos[1] <= game.snake_pos[1]:
        rel_pos = "1"
    if game.food_pos[0] > game.snake_pos[0] and game.food_pos[1] > game.snake_pos[1]:
        rel_pos = "3"

    score = game.score

    x = [snake_length, snake_x, snake_y, food_x, food_y, rel_pos, score]

    # Predecir la dirección con el modelo de Weka
    action = weka.predict("./RandomForest.model", x, "./training_keyboard.arff")

    # Imprimir el valor de la predicción para inspeccionarlo
    print("Predicción de Weka:", action)  # Esto mostrará el valor de la predicción

    # Mapeo de la predicción
    if action == "NORTH":
        return "UP"
    elif action == "SOUTH":
        return "DOWN"
    elif action == "WEST":
        return "LEFT"
    elif action == "EAST":
        return "RIGHT"

    # Si no se puede predecir, se sigue la dirección actual
    return game.direction

# PRINTING DATA FROM GAME STATE
def print_line_data(game, filename="all_data_snake.arff"):
    snake_length = len(game.snake_body)
    #Generalise the coordinates of food and snake:
    if game.snake_pos[0] <= 240:
        snake_x = "WEST"
    if game.snake_pos[0] > 240:
        snake_x = "EAST"
    if game.snake_pos[1] <= 240:
        snake_y = "NORTH"
    if game.snake_pos[1] > 240:
        snake_y = "SOUTH"

    if game.food_pos[0] <= 240:
        food_x = "WEST"
    if game.food_pos[0] > 240:
        food_x = "EAST"
    if game.food_pos[1] <= 240:
        food_y = "NORTH"
    if game.food_pos[1] > 240:
        food_y = "SOUTH"

    if game.food_pos[0] <= game.snake_pos[0] and game.food_pos[1] <= game.snake_pos[1]:
        rel_pos = "0"
    if game.food_pos[0] <= game.snake_pos[0] and game.food_pos[1] > game.snake_pos[1]:
        rel_pos = "2"
    if game.food_pos[0] > game.snake_pos[0] and game.food_pos[1] <= game.snake_pos[1]:
        rel_pos = "1"
    if game.food_pos[0] > game.snake_pos[0] and game.food_pos[1] > game.snake_pos[1]:
        rel_pos = "3"

    direction = game.direction
    score = game.score

    file_exists = os.path.exists(filename)

    with open(filename, mode="a") as file:
        # Write ARFF header
        if not file_exists:
            file.write("@RELATION snake_game\n\n")
            file.write("@ATTRIBUTE snake_length NUMERIC\n")
            file.write("@ATTRIBUTE snake_x {WEST, EAST}\n")
            file.write("@ATTRIBUTE snake_y {NORTH, SOUTH}\n")
            file.write("@ATTRIBUTE food_x {WEST, EAST}\n")
            file.write("@ATTRIBUTE food_y {NORTH, SOUTH}\n")
            file.write("@ATTRIBUTE rel_pos {0, 1, 2, 3}\n")
            file.write("@ATTRIBUTE score NUMERIC\n")
            file.write("@ATTRIBUTE direction {UP, DOWN, LEFT, RIGHT}\n\n")
            file.write("@DATA\n")

        # Write game state data
        data_line = (
                f"{snake_length},{snake_x},{snake_y},{food_x},{food_y},{rel_pos},{score},{direction}\n"
        )
        file.write(data_line)

# Checks for errors encounteRED
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Initialise game window
pygame.display.set_caption('Snake Eater - Machine Learning (UC3M)')
game_window = pygame.display.set_mode((FRAME_SIZE_X, FRAME_SIZE_Y))

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# Main logic
game = GameState((FRAME_SIZE_X,FRAME_SIZE_Y))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        # CALLING MOVE METHOD
        game.direction = move_keyboard(game, event)

    # UNCOMMENT WHEN METHOD IS IMPLEMENTED
    game.direction = move_snake(game)

    # Moving the snake
    if game.direction == 'UP':
        game.snake_pos[1] -= 10
    if game.direction == 'DOWN':
        game.snake_pos[1] += 10
    if game.direction == 'LEFT':
        game.snake_pos[0] -= 10
    if game.direction == 'RIGHT':
        game.snake_pos[0] += 10

    # Snake body growing mechanism
    game.snake_body.insert(0, list(game.snake_pos))
    if game.snake_pos[0] == game.food_pos[0] and game.snake_pos[1] == game.food_pos[1]:
        game.score += 100
        game.food_spawn = False
    else:
        game.snake_body.pop()
        game.score -= 1

    # Spawning food on the screen
    if not game.food_spawn:
        game.food_pos = [random.randrange(1, (FRAME_SIZE_X//10)) * 10, random.randrange(1, (FRAME_SIZE_Y//10)) * 10]
    game.food_spawn = True

    # GFX
    game_window.fill(BLUE)
    for pos in game.snake_body:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

    # Snake food
    pygame.draw.rect(game_window, RED, pygame.Rect(game.food_pos[0], game.food_pos[1], 10, 10))

    # Game Over conditions
    # Getting out of bounds
    if game.snake_pos[0] < 0 or game.snake_pos[0] > FRAME_SIZE_X-10:
        game_over(game)
    if game.snake_pos[1] < 0 or game.snake_pos[1] > FRAME_SIZE_Y-10:
        game_over(game)
    # Touching the snake body
    for block in game.snake_body[1:]:
        if game.snake_pos[0] == block[0] and game.snake_pos[1] == block[1]:
            game_over(game)

    show_score(game, 1, WHITE, 'consolas', 15)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(DIFFICULTY)