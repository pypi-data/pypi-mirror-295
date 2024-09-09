import pygame
import time
import random

class SnakeGame:
    def __init__(self, screen_width=800, screen_height=600, snake_block=20, snake_speed=10):
        # Initialize Pygame
        pygame.init()

        # Colors
        self.white = (255, 255, 255)
        self.orange = (255, 165, 0)
        self.black = (0, 0, 0)

        # Screen dimensions
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Create the screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Set the title
        pygame.display.set_caption('Amazing Snake Game')

        # Clock to control the speed
        self.clock = pygame.time.Clock()

        # Snake attributes
        self.snake_block = snake_block
        self.snake_speed = snake_speed

        # Font
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 35)

    # Function to display the score
    def your_score(self, score):
        value = self.score_font.render("Your Score: " + str(score), True, self.white)
        self.screen.blit(value, [0, 0])

    # Function to draw our snake
    def our_snake(self, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.screen, self.orange, [x[0], x[1], self.snake_block, self.snake_block])

    # Function to display the message on the screen
    def message(self, msg, color):
        mesg = self.font_style.render(msg, True, color)
        self.screen.blit(mesg, [self.screen_width / 6, self.screen_height / 3])

    # Game Loop
    def gameLoop(self):
        game_over = False
        game_close = False

        x1 = self.screen_width / 2
        y1 = self.screen_height / 2

        x1_change = 0
        y1_change = 0

        snake_list = []
        length_of_snake = 1

        foodx = round(random.randrange(0, self.screen_width - self.snake_block) / 20.0) * 20.0
        foody = round(random.randrange(0, self.screen_height - self.snake_block) / 20.0) * 20.0

        while not game_over:

            while game_close:
                self.screen.fill(self.black)
                self.message("You Lost! Press Q-Quit or C-Play Again", self.white)
                self.your_score(length_of_snake - 1)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            self.gameLoop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -self.snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = self.snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -self.snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = self.snake_block
                        x1_change = 0

            if x1 >= self.screen_width or x1 < 0 or y1 >= self.screen_height or y1 < 0:
                game_close = True
            x1 += x1_change
            y1 += y1_change
            self.screen.fill(self.black)

            # Draw food as a circle
            pygame.draw.circle(self.screen, self.white, (int(foodx) + self.snake_block // 2, int(foody) + self.snake_block // 2), self.snake_block // 2)

            snake_head = [x1, y1]
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for x in snake_list[:-1]:
                if x == snake_head:
                    game_close = True

            self.our_snake(snake_list)
            self.your_score(length_of_snake - 1)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, self.screen_width - self.snake_block) / 20.0) * 20.0
                foody = round(random.randrange(0, self.screen_height - self.snake_block) / 20.0) * 20.0
                length_of_snake += 1

            self.clock.tick(self.snake_speed)

        pygame.quit()
        quit()

def play():
    game = SnakeGame()
    game.gameLoop()
