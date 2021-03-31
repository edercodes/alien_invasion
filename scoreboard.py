import pygame.font

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):    ### ai_game parameter allows access to settings, screen, and stat objects to report values being tracked
        """Initialze scorekeeping attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial image.
        self.prep_score()   ### turns text to be displayed into an image

    def prep_score(self):
        """Turn the score into a rendered image."""
        score_str = str(self.stats.score)   ### turns numerical value stats.score into a string
        self.score_image = self.font.render(score_str, True,    ### string is passed to a render, which creates the image
                self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)