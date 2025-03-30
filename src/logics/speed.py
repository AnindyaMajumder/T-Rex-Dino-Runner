import time

class GameSpeed:
    def __init__(self):
        self.base_speed = 2.0  # Starting speed (pixels per frame)
        self.current_speed = self.base_speed
        self.max_speed = 10.0  # Maximum speed cap
        self.acceleration_rate = 0.05  # Speed increase per second
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.elapsed_time = 0
        self.score = 0
        self.score_multiplier = 0.05  # Score increment per frame
        
    def update(self, delta_time):
        """Update game speed based on elapsed time"""
        current_time = time.time()
        self.elapsed_time = current_time - self.start_time
        frame_time = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Gradually increase speed based on elapsed time
        # The speed will grow faster at the beginning and slow down as it approaches max_speed
        time_factor = min(self.elapsed_time / 60.0, 1.0)  # Cap at 60 seconds
        self.current_speed = self.base_speed + (self.max_speed - self.base_speed) * time_factor
        
        # Alternative: Linear acceleration
        # self.current_speed += self.acceleration_rate * frame_time
        # self.current_speed = min(self.current_speed, self.max_speed)
        
        # Increase score based on speed
        self.score += self.current_speed * self.score_multiplier
        
        return self.current_speed
    
    def get_speed(self):
        """Return the current game speed"""
        return self.current_speed
    
    def get_score(self):
        """Return the current score"""
        return int(self.score)
    
    def reset(self):
        """Reset the game speed and timer"""
        self.current_speed = self.base_speed
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.elapsed_time = 0
        self.score = 0