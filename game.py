from tkinter import *
import random
from player import Player
from vehicle import Vehicle
from helper import *
from save import Save
from cheat import CheatCode
import os

#Resolution=1280x720
""" ---------------------------------------Window Configuration--------------------------------------------- """

def configure_window(width, height):
    window.title("Crossy Road")
    window.resizable(False, False)
    center_window(width, height, window)

def center_window(width, height, win):
    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    win.geometry(f"{width}x{height}+{x}+{y}")

""" ---------------------------------------Game--------------------------------------------- """

class Game():
    def __init__(self, window):
        self.window = window
        self.round = 1
        self.game_running = False
        self.paused = False
        self.multiplier = 1

        # Create a canvas
        self.canvas = Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="white")
        self.canvas.pack()

        # To be initialised later when user has inputted a name
        self.player = None

        # Home screen labels and buttons 
        self.popupwindow = None
        self.name_label = Label(self.popupwindow, text="Enter your name:")
        self.name_entry = Entry(self.popupwindow, width=20)
        self.play_btn = Button(self.popupwindow, text="New Game", command=self.play)
        self.load_btn = Button(self.popupwindow, text="Load Game", command=self.load_game)
        self.lb_btn = Button(self.popupwindow, text="Leaderboards", command=self.show_leaderboard)
        self.settings_btn = Button(self.popupwindow, text="Settings", command=self.show_settings)
        self.quit_btn = Button(self.popupwindow, text="Quit", command=self.quit_everything)

        # Displayed if game has started but paused
        self.continue_btn = Button(self.popupwindow, text="Continue", command=self.unpause_game)
        self.save_btn = Button(self.popupwindow, text="Save & Exit", command=self.save_game)
        self.end_btn = Button(self.popupwindow, text="End Game", command=self.end_game)

        # Displayed error message when error occurs
        self.error_label = Label(self.popupwindow, text="", fg="red")

        # Game over screen labels and buttons
        self.game_over_label = Label(self.window, text="Game Over", font=("Helvetica", 24))
        self.game_over_score_label = Label(self.window, text="You Scored: ", font=("Helvetica", 18))
        self.game_over_high_score_label = Label(self.window, text="High Score: ", font=("Helvetica", 18))
        self.play_again_btn = Button(self.window, text="Play Again", command=self.play_again)
        self.back_btn = Button(self.window, text="Back", command=self.back)

        # Stats labels
        self.high_score_label = Label(self.canvas, text="High Score: ")
        self.score_label = Label(self.canvas, text="Current Score: ")
        self.round_label = Label(self.canvas, text="Current Round: ")
        self.player_label = Label(self.canvas, text="Player Name")

        self.work_image = None
        self.car_stopped = False
        self.cheat = CheatCode(self)

    def show_popup(self):
        # Recreate the widgets and pack them
        self.popupwindow = Toplevel(self.window)
        self.popupwindow.title("Crossy Road")
        center_window(POPUP_WINDOW_WIDTH, POPUP_WINDOW_HEIGHT, self.popupwindow)

        self.popupwindow.protocol("WM_DELETE_WINDOW", self.window.destroy)  # closes main window if popup is closed
        
        self.error_label = Label(self.popupwindow, text="", fg="red")
        self.name_label = Label(self.popupwindow, text="Enter your name:")
        self.name_entry = Entry(self.popupwindow, width=20)
        self.play_btn = Button(self.popupwindow, text="New Game", command=self.play)
        self.load_btn = Button(self.popupwindow, text="Load Game", command=self.load_game)
        self.lb_btn = Button(self.popupwindow, text="Leaderboards", command=self.show_leaderboard)
        self.settings_btn = Button(self.popupwindow, text="Settings", command=self.show_settings)
        self.quit_btn = Button(self.popupwindow, text="Quit", command=self.quit_everything)

        self.show_home_text()

    def back_to_home(self):
        for widget in self.popupwindow.winfo_children():
            widget.pack_forget()
            widget.place_forget()

        self.show_home_text()

    def end_game(self):
        self.unpause_game()
        self.game_over()

    def show_home_text(self):
        if not self.game_running:
            self.error_label.pack(pady=(POPUP_WINDOW_HEIGHT//25, 3))
            self.name_label.pack(pady=3)
            self.name_entry.pack(pady=3)
            self.play_btn.pack(pady=3)
            self.load_btn.pack(pady=3)
        else:
            self.continue_btn = Button(self.popupwindow, text="Continue", command=self.unpause_game)
            self.continue_btn.pack(pady=(POPUP_WINDOW_HEIGHT//6,3))
            self.save_btn = Button(self.popupwindow, text="Save & Exit", command=self.save_game)
            self.save_btn.pack(pady=3)
            self.end_btn = Button(self.popupwindow, text="End Game", command=self.end_game)
            self.end_btn.pack(pady=3)
        self.lb_btn.pack(pady=3)
        self.settings_btn.pack(pady=3)
        self.quit_btn.pack(pady=3)
            
        self.popupwindow.update_idletasks()

    def hide_all_text(self):
        self.name_label.pack_forget()
        self.name_entry.pack_forget()
        self.play_btn.pack_forget()
        self.load_btn.pack_forget()
        self.continue_btn.pack_forget()
        self.save_btn.pack_forget
        self.end_btn.pack_forget()
        self.lb_btn.pack_forget()
        self.settings_btn.pack_forget()
        self.quit_btn.pack_forget()
        self.error_label.pack_forget()
        self.play_again_btn.pack_forget()
        self.back_btn.pack_forget()
        self.game_over_label.pack_forget()
        self.game_over_score_label.pack_forget()
        self.game_over_high_score_label.pack_forget()

    def quit_everything(self):
        self.popupwindow.destroy()  # Destroy the popup window
        window.quit()  # Terminate the main loop
        window.destroy()  # Destroy the main window

    def back(self):
        self.hide_stats()
        self.hide_all_text()
        self.canvas.pack()
        self.generate_new_map()

        self.show_popup()
        self.show_home_text()
        self.popupwindow.mainloop()

    def show_leaderboard(self):
        pass

    def show_settings(self):
        self.hide_all_text()
        
        self.back_to_home_btn = Button(self.popupwindow, text="Back", command=self.back_to_home)
        self.back_to_home_btn.place(relx=0.0, rely=0.0, anchor=NW, in_=self.popupwindow)

        def change_key(event, action):
            key = event.keysym
            # Exit if <esc> is pressed
            if key == 'Escape':
                self.popupwindow.unbind('<KeyPress>')
                return

            # Only save the first key pressed, then stop tracking key press
            self.change_key_binding(action, key)
            action_labels[action].config(text=key)
            self.popupwindow.unbind('<KeyPress>')

        def action_btn(action):
            self.popupwindow.bind('<KeyPress>', lambda event: change_key(event, action))
        
        key_bindings = read_keybinds("keybinds.txt")
        
        actions = default_binds.keys()
        action_labels = {}

        frame = Frame(self.popupwindow)
        frame.pack(side="top", pady=POPUP_WINDOW_HEIGHT//14)
        for action in actions:
            frame = Frame(self.popupwindow)
            frame.pack(side="top", pady=4)

            btn = Button(frame, text=action, command=lambda a=action: action_btn(a))
            btn.pack(side="left")

            label = Label(frame, text=key_bindings[action])
            label.pack(side="left")

            action_labels[action] = label  # Store the label in the dictionary

    def show_leaderboard(self):
        self.hide_all_text()
        
        self.back_to_home_btn = Button(self.popupwindow, text="Back", command=self.back_to_home)
        self.back_to_home_btn.place(relx=0.0, rely=0.0, anchor=NW, in_=self.popupwindow)

        with open('leaderboard.txt', 'r') as file:
            top_10_lines = [next(file).strip() for _ in range(10)]
        
        # Create labels to display the top 10 names and scores
        for i, line in enumerate(top_10_lines):
            label_text = f'{i + 1}. {line}'
            label = Label(self.popupwindow, text=label_text)
            label.pack(pady=3)
        
    # Clear and create a new game background
    def generate_new_map(self):
        # Delete old player, coin, vehicles, obstacles, etc.
        self.canvas.delete("all")

        draw_game_background(self.canvas)
        spawn_obstacles(self.canvas, self.round)
        x = random.uniform(END_COIN_SIZE, WINDOW_WIDTH - END_COIN_SIZE) 
        y = random.uniform(END_COIN_SIZE, road_height - END_COIN_SIZE)
        spawn_end_coin(self.canvas, x, y)
        spawn_starting_vehicles_and_coins(self.spawn_vehicle, self.canvas)

    def show_stats(self):
        self.high_score_label.place(relx=1.0, rely=0.0, anchor=NE, in_=self.canvas)
        self.high_score_label.config(text='High Score: ' + str(self.player.high_score), font=("Helvetica", 16))

        # Display Current round in top left
        self.round_label.place(relx=0.0, rely=0.0, anchor=NW, in_=self.canvas)
        self.round_label.config(text='Current Round: ' + str(self.round), font=("Helvetica", 16))

        self.score_label.place(relx=0.0, rely=0.04, anchor=NW, in_=self.canvas)
        self.score_label.config(text='Current Score: ' + str(self.player.score), font=("Helvetica", 16))

        # Display Player name at the top
        self.player_label.place(relx=0.5, rely=0.0, in_=self.canvas)
        self.player_label.config(text=self.player.name, font=("Helvetica", 16))
    
    def hide_stats(self):
        self.high_score_label.place_forget()
        self.score_label.place_forget()
        self.round_label.place_forget()
        self.player_label.place_forget()

    # Create a vehicle object and draw it on screen
    def spawn_vehicle(self, x, y, direction): # x, y = initial position on road
        vehicle = Vehicle(self.canvas, x, y, direction)
        vehicle.spawn()
    
    def spawn_vehicles(self):
        # Recursive loop of spawning vehicles until game stops
        def spawn_more_vehicles():
            # To spawn vehicle on each road, increments by 1 until all roads have spawned 1 car then loops
            def spawn_vehicle_per_road(i):
                if self.paused or not self.game_running or i == NUMBER_OF_ROADS or self.car_stopped:
                    return False
                y = space_between_roads + i * (road_height + space_between_roads)
                isEven = i%2==0
                self.spawn_vehicle(isEven * 1280, y, "rightToLeft" if isEven else "leftToRight") 
                # create an offset, so all 4 vehicles don't spawn at same time
                offset = int(random.uniform(1/self.round, 2.5/self.round) * 1000)
                self.window.after(offset, lambda: spawn_vehicle_per_road(i + 1))
            if not self.paused and self.game_running:    
                spawn_vehicle_per_road(0)

            """
            Schedule the next iteration after a delay
            
            Delay:
            - needs to be relative to speed so they don't spawn next adjacent / on top of each other
            - shorter delay as rounds progress so game gets harder (more vehicles)

            Calculation:
                - Speed = 2 pixels per (BASE_DELAY // round) ms  
                - distance = self.size * 1.5 (as vehicles are spawned halfway on screen)
                - time = d/t = (self.size * 1.5 // 2) * (BASE_DELAY // round)
            delay > time to not overlay
            """
            time = VEHICLE_SIZE * (BASE_DELAY // self.round)
            delay = int(random.uniform(time, time*4)) # Leave enough delay for player to cross road
            self.window.after(delay, spawn_more_vehicles) # Repeat function after delay
        
        spawn_more_vehicles()
            
    def detect_collision(self, tags, margin):
        if self.game_running:
            player_coords = self.canvas.bbox(self.player.sprite_id)
            object_ids = [obj_id for tag in tags for obj_id in self.canvas.find_withtag(tag)]
        
            for object in object_ids:
                object_coords = self.canvas.bbox(object)
                if (player_coords[0] < object_coords[2] - margin and      
                    player_coords[2] > object_coords[0] + margin and
                    player_coords[1] < object_coords[3] - margin and
                    player_coords[3] > object_coords[1] + margin):
                    # Collision detected
                    return object
        return False
            
    def move_vehicles(self):
        # If game is still running, Move all vehicles in their direction by 2 pixels horizontally every 50 ms
        if  self.game_running:
            # Move cars if game isn't paused and stop cheat code isn't active
            if not self.paused and not self.car_stopped:
                self.canvas.move("leftToRight", 2, 0)
                self.canvas.move("rightToLeft", -2, 0)
            # Ends game when vehicle is touched
            if self.detect_collision(["leftToRight", "rightToLeft"], 5) and not self.player.invincible:
                self.game_over()

            # Ends round when final coin is touched
            if self.detect_collision(["end_coin"], 0):    
                self.next_round()

            # Increment score when coin is collected
            coin = self.detect_collision(["coin"], 0)
            if coin:
                self.player.score += self.round * self.multiplier
                self.canvas.delete(coin)
                self.score_label.config(text='Current Score: ' + str(self.player.score), font=("Helvetica", 16))
            self.window.after(BASE_DELAY - int(self.round * 0.1), self.move_vehicles)

    def start_round(self):
        self.generate_new_map()
        self.show_stats()

        # Spawn Player
        self.player.spawn_player(WINDOW_WIDTH / 2, WINDOW_HEIGHT - road_height / 2)
        self.paused = False
        
        self.move_vehicles()

    def next_round(self):
        self.paused = True
        self.round += 1
        self.start_round()
        
    def game_over(self):
        # Display Game over message
        self.game_running = False

        self.game_over_label.pack(pady=(self.canvas.winfo_width()//5, 5))
        self.game_over_score_label.pack(pady=5)
        self.game_over_score_label.config(text='You Scored: ' + str(self.player.score), font=("Helvetica", 16))
        self.game_over_high_score_label.pack(pady=(5, 20))
        self.game_over_high_score_label.config(text='High Score: ' + str(self.player.high_score), font=("Helvetica", 16))
        self.play_again_btn.pack(pady=(5))
        self.back_btn.pack(pady=5)

        # Hide the main game canvas
        self.canvas.pack_forget()

        self.player.update_stats()
        self.canvas.update_idletasks()

        # Update Variables
        self.round = 1
        self.player.score = 0
    
    def pause_game(self, event):
        self.paused = True
        self.player.moveable = False
        self.show_popup()
    
    def unpause_game(self):
        self.popupwindow.destroy()
        self.paused = False
        self.player.moveable = True
        self.move_vehicles()

    def boss_key(self, event):
        # If game is running and they press tab
        if not self.paused:
            # Pause game and open fake image
            self.paused = True
            self.player.moveable = False
            self.hide_stats()

            # Load work image and assign it so it can be hidden when tab is pressed again
            self.work_image = show_work_image(self.canvas)

            self.window.title("CONFIDENTIAL INFORMATION - LOOK AWAY!")
            return
        # To unpause the game and remove the work image
        self.canvas.delete(self.work_image)
        self.window.title("Crossy Road")
        self.unpause_game()
        self.show_stats()

    def play_again(self):
        self.hide_all_text()
        self.canvas.pack()
        self.reset_game_settings()
        remove_save_file(self.player.name)
        self.start_round()

    # Start the game when user enters name
    def play(self):
        name = self.name_entry.get()
        if len(name) < 3:
            self.error_label.config(text="Enter username (min. 3)")
            return
        
        # close the popup window
        self.popupwindow.destroy()
        self.hide_all_text()

        print("Start game")

        # Create and spawn player
        self.player = Player(name, self.canvas, None)
        self.player.spawn_player(WINDOW_WIDTH / 2, WINDOW_HEIGHT - road_height / 2)

        # Since new game, delete any old saves
        remove_save_file(self.player.name)

        self.reset_game_settings()
        self.show_stats()
        self.spawn_vehicles()
        self.move_vehicles()
        self.set_key_bindings() 

    def create_game(self):
        # Write default keybinds to settings file
        self.reset_key_bindings()

        self.generate_new_map()

        self.show_popup()
        self.popupwindow.mainloop()

    def save_game(self):
        if not self.player:
            return
        save = Save(self.canvas, name=self.player.name, curr_round=self.round, curr_score=self.player.score)
        save.save_game()
        self.popupwindow.destroy()
        self.game_over()
        self.back()

    # Load save from start menu
    def load_game(self):
        name = self.name_entry.get()
        if len(name) < 3:
            self.error_label.config(text="Enter username (min. 3)")
            return
        
        # Check if file path exists and stops if it doesn't
        file_path = "saves/{}_save.json".format(name)
        if not os.path.exists(file_path):
            self.error_label.config(text="No Load file for {}".format(name))
            return False
        
        # close the popup window
        self.popupwindow.destroy()
        self.hide_all_text()

        # Delete pre-drawn obstacles, cars and coins
        self.canvas.delete("all")

        print("Load saved game")

        # Re-draw background with all the objetcs/sprites in their saved positions
        draw_game_background(self.canvas)
        
        save = Save(self.canvas, name, None, None)
        
        saved_player, saved_round = save.load_game(file_path)
        self.player = saved_player

        self.round = saved_round
        self.reset_game_settings()

        self.show_stats()
        self.spawn_vehicles()
        self.move_vehicles()
        self.set_key_bindings() 

    def reset_game_settings(self):
        self.game_running = True
        self.paused = False
        self.player.moveable = True
        self.car_stopped = False
        self.multiplier = 1

    def change_key_binding(self, action, key):
        key_bindings = read_keybinds("keybinds.txt")
        old_key = key_bindings[action]
        if old_key:
            self.window.unbind(f"<{old_key}>")                      # unbind old key
        update_keybind(action, key)

        if not self.player:
            return
        
        function_map = {
            'Left': self.player.move_left,
            'Right': self.player.move_right,
            'Up': self.player.move_up,
            'Down': self.player.move_down,
            'Pause': self.pause_game,
            'Boss': self.boss_key
        }
        action = function_map[action]
        self.window.bind(f"<{key}>", action)                   # set key to corresponding method

    # Set default bindings to arrow keys
    def set_key_bindings(self):
        key_bindings = read_keybinds("keybinds.txt")

        for action, key in key_bindings.items():
            self.change_key_binding(action, key)          

    def reset_key_bindings(self):
        for action, key in default_binds.items():
            update_keybind(action, key)

        self.set_key_bindings()

""" ---------------------------------------Main Code--------------------------------------------- """

window = Tk()

configure_window(WINDOW_WIDTH, WINDOW_HEIGHT)

new_game = Game(window)
new_game.create_game()

window.mainloop()