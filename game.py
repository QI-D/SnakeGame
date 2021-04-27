from snake import Snake
from food import Food
import pygame
import tkinter as tk
from tkinter import simpledialog, messagebox

import mysql.connector

temp_db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="MyNewPassword"
)

temp_cursor = temp_db.cursor()

temp_cursor.execute("CREATE DATABASE IF NOT EXISTS snakegame")
temp_db.commit()
temp_db.close()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="MyNewPassword",
    database="snakegame",
    auth_plugin="mysql_native_password"
)

cursor = db.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS scores (player VARCHAR(25), score INT, difficulty VARCHAR(15))")
db.commit()
db.close()


class Game():
    def __init__(self):
        self.ROOT = tk.Tk()
        self.ROOT.withdraw()
        self.DISPLAY = pygame.display.set_mode(
            (500, 500))
        # initalizes objects/game
        pygame.init()  # creates game
        pygame.font.init()  # gets pygame fonts
        self.snake = Snake()  # creates snake
        self.clock = pygame.time.Clock()  # fps setter
        self.food = Food()  # creates food
        self.scores = dict()

        pygame.display.set_caption('Snake Game')

        # Temporary window:  fifty 10 by 10 squares

        # TEXT FONTS
        self.menu_buttons = pygame.font.SysFont("comicsansms", 20)

        self.game = True

        # spawns food at a random location not on snake
        self.food.new_food(self.snake.get_pos[0])

        # Global Variables
        self.screen = "menu"
        self.restart = True
        self.difficulty = ""
        self.score = 0
        self.hunger = 0  # time since last meal

    def button(self, msg, x, y, w, h, color, click_color, text_color, font, action=None):
        mouse = pygame.mouse.get_pos()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.DISPLAY, click_color, (x, y, w, h))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return action()
        else:
            pygame.draw.rect(self.DISPLAY, color, (x, y, w, h))
        text = font.render(msg, True, text_color)
        text_rect = text.get_rect()
        text_rect.center = (x + w // 2, y + h // 2)
        self.DISPLAY.blit(text, text_rect)

    def record_score(self, name, score):
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="MyNewPassword",
            database="snakegame",
            auth_plugin="mysql_native_password"
        )
        cursor = db.cursor()
        cursor.execute("SELECT * FROM scores WHERE player = %s", (name,))
        result = cursor.fetchone()
        if result == None:
            cursor.execute(
                "INSERT INTO scores (player, score, difficulty) VALUES (%s, %s, %s)", (name, score, self.difficulty,))
            messagebox.showinfo(
                "Success", f"Score of {int(self.score)} recorded for player {name}!")
        else:
            db_score = result[1]
            if db_score <= score:
                cursor.execute(
                    "UPDATE scores SET score = %s, difficulty = %s WHERE player = %s", (score, self.difficulty, name))
            else:
                messagebox.showinfo(
                    "Failure", f"{name} already has a higher score than {int(self.score)}.")
        db.commit()
        db.close()
        return True

    def menu_action(self):
        self.screen = "menu"

    def record_action(self):
        name = simpledialog.askstring(title="Record Score",
                                      prompt="Please enter your player name:")
        if name is not None:
            if name != '':
                try:
                    int(name)
                    messagebox.showinfo(
                        "Invalid.", "The name you entered is invalid.")
                except ValueError:
                    if self.record_score(name, self.score):
                        self.screen = "menu"
                        return "success"
            else:
                messagebox.showinfo(
                    "Invalid.", "The name you entered is invalid.")
        return "menu"

    def calculate_score(self, ate=False):
        multiplier = 0
        if self.difficulty == "easy":
            multiplier = 1
        elif self.difficulty == "medium":
            multiplier = 5
        elif self.difficulty == "hard":
            multiplier = 10
        if not ate:
            self.hunger += 1
        else:
            self.hunger = 0
            self.score += 1*multiplier

        if self.score <= 0:
            self.score = 0

    def easy_action(self):
        self.food = Food()
        self.snake = Snake()
        self.DISPLAY.fill([0, 0, 0])
        self.food.new_food(self.snake.get_pos[0])
        self.snake.draw_on_display(self.DISPLAY)
        self.food.draw_on_display(self.DISPLAY)
        self.difficulty = "easy"
        self.screen = "game"

    def medium_action(self):
        self.food = Food()
        self.snake = Snake()
        self.DISPLAY.fill([0, 0, 0])
        self.food.new_food(self.snake.get_pos[0])
        self.snake.draw_on_display(self.DISPLAY)
        self.food.draw_on_display(self.DISPLAY)
        self.difficulty = "medium"
        self.screen = "game"

    def hard_action(self):
        self.food = Food()
        self.snake = Snake()
        self.DISPLAY.fill([0, 0, 0])
        self.food.new_food(self.snake.get_pos[0])
        self.snake.draw_on_display(self.DISPLAY)
        self.food.draw_on_display(self.DISPLAY)
        self.difficulty = "hard"
        self.screen = "game"

    def check_for_death(self):
        if any(self.snake.get_pos[1] == part for part in self.snake.get_pos[0][1:]):
            # check if head is on body part this frame

            return True
        return False

    def center(self, score):
        center = 240
        while score >= 10:
            score /= 10
            center -= 4
        return center

    def play(self):
        while self.game is True:

            if self.screen == "game":

                for event in pygame.event.get():  # Arrow key inputs
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.snake.left()
                        if event.key == pygame.K_RIGHT:
                            self.snake.right()
                        if event.key == pygame.K_UP:
                            self.snake.up()
                        if event.key == pygame.K_DOWN:
                            self.snake.down()
                    if event.type == pygame.QUIT:
                        pygame.quit()

                # snake.debug() #debug info
                if self.check_for_death():  # snake will die next round
                    self.screen = "lose"

                if self.snake.get_pos[1] == self.food.get_pos:
                    # makes snake longer if snake on food
                    self.snake.move(ate=True)
                    self.calculate_score(ate=True)
                    self.food.new_food(self.snake.get_pos[0])
                else:
                    self.calculate_score()
                    self.snake.move()

                self.DISPLAY.fill([0, 0, 0])

                self.button(str(int(self.score)), self.center(self.score), 0, 50, 50, [
                            0, 0, 0], [0, 0, 0], [255, 255, 255], self.menu_buttons)
                self.snake.draw_on_display(self.DISPLAY)
                self.food.draw_on_display(self.DISPLAY)
                pygame.display.flip()

            elif self.screen == "lose":
                self.DISPLAY.fill([0, 0, 0])
                self.button("Menu", 150, 150, 70, 35, [70, 102, 255], [90, 120, 255], [255, 255, 255], self.menu_buttons,
                            self.menu_action)
                self.button("Record score!", 250, 250, 175, 35, [70, 102, 255], [90, 120, 255], [255, 255, 255], self.menu_buttons,
                            self.record_action)
                self.button(f"Score: {int(self.score)}", 200, 200, 50, 35, [0, 0, 0], [0, 0, 0], [255, 255, 255],
                            self.menu_buttons)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

            elif self.screen == "menu":
                self.score = 0
                self.DISPLAY.fill([0, 0, 0])
                response = self.button("EASY!", 75, 150, 100, 35, [70, 102, 255], [90, 120, 255], [255, 255, 255],
                                       self.menu_buttons, self.easy_action)
                response2 = self.button("MEDIUM!", 210, 150, 100, 35, [70, 102, 255], [90, 120, 255], [255, 255, 255],
                                        self.menu_buttons, self.medium_action)
                response3 = self.button("HARD!", 345, 150, 100, 35, [70, 102, 255], [90, 120, 255], [255, 255, 255],
                                        self.menu_buttons, self.hard_action)
                if response == "game":  # simple menu system
                    self.screen = "game"
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

            if self.screen != "game":
                self.clock.tick(200)
            else:
                if self.difficulty == "easy":
                    self.clock.tick(10)
                elif self.difficulty == "medium":
                    self.clock.tick(15)
                elif self.difficulty == "hard":
                    self.clock.tick(20)
                else:
                    self.clock.tick(1)
