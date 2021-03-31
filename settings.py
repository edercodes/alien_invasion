class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 1.5 ### ship speed adjusted to 1.5 pixels on each pass through the loop
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10 ### controls how quickly fleet drops down each time an alien reaches the edge of the screen
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1 ### use of numbers instead of elif statements because there are only two directions to work with x and y coordinates

        # How quickly the game speeds up
        self.speedup_scale = 1.1 ### controls how quickly the game speeds up; 2 would double game speed and 1 would be constant

        self.initialize_dynamic_settings() ### intializes the values for attributes that need to change throughout game

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1 ### included so aliens know to go right at game start

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale ### multiplying each speed setting to increase speed of these elements
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale