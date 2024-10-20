import os
import random
from PIL import Image, ImageTk
from helper import VEHICLE_SIZE

vehicles = [] # Just so the image of vehicle is not garbage collected 
class Vehicle():
    def __init__(self, canvas, x, y, direction):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.direction = direction
        self.image_path = self.choose_vehicle()
    
    # Gets a random vehicle image path from the folder vehicles based on self.direction
    def choose_vehicle(self):
        path = "vehicles"
        
        # Get a list of all files in the folder
        all_files = os.listdir(path)

        # Filter the list to include only image files (you may customize this based on your image file extensions)
        image_files = []
        direction = "left" if self.direction == 'rightToLeft' else "right"
        for file in all_files:
            file = file.lower()
            if file.endswith(('.png', '.jpg', '.jpeg')) and direction in file:
                image_files.append(file)

        # Check if there are any image files in the folder
        if not image_files:
            return None

        random_image = random.choice(image_files)
        return os.path.join(path, random_image)
    
    def spawn(self):
        vehicle_image = Image.open(self.image_path)

        # Calculate the width based on the target height and the original aspect ratio
        width, height = vehicle_image.size
        aspect_ratio = width / height
        target_width = int(VEHICLE_SIZE * aspect_ratio)

        vehicle_image = vehicle_image.resize((target_width, VEHICLE_SIZE), Image.LANCZOS)  # Resize image to match obstacle size
        vehicle_photo = ImageTk.PhotoImage(vehicle_image)
        vehicles.append(vehicle_photo)
        self.canvas.create_image(self.x, self.y + 10, image=vehicle_photo, tags=(self.direction, self.image_path))

    