import sys ### this is my own code

import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
    """Overall class to manage game assets and bahavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("AlienInvasion")

        self.ship = Ship(self)


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN: ### responds when Pygame notices KEYDOWN
                if event.key == pygame.K_RIGHT: ### checks what key is pressed
                    # Move the ship to the right.
                    self.ship.rect.x += 1 ### tells how far in each direction to move

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()