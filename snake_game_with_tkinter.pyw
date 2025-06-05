import tkinter
import random
import cryptography.fernet


class Game:

    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Snake Game")

        self.WIDTH = 520
        self.HEIGHT = 560

        self.CANVAS_HEIGHT = 520

        self.CELL_SIZE = 26

        self.LATENCY = 85

        self.window.geometry(f"{self.WIDTH}x{self.HEIGHT}+100+100")
        self.window.resizable(False, False)

        tkinter.Label(self.window, text="", font="Helvetica 1", bg="black").pack(expand=True)

        self.frame = tkinter.Frame(self.window, width=self.WIDTH - 2 * self.CELL_SIZE,
                                   height=self.HEIGHT - self.CANVAS_HEIGHT - self.CELL_SIZE, bg="black")
        self.frame.pack_propagate(False)
        self.frame.pack(side="top")

        self.canvas = tkinter.Canvas(self.window, width=self.WIDTH, height=self.CANVAS_HEIGHT, highlightthickness=0,
                                     bg="white")
        self.canvas.pack(side="bottom")
        self.canvas.focus_set()

        self.score_label = tkinter.Label(self.frame, text="Score : 0", font="Helvetica 14 bold", fg="cyan", bg="black")
        self.score_label.pack(side="left")

        self.window.configure(bg="black")

        self.snake_direction = "right"

        self.snake_body = None
        self.food_coordinates = None
        self.score_value = None

        self.KEY = "A722iTDrdGuUy6JPAiI7T2iE2cndT2MvlOVcVNUBW8g="

        self.fernet = cryptography.fernet.Fernet(bytes(self.KEY, "utf-8"))

        self.high_score = 0

        try:
            self.high_score = int(self.decrypt_high_score())
            assert 0 <= self.high_score <= ((self.WIDTH - 2 * self.CELL_SIZE) // self.CELL_SIZE) ** 2
        except (Exception,):
            with open("high_score_tkinter_game.txt", "wb") as file:
                file.write(b"")

        self.high_score_label = tkinter.Label(self.frame, text=f"Best Score : {self.high_score}",
                                              font='Helvetica 14 bold', fg="cyan", bg="black")
        self.high_score_label.pack(side="right")

        self.is_direction_changeable = True

        self.is_playing = False

        self.display_frame()
        self.create_snake()
        self.display_snake_body()

        self.canvas.create_text(self.WIDTH // 2, self.CANVAS_HEIGHT // 4,
                                text="Press <space> to start the game",
                                fill="orange", font='Helvetica 20 bold')

        self.bind_space_key()

        self.window.mainloop()

    def encrypt_high_score(self, value):
        with open("high_score_tkinter_game.txt", "wb") as file:
            file.write(self.fernet.encrypt(value))

    def decrypt_high_score(self):
        with open("high_score_tkinter_game.txt", "rb") as file:
            return self.fernet.decrypt(file.read())

    def display_frame(self):
        self.canvas.create_rectangle(0, 0, self.CELL_SIZE, self.CANVAS_HEIGHT, fill="black")
        self.canvas.create_rectangle(0, 0, self.WIDTH, self.CELL_SIZE, fill="black")
        self.canvas.create_rectangle(self.WIDTH - self.CELL_SIZE, 0, self.WIDTH, self.CANVAS_HEIGHT, fill="black")
        self.canvas.create_rectangle(0, self.CANVAS_HEIGHT - self.CELL_SIZE, self.WIDTH, self.CANVAS_HEIGHT,
                                     fill="black")

    def create_snake(self):
        self.snake_body = [
            (self.WIDTH // 2, self.CANVAS_HEIGHT // 2),
            (self.WIDTH // 2 + self.CELL_SIZE, self.CANVAS_HEIGHT // 2),
            (self.WIDTH // 2 + 2 * self.CELL_SIZE, self.CANVAS_HEIGHT // 2)
        ]

    def display_snake_body(self):
        for part in self.snake_body:
            self.canvas.create_rectangle(part[0], part[1],
                                         part[0] + self.CELL_SIZE, part[1] + self.CELL_SIZE,
                                         fill="green")

    def generate_food(self):
        self.food_coordinates = random.choice([
            (row, column)
            for row in range(self.CELL_SIZE, self.WIDTH - 2 * self.CELL_SIZE + 1, self.CELL_SIZE)
            for column in range(self.CELL_SIZE, self.CANVAS_HEIGHT - 2 * self.CELL_SIZE + 1, self.CELL_SIZE)
            if (row, column) not in self.snake_body
        ])

    def display_food(self):
        self.canvas.create_rectangle(self.food_coordinates[0],
                                     self.food_coordinates[1],
                                     self.food_coordinates[0] + self.CELL_SIZE,
                                     self.food_coordinates[1] + self.CELL_SIZE,
                                     fill="red")

    def start_game(self, _):
        self.canvas.delete("all")

        self.display_frame()

        self.snake_direction = "right"

        self.generate_food()
        self.display_food()

        self.bind_move_keys()

        self.score_value = 0
        self.score_label["text"] = "Score : 0"

        self.is_playing = True

        self.move()

    def bind_space_key(self):
        self.canvas.unbind("z")
        self.canvas.unbind("s")
        self.canvas.unbind("q")
        self.canvas.unbind("d")

        self.canvas.bind("<space>", self.start_game)

    def bind_move_keys(self):
        self.canvas.unbind("<space>")

        self.canvas.bind("z", self.move_up)
        self.canvas.bind("s", self.move_down)
        self.canvas.bind("q", self.move_left)
        self.canvas.bind("d", self.move_right)

    def move_up(self, _):
        if self.snake_direction in ("left", "right") and self.is_direction_changeable:
            self.snake_direction = "up"
            self.is_direction_changeable = False

    def move_down(self, _):
        if self.snake_direction in ("left", "right") and self.is_direction_changeable:
            self.snake_direction = "down"
            self.is_direction_changeable = False

    def move_left(self, _):
        if self.snake_direction in ("up", "down") and self.is_direction_changeable:
            self.snake_direction = "left"
            self.is_direction_changeable = False

    def move_right(self, _):
        if self.snake_direction in ("up", "down") and self.is_direction_changeable:
            self.snake_direction = "right"
            self.is_direction_changeable = False

    def move(self):
        will_grow_up = False

        snake_head = self.snake_body[-1]
        if (self.snake_direction == "right" and snake_head[0] + self.CELL_SIZE * 2 == self.WIDTH) or \
            (self.snake_direction == "left" and snake_head[0] - self.CELL_SIZE == 0) or \
            (self.snake_direction == "down" and snake_head[1] + self.CELL_SIZE * 2 == self.CANVAS_HEIGHT) or \
                (self.snake_direction == "up" and snake_head[1] - self.CELL_SIZE == 0):

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
                self.score_label["text"] = f"Score : {self.score_value}"

                if self.score_value > self.high_score:
                    self.high_score = self.score_value
                    self.high_score_label["text"] = f"Best Score : {self.high_score}"
                    self.encrypt_high_score(bytes(str(self.high_score), "utf-8"))
            else:
                new_snake_body = self.snake_body[1:] + [snake_head]

                if snake_head in new_snake_body[:-1]:
                    game_over = True

            self.snake_body = new_snake_body

            self.canvas.delete("all")

            self.display_frame()
            self.display_food()
            self.display_snake_body()

            if len(self.snake_body) == ((self.WIDTH - 2 * self.CELL_SIZE) // self.CELL_SIZE) ** 2:
                self.window.after(500, self.game_won)
            else:
                if will_grow_up:
                    self.generate_food()
                    self.display_food()

            if self.is_playing and not game_over:
                self.is_direction_changeable = True

                self.window.after(self.LATENCY, self.move)
            elif game_over:
                self.game_lost()

    def game_lost(self):
        self.is_playing = False

        self.canvas.delete("all")

        self.display_frame()
        self.create_snake()
        self.display_snake_body()

        return_char = "\n"
        self.canvas.create_text(self.WIDTH // 2, self.CANVAS_HEIGHT // 2,
                                text=f"            GAME OVER{return_char * 8}Press <space> to try again",
                                fill="red", font='Helvetica 20 bold')

        self.bind_space_key()

    def game_won(self):
        self.is_playing = False

        self.canvas.delete("all")

        self.display_frame()

        self.canvas.create_text(self.WIDTH // 2, self.CANVAS_HEIGHT // 2,
                                text="              YOU WON\n\n\n     "
                                     "You have reached the\nhighest possible score: 321\n\n\n              Well done!",
                                fill="blue", font='Helvetica 20 bold')


Game()
