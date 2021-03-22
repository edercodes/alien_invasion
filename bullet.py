import pygame
from pygame.sprite import Sprite

class Bullet(Sprite): ### using sprites allows for elements to be grouped and be acted on all at once
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__() ### call super to inherit elements from Sprite module in pygame
        self.screen = ai_game.screen
        self.settings =ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, ### uses rect attribute to create the instance of bullets instead of an image
            self.settings.bullet_height) ### gets coordinates from width and height and rearranges according to ship position
        self.rect.midtop = ai_game.ship.rect.midtop ### ensures bullet fired from top of ship

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y) ### decimal value is stored in the bullet's y coordinate to make adjustments to bullet speed

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed ### amount stored in settings.bullet_speed is subtracted from self.y
        # Update the rect position.
        self.rect.y = self.y ### value of self.y is then set to self.rect.y

    def draw_bullet(self): ### call to draw bullet when ready
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect) ### fills color of draw.rect by using colors stored in self.color