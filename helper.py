import random
from PIL import Image, ImageTk
import os 

WINDOW_WIDTH=1280
WINDOW_HEIGHT=720
POPUP_WINDOW_WIDTH=350
POPUP_WINDOW_HEIGHT=300
GRASS_COLOR="#37c84c"
NUMBER_OF_ROADS=4
VEHICLE_SIZE=40
PLAYER_SIZE=30
COIN_SIZE=15
OBSTACLE_SIZE=40
END_COIN_SIZE=30
BASE_DELAY=50


# Ratio of 2 land : 1 road 
height_ratio = WINDOW_HEIGHT / ((NUMBER_OF_ROADS+1) * 2 + NUMBER_OF_ROADS * 1)

# Four horizontal roads
road_height = height_ratio
space_between_roads = 2*height_ratio

default_binds = {
    'Left': 'Left',
    'Right': 'Right',
    'Up': 'Up',
    'Down': 'Down',
    'Pause': 'Escape',
    'Boss': 'Tab'
}

""" ---------------------------------------Useful functions--------------------------------------------- """
def draw_game_background(canvas):
    # Green background
    canvas.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill=GRASS_COLOR, outline=GRASS_COLOR)

    for i in range(NUMBER_OF_ROADS):
        y = space_between_roads + i * (road_height + space_between_roads)

        # Create Road
        canvas.create_rectangle(0, y, WINDOW_WIDTH, y + road_height, fill="#000000", outline="#000000")

        # # White striped road markings
        strip_width = 50
        # 1 : 1 - road : marking
        num_stripes = WINDOW_WIDTH // (2*strip_width)
        random_width_offset = random.uniform(0, strip_width/2)
        for j in range(1, (num_stripes+1) * 2, 2):
            x1 = strip_width*j - random_width_offset
            x2 = strip_width*(j+1) - random_width_offset
            road_height_ratio = road_height / 14
            y1 = road_height_ratio * 7 + y
            y2 = road_height_ratio * 8 + y
            canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="white")

images = []
def spawn_obstacle(canvas, x, y):
    imagePath = "tree.png"
    tree_image = Image.open(imagePath)
    # Calculate the width based on the target height and the original aspect ratio
    width, height = tree_image.size
    aspect_ratio = width / height
    target_width = int(OBSTACLE_SIZE * aspect_ratio)

    tree_image = tree_image.resize((target_width, OBSTACLE_SIZE), Image.LANCZOS)  # Resize image to match obstacle size
    tree_photo = ImageTk.PhotoImage(tree_image)
    images.append(tree_photo)
    canvas.create_image(x, y, image=tree_photo, tag="obstacle")

# Draw random trees/obstacles on grass 
def spawn_obstacles(canvas, round):
    for i in range(NUMBER_OF_ROADS - 1):
        obstacle_multiplier = round // 5 # Increase range by 1 every 5 rounds
        for _ in range(random.randint(4 + obstacle_multiplier , 8 + obstacle_multiplier)):
            y = space_between_roads + i * (road_height + space_between_roads) + road_height/2 + random.uniform(-road_height/2, road_height/2) # Height of grass row

            # Create obstacle
            x = random.randint(OBSTACLE_SIZE, WINDOW_WIDTH - OBSTACLE_SIZE)
            spawn_obstacle(canvas, x, y + road_height)

def spawn_end_coin(canvas, x, y):
    canvas.create_oval(x, y, x + END_COIN_SIZE, y + END_COIN_SIZE, fill="yellow", tag="end_coin")

def spawn_coin(canvas, x, y):
    canvas.create_oval(x, y + COIN_SIZE, x + COIN_SIZE, y + COIN_SIZE * 2, fill="#ffe64d", outline="#ffdb00", tag="coin")

def spawn_starting_vehicles_and_coins(spawn_vehicle, canvas):
    for i in range(NUMBER_OF_ROADS):
        number_of_vehicles_to_spawn = random.randint(3, 5)
        positions = generate_random_positions(number_of_vehicles_to_spawn, WINDOW_WIDTH, VEHICLE_SIZE)
        y = space_between_roads + i * (road_height + space_between_roads) # Height of road
        spawn_coin(canvas, random.uniform(COIN_SIZE, WINDOW_WIDTH - COIN_SIZE), y)
        for j in range(number_of_vehicles_to_spawn):
            # If is odd: vehicles move left -> right || i is even: vehicles move right -> left
            isEven = i%2==0
            spawn_vehicle(positions[j], y, "rightToLeft" if isEven else "leftToRight") 

def show_work_image(canvas):
    # Load work image and get dimensions
    work_image = Image.open('spreadsheet.webp')
    work_image = work_image.resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.LANCZOS)
    work_image = ImageTk.PhotoImage(work_image)
    images.append(work_image)

    img_id = canvas.create_image(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, image=work_image)
    return img_id

def generate_random_positions(number_of_vehicles, length, vehicle_width):
    # Ensure there is enough space for all objects
    if number_of_vehicles * vehicle_width > length:
        raise ValueError("Not enough space for the given number of objects.")

    # Store the positions of the vehicles
    positions = []

    # Generate random positions without overlapping
    for _ in range(number_of_vehicles):
        # Generate a random position within the available space
        position = random.uniform(vehicle_width, length - vehicle_width * 2)

        # Check for overlaps with existing positions
        while any(
            existing_position <= position <= existing_position + 2 * vehicle_width or
            position <= existing_position <= position + 2 * vehicle_width
            for existing_position in positions
        ):
            position = random.uniform(vehicle_width, length - vehicle_width * 2)

        # Add the position to the list
        positions.append(position)

    return positions

def read_keybinds(file_path):
    keybinds = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(':')
            keybinds[key.strip()] = value.strip()
    return keybinds

def update_keybind(action, new_keybind):
    file = "keybinds.txt"
    keybinds = read_keybinds(file)
    keybinds[action] = new_keybind
    
    with open(file, 'w') as file:
        for action, keybind in keybinds.items():
            file.write(f"{action}: {keybind}\n")

def read_leaderboard(file_path):
    leaderboard = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(':')
            leaderboard[key.strip()] = int(value.strip())
    return leaderboard

def update_leaderboard(name, score):
    file = "leaderboard.txt"
    leaderboard = read_leaderboard(file)
    leaderboard[name] = score
    new_leaderboard = list(leaderboard.items())
    new_leaderboard.sort(key=lambda x: x[1], reverse=True)
    with open(file, 'w') as file:
        for name, score in new_leaderboard:
            file.write(f"{name}: {score}\n")

def remove_save_file(name):
    file_path = "saves/{}_save.json".format(name)
    if os.path.exists(file_path):
        os.remove(file_path)