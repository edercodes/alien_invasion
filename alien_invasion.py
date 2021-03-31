import sys
from time import sleep

import pygame ### imports pygame from terminal installation

from settings import Settings ### imports Settings module for adjustments to game
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
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

        # Create an instance to store game statistics,
        #   and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group() ### groups is used to draw bullets to screen and store used bullets
        self.aliens = pygame.sprite.Group() ### group is created to hold all aliens

        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play") ### creates the instance of Button with the label Play but doesn't draw button to screen

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
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
            elif event.type == pygame.MOUSEBUTTONDOWN: ### detected any time player clicks anywhere on screen
                mouse_pos = pygame.mouse.get_pos() ### returns tuple of mouse cursor's x and y corrdinates
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos) ### contains True or False value and will only restart if PLay is clicked and game is not currently active
        if button_clicked and not self.stats.game_active():
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

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

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):  ### compares positions of all bullets in self.bullets and aliens in self.aliens and removes them
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide( ### when the rects of a bullet and an alien overlap, groupcollide() sends a key-value pair to the dictionary it returns### this code compares the positions of all bullets in self.bullets and aliens in self.aliens
                self.bullets, self.aliens, True, True) ### the True statements

        if collisions:
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()

        if not self.aliens: ### checks whether aliens group is empty
            # Destroy existing bullets and create new fleet.
            self.bullets.empty() ### empty() method removes all remaining sprites(bullets) from the group
            self._create_fleet() ### this call fills the screen with aliens again
            self.settings.increase_speed() ### increased game tempo by using this call in this function when last alien is shot down

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
            then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions. ### function below loops through the group aliens and returns the first alien it finds that has collided with ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens): ### if no collisions occur, functions returns None and if block does not execute
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0: ### moved existing code into an if block, which tests for at least one ship remaining
            # Decrement ships_left.
            self.stats.ships_left -= 1 ### number of ships left is 1 after this process

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5) ### pauses program executions for a half second, enough for player to see collision
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

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

        # Daraw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
