
import pygame
from game import Game

screen_width = 800
screen_height = 576

green = (0, 255, 0)


def main():
    # Initialize all imported pygame modules
    pygame.init()
    # Set the width and height of the screen [width, height]
    screen = pygame.display.set_mode((screen_width, screen_height))
    # Set the current window caption
    pygame.display.set_caption("Senior Proj - Pacman")
    # Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Create a game object
    game = Game()
    # -------- Main Program Loop -----------
    while not done:
        # --- Process events (keystrokes, mouse clicks, etc)
        done = game.process_events(screen)
        # --- Game logic should go here
        game.run_logic(screen)
        # --- Draw the current frame
        game.display_frame(screen)

        # --- Limit to 60 frames per second
        clock.tick(50)
    pygame.quit()


if __name__ == '__main__':
    main()
