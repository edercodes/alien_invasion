import sys ### this is my own code

import pygame ### imports pygame from terminal installation

from settings import Settings ### imports Settings module for adjustments to game
from ship import Ship ### imports Ship module with additional settings
from bullet import Bullet ### imports Bullet module with adjustments
from alien import Alien ### imports alien image to game module


class AlienInvasion:
    """Overall class to manage game assets and bahavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) ### adjusted settings to allow full screen mode
        self.settings.screen_width = self.screen.get_rect().width ### fullscreen mode allows for faster speeds on MacOS
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("AlienInvasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group() ### groups is used to draw bullets to screen and store used bullets
        self.aliens = pygame.sprite.Group() ### group is created to hold all aliens

        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update() ### ship updates in response to player input and processed before screen is updated
            self._update_bullets()
            self._update_aliens()
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
        elif event.key == pygame.K_SPACE:
            self._fire_bullet() ### calls to fire bullets on screen when spacebnar is pressed

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update() ### updates for each bullet placed in the group

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy(): ### copy method allows for bullet modifications inside the loop
            if bullet.rect.bottom <= 0: ### checks to see if bullet has disappeared from the screen
                self.bullets.remove(bullet) ### removed from bullets if it disappears

        # Check for any bullets that have hit aliens.
        #   If so, get rid of the bullet and the alien. ### this code compares the positions of all bullets in self.bullets and aliens in self.aliens
        collisions = pygame.sprite.groupcollide( ### when the rects of a bullet and an alien overlap, groupcollide() sends a key-value pair to the dictionary it returns### this code compares the positions of all bullets in self.bullets and aliens in self.aliens
                self.bullets, self.aliens, True, True) ### the True statements

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
            then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self) ### creates an alien before performing calculations
        alien_width, alien_height = alien.rect.size ### using size attribute to contain width and height of a rect object
        available_space_x = self.settings.screen_width - (2 * alien_width) ### calculates horizontal space and space available for # of aliens
        number_aliens_x = available_space_x // (2 * alien_width)

        # Detemine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height) ### calulcation space_y_ cald immediate after previous calc
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows): ### use two nested loops to create multiple rows, inner loop creates the aliens in one row, outer loop counts from 0 to number of rows we want
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self): ### this action loops through the fleet
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites(): ### calls check_edges on each alien
            if alien.check_edges():
                self._change_fleet_direction() ### if true, the alien is at an edge and whole fleet needs to change direction
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed ### in this definition, the call loops through all the aliens and drops each one using self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
