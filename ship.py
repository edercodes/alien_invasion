import pygame

class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship imafe and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x) ### adding decimal values to keep ship movement accurate

        # Movement flags
        self.moving_right = False ### this flag keeps the ship motionless unless the right arroy key is pressed
        self.moving_left = False ### flag for left direction movement

    def update(self): ### checks status of moveing_right flag is changed
        """Update the ship's position based on the movement flags."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right: ### moves the ship right if flag is true ### adds a conditional layer to detect edge of the screen
            self.x += self.settings.ship_speed ### adjustment to speed made by amount stored in settings
        if self.moving_left and self.rect.left > 0: ### using two if statements allows for accurate movement when switching from right to left
            self.x -= self.settings.ship_speed ### an elif statement would've given the right arrow key priority

        # Update rect object from self.x.
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)