class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 1.5 ### ship speed adjusted to 1.5 pixels on each pass through the loop

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10 ### controls how quickly fleet drops down each time an alien reaches the edge of the screen
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1 ### use of numbers instead of elif statements because there are only two directions to work with x and y coordinates