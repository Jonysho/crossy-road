from tkinter import *
import json
from helper import spawn_coin, spawn_end_coin, spawn_obstacle, draw_game_background
from vehicle import Vehicle
from player import Player
import os

class Save:
    def __init__(self, canvas, name, curr_round, curr_score):
        self.canvas = canvas
        self.save_info = {
            'name': name,
            'curr_round': curr_round,
            'curr_score': curr_score,
            'canvas_state': {}
        }

    # Save the score and round to save.txt
    def save_game(self):
        name = self.save_info["name"]
        # with open("save.json", "r") as f:

        # Get all items on the canvas
        all_items = self.canvas.find_all()

        # Create a dictionary to store item properties
        for item_id in all_items:
            # Get type, coordinates and tags
            coords = self.canvas.coords(item_id)
            tags = self.canvas.gettags(item_id)

            # Store in the dictionary
            if len(tags) > 0:
                self.save_info["canvas_state"][item_id] = {"coords": coords, "tags": tags}
        
        # Save the canvas state to a JSON file
        file_path = "saves/{}_save.json".format(self.save_info["name"])
        with open(file_path, "w") as f:
            json.dump(self.save_info, f)

    def load_game(self, file_path):
        try:
            # Try to open the JSON file and draw items on the canvas
            self.canvas.delete("all")  # Clear the current canvas
            draw_game_background(self.canvas)

            # Load the save info from the JSON file
            with open(file_path, "r") as f:
                self.save_info = json.load(f)

            # Iterate over items in the saved state and draw them on the canvas
            for item_id, properties in self.save_info["canvas_state"].items():
                tags = properties["tags"]
                tags_set = set(tags)
                coords = properties["coords"]
                
                # Draw the item on the canvas
                if "coin" in tags_set:
                    spawn_coin(self.canvas, x=(coords[0]+coords[2])/2, y=(coords[1]+coords[3])/2) 

                elif "end_coin" in tags_set:
                    spawn_end_coin(self.canvas, x=(coords[0]+coords[2])/2, y=(coords[1]+coords[3])/2) 

                elif "obstacle" in tags_set:                    
                    spawn_obstacle(self.canvas, coords[0], coords[1])

                elif "leftToRight" in tags_set or "rightToLeft" in tags_set:
                    vehicle = Vehicle(self.canvas, x=coords[0], y=coords[1], direction=tags[0])
                    vehicle.image_path = tags[1]
                    vehicle.spawn()

                elif "player" in tags_set:
                    player = Player(self.save_info["name"], self.canvas, None, self.save_info["curr_score"])
                    player.spawn_player(coords[0], coords[1])
            
            os.remove(file_path)
            return (player, self.save_info["curr_round"])

        except Exception as e:
            print(f"Error loading canvas state: {e}")