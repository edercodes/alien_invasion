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

        self.screen = pygame.display.set_mode((0, 0), pygame. FULLSCREEN) ### adjusted settings to allow full screen mode
        self.settings.screen_width = self.screen.get_rect().width ### fullscreen mode allows for faster speeds on MacOS
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("AlienInvasion")

        self.ship = Ship(self)


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update() ### ship updates in response to player input and processed before screen is updated
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN: ### responds when Pygame notices KEYDOWN
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP: ### detects KEYUP events by responding to key movements
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT: ### checks what key is pressed
            self.ship.moving_right = True ### detects which direction for ship to move
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()