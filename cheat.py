import time
from tkinter import *

class CheatCode:
    def __init__(self, game):
        self.game = game
        self.cheats = [
            (["s", "t", "o", "p"], self.stop_cars),
            (["c", "l", "e", "a", "r"], self.clear),
            (["2", "x", "x"], self.double_points),
            (["3", "x", "x", "x"], self.triple_points),
            (["s", "p", "e", "e", "d"], self.speedy),
            (["i", "n", "v", "i", "n", "c", "i", "b", "l", "e"], self.invincible),
        ]
        self.last_key_time = time.time()  # Time of the last key press
        self.sequence_timer = 2.0  # Duration (in seconds) to complete the cheat code
        self.sequence = []  # Current key press sequence
        # Bind key events to update the key sequence
        self.game.window.bind("<KeyPress>", self.key_pressed)

    def key_pressed(self, event):
        # Add the pressed key to the current sequence or start a new sequence after 2s
        key = event.keysym.lower()
        elapsed_time = time.time() - self.last_key_time
        if elapsed_time > self.sequence_timer:
            self.sequence = []
        self.sequence.append(key)

        # Check for cheat code when a key is pressed
        action = self.check_cheat_code()
        if action:
            print("CHEAT!", action)

    def check_cheat_code(self):
        print(self.sequence)

        # Check if the current sequence matches the cheat code
        for cheat_sequence, action in self.cheats:
            if self.sequence == cheat_sequence:
                self.sequence = []
                action()
                return action

        # Update the last key press time
        self.last_key_time = time.time()

        return False
    
    # Cheat functions
    def stop_cars(self):
        self.game.car_stopped = not(self.game.car_stopped)
        print(self.game.car_stopped)

    def clear(self):
        self.game.canvas.delete("leftToRight")
        self.game.canvas.delete("rightToLeft")
        self.game.canvas.delete("obstacles")

    def double_points(self):
        self.game.multiplier = 2 if self.game.multipler != 2 else 1

    def triple_points(self):
        self.game.multiplier = 3 if self.game.multipler != 3 else 1

    def invincible(self):
        self.game.player.invincible = not(self.game.player.invincible)
    
    def speedy(self):
        self.game.player.speed = 40 if self.game.player.speed != 40 else 20