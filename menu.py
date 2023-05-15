from ursina import *
class Menu:
    def __init__(self, game_setup_callback):
        self.start_button = Button(text='Start Game', scale=(0.25, 0.1), position=(0, 0.1), color=color.azure)
        self.start_button.on_click = self.start_game

        self.exit_button = Button(text='Exit', scale=(0.25, 0.1), position=(0, -0.1), color=color.azure)
        self.exit_button.on_click = self.exit_game

        self.game_setup = game_setup_callback

    def start_game(self):
        self.hide_menu()
        self.game_setup()

        print("Start Game button clicked!")

    def exit_game(self):
        print("Exit button clicked!")
        application.quit()

    def hide_menu(self):
        self.start_button.enabled = False
        self.exit_button.enabled = False

    def show_menu(self):
        self.start_button.enabled = True
        self.exit_button.enabled = True