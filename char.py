import pygame

class Char:
    """A class to manage the Pokemon."""

    def __init__(self, ai_game):
        """Initialize the Charizard and set its starting position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load the Charizard image and get its rect.
        self.image = pygame.image.load('images/char.bmp')
        self.rect = self.image.get_rect()

        # Start each new Charizard at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Draw the Charizard at its current location."""
        self.screen.blit(self.image, self.rect)