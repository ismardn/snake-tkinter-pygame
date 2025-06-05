import pygame
import random
import cryptography.fernet
import time


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")

        self.WIDTH = 520
        self.HEIGHT = 560

        self.CELL_SIZE = 26

        self.SPEED = 85

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.CANVAS_HEIGHT = 520

        self.snake_direction = "right"

        self.snake_body = None
        self.food_coordinates = None
        self.score_value = None

        self.score_surface = pygame.Surface(((self.WIDTH - 2 * self.CELL_SIZE) // 2, self.HEIGHT - self.CANVAS_HEIGHT))
        self.score_surface.fill("black")

        self.frame_game_surface = pygame.Surface((self.WIDTH - 2 * self.CELL_SIZE,
                                                  self.CANVAS_HEIGHT - 2 * self.CELL_SIZE))
        self.clear_game_surface()

        self.create_score_text(0)

        self.KEY = "A722iTDrdGuUy6JPAiI7T2iE2cndT2MvlOVcVNUBW8g="

        self.fernet = cryptography.fernet.Fernet(bytes(self.KEY, "utf-8"))

        self.high_score = 0

        try:
            self.high_score = int(self.decrypt_high_score())
            assert 0 <= self.high_score <= ((self.WIDTH - 2 * self.CELL_SIZE) // self.CELL_SIZE) ** 2
        except (Exception,):
            with open("high_score_tkinter_game.txt", "wb") as file:
                file.write(b"")

        self.create_high_score_text(self.high_score)

        start_game_text = pygame.font.SysFont("Helvetica", 27, True).render("Press <space> to start the game", True,
                                                                            "orange")
        start_game_text_rectangle = start_game_text.get_rect()
        start_game_text_rectangle.centerx = self.WIDTH // 2
        start_game_text_rectangle.centery = self.HEIGHT - self.CANVAS_HEIGHT + self.CANVAS_HEIGHT // 4
        self.window.blit(start_game_text, start_game_text_rectangle)

        self.is_running = True

        self.is_direction_changeable = True

        self.is_playing = False

        self.create_snake()
        self.display_snake_body()

        self.game_events()

    def clear_game_surface(self):
        self.frame_game_surface.fill("white")
        self.window.blit(self.frame_game_surface, (self.CELL_SIZE, self.HEIGHT - self.CANVAS_HEIGHT + self.CELL_SIZE))

        black_left_line = pygame.Surface((self.CELL_SIZE, self.HEIGHT))
        black_left_line.fill("black")
        self.window.blit(black_left_line, (0, 0))

        black_right_line = pygame.Surface((self.CELL_SIZE, self.HEIGHT))
        black_right_line.fill("black")
        self.window.blit(black_right_line, (self.WIDTH - self.CELL_SIZE, 0))

        black_top_line = pygame.Surface((self.WIDTH, self.CELL_SIZE))
        black_top_line.fill("black")
        self.window.blit(black_top_line, (0, self.HEIGHT - self.CANVAS_HEIGHT))

        black_bottom_line = pygame.Surface((self.WIDTH, self.CELL_SIZE))
        black_bottom_line.fill("black")
        self.window.blit(black_bottom_line, (0, self.HEIGHT - self.CELL_SIZE))

    def create_score_text(self, score):
        self.window.blit(self.score_surface, (self.CELL_SIZE, 0))

        score_text = pygame.font.SysFont("Helvetica", 20, True).render(f"Score : {score}", True, "cyan")
        self.window.blit(score_text, (self.CELL_SIZE, (self.HEIGHT - self.CANVAS_HEIGHT) // 2))

    def create_high_score_text(self, score):
        self.window.blit(self.score_surface, (self.WIDTH // 2, 0))

        high_score_text = pygame.font.SysFont("Helvetica", 20, True).render(f"Best Score : {score}", True, "cyan")
        high_score_text_rectangle = high_score_text.get_rect()
        high_score_text_rectangle.right = self.WIDTH - self.CELL_SIZE
        high_score_text_rectangle.top = (self.HEIGHT - self.CANVAS_HEIGHT) // 2
        self.window.blit(high_score_text, high_score_text_rectangle)

    def encrypt_high_score(self, value):
        with open("high_score_pygame_game.txt", "wb") as file:
            file.write(self.fernet.encrypt(value))

    def decrypt_high_score(self):
        with open("high_score_pygame_game.txt", "rb") as file:
            return self.fernet.decrypt(file.read())

    def create_snake(self):
        self.snake_body = [
            (self.WIDTH // 2, self.HEIGHT - self.CANVAS_HEIGHT + self.CANVAS_HEIGHT // 2),
            (self.WIDTH // 2 + self.CELL_SIZE, self.HEIGHT - self.CANVAS_HEIGHT + self.CANVAS_HEIGHT // 2),
            (self.WIDTH // 2 + 2 * self.CELL_SIZE, self.HEIGHT - self.CANVAS_HEIGHT + self.CANVAS_HEIGHT // 2)
        ]

    def display_snake_body(self):
        for part in self.snake_body:
            part_surface = pygame.Surface((self.CELL_SIZE, self.CELL_SIZE))
            part_surface.fill("green4")
            pygame.draw.rect(part_surface, "black", (0, 0, self.CELL_SIZE, self.CELL_SIZE), 1)
            self.window.blit(part_surface, (part[0], part[1]))

    def generate_food(self):
        self.food_coordinates = random.choice([
            (row, column)
            for row in range(self.CELL_SIZE, self.WIDTH - 2 * self.CELL_SIZE + 1, self.CELL_SIZE)
            for column in range(self.HEIGHT - self.CANVAS_HEIGHT + self.CELL_SIZE, self.HEIGHT - 2 * self.CELL_SIZE + 1,
                                self.CELL_SIZE)
            if (row, column) not in self.snake_body
        ])

    def display_food(self):
        food_surface = pygame.Surface((self.CELL_SIZE, self.CELL_SIZE))
        food_surface.fill("red")
        pygame.draw.rect(food_surface, "black", (0, 0, self.CELL_SIZE, self.CELL_SIZE), 1)
        self.window.blit(food_surface, (self.food_coordinates[0], self.food_coordinates[1]))

    def start_game(self):
        self.clear_game_surface()

        self.snake_direction = "right"

        self.generate_food()
        self.display_food()

        self.score_value = 0
        self.create_score_text(0)

        self.is_playing = True

    def move_up(self):
        if self.snake_direction in ("left", "right") and self.is_direction_changeable:
            self.snake_direction = "up"
            self.is_direction_changeable = False

    def move_down(self):
        if self.snake_direction in ("left", "right") and self.is_direction_changeable:
            self.snake_direction = "down"
            self.is_direction_changeable = False

    def move_left(self):
        if self.snake_direction in ("up", "down") and self.is_direction_changeable:
            self.snake_direction = "left"
            self.is_direction_changeable = False

    def move_right(self):
        if self.snake_direction in ("up", "down") and self.is_direction_changeable:
            self.snake_direction = "right"
            self.is_direction_changeable = False

    def game_events(self):
        while self.is_running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.is_running = False
                    exit()

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE and not self.is_playing:
                        self.start_game()

                    elif event.key == pygame.K_z and self.is_playing:
                        self.move_up()
                    elif event.key == pygame.K_s and self.is_playing:
                        self.move_down()
                    elif event.key == pygame.K_q and self.is_playing:
                        self.move_left()
                    elif event.key == pygame.K_d and self.is_playing:
                        self.move_right()

            if self.is_playing:
                will_grow_up = False

                snake_head = self.snake_body[-1]
                if snake_head[0] == 0 or snake_head[0] + self.CELL_SIZE == self.WIDTH or \
                        snake_head[1] + self.CELL_SIZE == self.HEIGHT or \
                        snake_head[1] == self.HEIGHT - self.CANVAS_HEIGHT:
                    self.game_lost()
                else:
                    game_over = False

                    if self.snake_direction == "right":
                        snake_head = (self.snake_body[-1][0] + self.CELL_SIZE, self.snake_body[-1][1])
                    elif self.snake_direction == "left":
                        snake_head = (self.snake_body[-1][0] - self.CELL_SIZE, self.snake_body[-1][1])
                    elif self.snake_direction == "down":
                        snake_head = (self.snake_body[-1][0], self.snake_body[-1][1] + self.CELL_SIZE)
                    else:
                        snake_head = (self.snake_body[-1][0], self.snake_body[-1][1] - self.CELL_SIZE)

                    if snake_head == self.food_coordinates:
                        will_grow_up = True
                        new_snake_body = self.snake_body + [snake_head]

                        self.score_value += 1
                        self.create_score_text(self.score_value)

                        if self.score_value > self.high_score:
                            self.high_score = self.score_value
                            self.create_high_score_text(self.high_score)
                            self.encrypt_high_score(bytes(str(self.high_score), "utf-8"))
                    else:
                        new_snake_body = self.snake_body[1:] + [snake_head]

                        if snake_head in new_snake_body[:-1]:
                            game_over = True

                    self.snake_body = new_snake_body

                    self.clear_game_surface()

                    self.display_food()
                    self.display_snake_body()

                    if len(self.snake_body) == ((self.WIDTH - 2 * self.CELL_SIZE) // self.CELL_SIZE) ** 2:
                        time.sleep(0.5)
                        self.game_won()
                    else:
                        if will_grow_up:
                            self.generate_food()
                            self.display_food()

                    if self.is_playing and not game_over:
                        self.is_direction_changeable = True

                        time.sleep(self.SPEED / 1000)
                    elif game_over:
                        self.game_lost()

            pygame.display.update()

    def game_lost(self):
        self.is_playing = False

        self.clear_game_surface()

        self.create_snake()
        self.display_snake_body()

        gameover_text = pygame.font.SysFont("Helvetica", 27, True).render("GAME OVER", True, "red")
        gameover_text_rectangle = gameover_text.get_rect()
        gameover_text_rectangle.centerx = self.WIDTH // 2
        gameover_text_rectangle.y = self.HEIGHT - self.CANVAS_HEIGHT + int(4.5 * self.CELL_SIZE)
        self.window.blit(gameover_text, gameover_text_rectangle)

        tryagain_text = pygame.font.SysFont("Helvetica", 27, True).render("Press <space> to try again", True, "red")
        tryagain_text_rectangle = tryagain_text.get_rect()
        tryagain_text_rectangle.centerx = self.WIDTH // 2
        tryagain_text_rectangle.y = self.HEIGHT // 2 + 5 * self.CELL_SIZE
        self.window.blit(tryagain_text, tryagain_text_rectangle)

    def game_won(self):
        self.is_playing = False

        self.clear_game_surface()

        youwon_text = pygame.font.SysFont("Helvetica", 27, True).render("YOU WON", True, "blue")
        youwon_text_rectangle = youwon_text.get_rect()
        youwon_text_rectangle.centerx = self.WIDTH // 2
        youwon_text_rectangle.y = self.HEIGHT - self.CANVAS_HEIGHT + 5 * self.CELL_SIZE
        self.window.blit(youwon_text, youwon_text_rectangle)

        reached_text = pygame.font.SysFont("Helvetica", 27, True).render("You have reached the", True, "blue")
        reached_text_rectangle = reached_text.get_rect()
        reached_text_rectangle.centerx = self.WIDTH // 2
        reached_text_rectangle.centery = self.HEIGHT // 2
        self.window.blit(reached_text, reached_text_rectangle)

        highestscore_text = pygame.font.SysFont("Helvetica", 27, True).render("highest possible score: 321", True,
                                                                              "blue")
        highestscore_text_rectangle = highestscore_text.get_rect()
        highestscore_text_rectangle.centerx = self.WIDTH // 2
        highestscore_text_rectangle.centery = self.HEIGHT // 2 + int(1.25 * self.CELL_SIZE)
        self.window.blit(highestscore_text, highestscore_text_rectangle)

        welldone_text = pygame.font.SysFont("Helvetica", 27, True).render("Well done!", True, "blue")
        welldone_text_rectangle = welldone_text.get_rect()
        welldone_text_rectangle.centerx = self.WIDTH // 2
        welldone_text_rectangle.y = self.HEIGHT // 2 + int(4.5 * self.CELL_SIZE)
        self.window.blit(welldone_text, welldone_text_rectangle)


Game()
