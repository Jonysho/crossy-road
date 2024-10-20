from helper import *

class Player():
    def __init__(self, name, canvas, sprite_id, score=0):
        self.canvas = canvas
        self.name = name
        self.sprite_id = sprite_id
        self.speed = 20
        self.moveable = False
        self.score = score  # Default to 0
        self.invincible = False
        
        self.high_score = 0
        self.set_high_score()
    
    # Create a player and spawn player object
    def spawn_player(self, x, y):
        sprite_image = Image.open("person.png")
        # Calculate the width based on the target height and the original aspect ratio
        width, height = sprite_image.size
        aspect_ratio = width / height
        target_width = int(PLAYER_SIZE * aspect_ratio)

        sprite_image = sprite_image.resize((target_width, PLAYER_SIZE), Image.LANCZOS)  # Resize image to match obstacle size
        sprite = ImageTk.PhotoImage(sprite_image)
        images.append(sprite)
        self.sprite_id = self.canvas.create_image(x, y, image=sprite, tags=("player", self.name))

    def set_high_score(self):
        leaderboard = read_leaderboard("leaderboard.txt")
        
        if self.name in leaderboard:
            self.high_score = leaderboard[self.name]
    
    # Update player stats
    def update_stats(self):
        self.high_score = max(self.high_score, self.score)
        update_leaderboard(self.name, self.high_score)
        
    # Movement Functions
    def move_left(self, event):
        if self.moveable and not self.handle_out_of_bounds(-self.speed, 0):
            self.handle_obstacle_collision(-self.speed, 0)

    def move_right(self, event):
        if self.moveable and not self.handle_out_of_bounds(self.speed, 0):
            self.handle_obstacle_collision(self.speed, 0)

    def move_up(self, event):
        if self.moveable and not self.handle_out_of_bounds(0, -self.speed):
            self.handle_obstacle_collision(0, -self.speed)

    def move_down(self, event):
        if self.moveable and not self.handle_out_of_bounds(0, self.speed):
            self.handle_obstacle_collision(0, self.speed)

    def check_collision(self, player_coords, obs_coords):
        return (
            player_coords[0] < obs_coords[2] and  # player's left is left of obstacle's right
            player_coords[2] > obs_coords[0] and  # player's right is right of obstacle's left
            player_coords[1] < obs_coords[3] and  # player's top is above obstacle's bottom
            player_coords[3] > obs_coords[1]      # player's bottom is below obstacle's top
        )
    
    def handle_obstacle_collision(self, dx, dy):
        # [x1, y1, x2, y2] - [left, top, right, bottom]
        player_coords = list(self.canvas.bbox(self.sprite_id))
        
        player_coords[0] += dx
        player_coords[2] += dx
        player_coords[1] += dy
        player_coords[3] += dy
        
        if not self.invincible: 
            for obstacle in self.canvas.find_withtag("obstacle"):
                obstacle_coords = self.canvas.bbox(obstacle)
                # Moving Left - collision if player's left overlaps obstacle's right
                if dx < 0 and self.check_collision(player_coords, obstacle_coords):
                    left = player_coords[0] - obstacle_coords[2]
                    # Move left to obstacle's right boundary 
                    self.canvas.move(self.sprite_id, dx - left, dy)
                    return            
                    
                # Moving Right - collisiion if player's right overlaps obstacle's left
                elif dx > 0 and self.check_collision(player_coords, obstacle_coords):
                    right = player_coords[2] - obstacle_coords[0]
                    # Move right to obstacle's left boundary 
                    self.canvas.move(self.sprite_id, dx - right, dy)
                    return   
                    
                # Moving Up - collisiion if player's top overlaps obstacle's bottom
                elif dy < 0 and self.check_collision(player_coords, obstacle_coords):
                    up = player_coords[1] - obstacle_coords[3]
                    # Move up to obstacle's bottom boundary 
                    self.canvas.move(self.sprite_id, dx, dy - up)
                    return   
                    
                # Moving Down - collisiion if player's bottom overlaps obstacle's top
                elif dy > 0 and self.check_collision(player_coords, obstacle_coords):
                    down = player_coords[3] - obstacle_coords[1]
                    # Move down to obstacle's top boundary 
                    self.canvas.move(self.sprite_id, dx, dy - down)
                    return
                
        # Doesnt collide so no need to change distance moved
        self.canvas.move(self.sprite_id, dx, dy)

    # Prevent user from going out of bounds
    def handle_out_of_bounds(self, dx, dy):
        player_coords = self.canvas.coords(self.sprite_id)

        # Left
        if player_coords[0] + dx < 0:
            self.canvas.coords(self.sprite_id, WINDOW_WIDTH + player_coords[0] + dx, player_coords[1])
            return True

        # Right
        if player_coords[0] + dx > WINDOW_WIDTH:
            self.canvas.coords(self.sprite_id, player_coords[0] + dx - WINDOW_WIDTH, player_coords[1])
            return True

        # Up
        if player_coords[1] + dy < 0:
            self.canvas.coords(self.sprite_id, player_coords[0], 0)
            return True
        
        # Down
        if player_coords[1] + dy > WINDOW_HEIGHT:
            self.canvas.coords(self.sprite_id, player_coords[0], WINDOW_HEIGHT)
            return True
        
        # Not out of bounds
        return False