from player import Player
from enemies import *

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

pygame.init()
screen_width = 800
screen_height = 576

# empty array for the scores
new_content_array = [0, 0, 0]

# below is the timer functionality
frame_count = 0
frame_rate = 60
start_time = 90
timerfont = pygame.font.Font('freesansbold.ttf', 32)


# deals with the win screen mostly
clock = pygame.time.Clock()

class Game(object):
    def __init__(self):
        self.font = pygame.font.Font(None, 40)
        self.finalScoreScreen = False
        self.about = False
        self.gameWonScreen = False
        self.powerupCollected = False
        self.game_over = True
        self.game_won = False

        # Create the variable for the score
        self.score = 0
        self.secondBest = 0
        self.worst_score = 0
        # should be 156
        self.dotsRemaining = 156
        self.timer = 200

        # Create the font for displaying the score on the screen
        self.font = pygame.font.Font(None, 35)
        # Create the menu of the game
        self.menu = Menu(("Start", "About", "Scores", "Exit", "Win Screen"), font_color=WHITE, font_size=60)
        # Create the player
        self.player = Player(32, 128, "player.png")
        # Create the blocks that will set the paths where the player can go
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()
        # Create a group for the dots on the screen
        self.dots_group = pygame.sprite.Group()
        # Set the environment:
        for i, row in enumerate(environment()):
            for j, item in enumerate(row):
                if item == 1:
                    self.horizontal_blocks.add(Block(j * 32 + 8, i * 32 + 8, BLACK, 16, 16))
                elif item == 2:
                    self.vertical_blocks.add(Block(j * 32 + 8, i * 32 + 8, BLACK, 16, 16))
        # Create the enemies
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Slime(288, 96, 0, 2))
        self.enemies.add(Slime(288, 320, 0, -2))
        self.enemies.add(Slime(544, 128, 0, 2))
        # print("Enemies g: " + str(self.enemies))

        for i, row in enumerate(environment()):
            for j, item in enumerate(row):
                if item != 0:
                    self.dots_group.add(Ellipse(j * 32 + 12, i * 32 + 12, WHITE, 8, 8))

        # ADDING POWER UPS
        # power ups have 0, 0 because change in x and y is 0
        # they will never move
        # creates powerups group from class
        self.powerups = pygame.sprite.Group()
        # puts powerups at a certain location
        self.powerups.add(Powerup(288, 310, 0, 0))
        self.powerups.add(Powerup(544, 64, 0, 0))

        # Load the sound effects
        self.pacman_sound = pygame.mixer.Sound("pacman_sound.ogg")
        self.game_over_sound = pygame.mixer.Sound("game_over_sound.ogg")

    def process_events(self, screen):
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                return True
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_over:
                        if self.menu.state == 0:
                            # ---- START ------
                            self.__init__()
                            self.dotsRemaining = 156
                            self.game_over = False
                            self.game_won = False

                        elif self.menu.state == 1:
                            # --- ABOUT ------
                            self.about = True

                        elif self.menu.state == 2:
                            # display final score screen
                            self.finalScoreScreen = True

                        elif self.menu.state == 3:
                            # --- EXIT -------
                            # User clicked exit
                            return True

                        if self.menu.state == 4:
                            # win screen
                            self.gameWonScreen = True

                    if self.game_won:
                        if self.menu.state == 0:
                            # ---- START ------
                            self.__init__()
                            self.dotsRemaining = 156
                            self.game_over = False
                            self.game_won = False
                            # both of these are True
                            # print("game won boolean: " + str(self.game_won))
                            # print("game over boolean: " + str(self.game_over))

                        elif self.menu.state == 1:
                            # --- ABOUT ------
                            self.about = True

                        elif self.menu.state == 2:
                            # display final score screen
                            self.finalScoreScreen = True

                        elif self.menu.state == 3:
                            # --- EXIT -------
                            # User clicked exit
                            return True

                        if self.menu.state == 4:
                            # win screen
                            self.gameWonScreen = True

                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()

                elif event.key == pygame.K_LEFT:
                    self.player.move_left()

                elif event.key == pygame.K_UP:
                    self.player.move_up()

                elif event.key == pygame.K_DOWN:
                    self.player.move_down()

                elif event.key == pygame.K_ESCAPE:
                    # gets out of all of these screens and to the main menu
                    self.game_over = True
                    self.about = False
                    self.finalScoreScreen = False
                    self.gameWonScreen = False

                elif event.key == pygame.K_s and self.gameWonScreen:
                    self.game_won = False
                    self.game_over = True
                    self.gameWonScreen = False
                    self.menu.display_frame(screen)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.stop_move_left()
                elif event.key == pygame.K_UP:
                    self.player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.stop_move_down()

            # delete this later?
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.explosion = True

        return False

    def run_logic(self, screen):
        global frame_count
        if not self.game_over:
            self.player.update(self.horizontal_blocks, self.vertical_blocks)
            block_hit_list = pygame.sprite.spritecollide(self.player, self.dots_group, True)
            # When the block_hit_list contains one sprite that means that player hit a dot
            if len(block_hit_list) > 0:
                # Here will be the sound effect
                self.pacman_sound.play()
                self.score += 1
                self.dotsRemaining -= 1
                # check to see how many dots remain, if none - game over!
                if self.dotsRemaining == 0:
                    self.player.explosion = True
                    self.game_won = self.player.game_won
                    self.game_won = True
                    if self.game_won:
                        # go to game won screen
                        self.game_over = True
                        self.gameWonScreen = True
                        if self.gameWonScreen:
                            display_surface = pygame.display.set_mode((screen_width, screen_height))
                            font = pygame.font.Font('freesansbold.ttf', 32)
                            winMessage = font.render("Congrats! You win! ", True, green)
                            display_surface.blit(winMessage, [275, 90])

            # changes the block hit list to be the sprite colliding with the enemy
            # if that is true, then the game is over
            block_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, True)
            if len(block_hit_list) > 0 and not self.powerupCollected:
                self.player.explosion = True
                self.game_over_sound.play()
                self.game_over = self.player.game_over

            if len(block_hit_list) > 0 and not self.powerupCollected:
                self.score += 200

            # sprite colliding with the powerup
            block_hit_list = pygame.sprite.spritecollide(self.player, self.powerups, True)

            # POWERUP FUNCTIONALITY BELOW
            # if pacman collides with the powerup
            if len(block_hit_list) > 0:
                self.timer = 200  # number of seconds the powerup lasts
                self.pacman_sound.play()  # get a different sound for when a powerup is picked up later
                self.score += 200   # increase the score by 200 points for each powerup that is picked up
                # power up has been picked up!
                self.powerupCollected = True
                # print("Pacman collided with powerup: " + str(block_hit_list))
            if self.powerupCollected:
                # makes blue lines turn to red to user knows powerup is active
                draw_environmentActive(screen)
                # power up active for user in console
                # print("Power up active!")
                self.timer -= 1
                # print("timer: " + str(self.timer))

                # if power up is over
                if self.timer <= 0:
                    self.powerupCollected = False
                    # print("Power up now over")


        pygame.display.update()
        self.enemies.update(self.horizontal_blocks, self.vertical_blocks)  # updates where the enemies are moving

    def updateScore(self, score, secondBest, worst_score):
        # newcontentarray is declared at the beginning of the file.
        # accessed by global because the score screen also grabs from this same array
        # to display score
        global new_content_array
        # print("current session score str: " + str(score))    # test line
        # print("second best score 1st run: " + str(self.secondBest))
        last = int(new_content_array[0])  # gets first line of file
        self.secondBest = int(new_content_array[1])  # gets the second line of the file
        self.worst_score = int(new_content_array[2])  # gets the worst score (aka last line) of file
        # print("old score " + str(last))  # test line

        if (int(score) < last) & (int(score) < self.secondBest):
            # everything remains the same.
            # the score is the smallest value so it would go at the end
            # print("worst score = " + str(self.worst_score))
            new_content_array[2] = int(score)
            if int(score) < self.worst_score:
                new_content_array[2] = self.worst_score

        if (int(score) > self.secondBest) & (int(score) > last):
            # score is the best score
            new_content_array[0] = score
            # last is the second best
            new_content_array[1] = last
            # second best becomes the third best/aka worst best
            self.worst_score = self.secondBest
            new_content_array[2] = self.worst_score
            # print("int(score) > self.secondBest) & (int(score) > last: " + str(new_content_array))

            # if the current score is less than the best score but higher than
            # the second best score
        if (int(score) < last) & (int(score) > self.secondBest):
            # print("CURRENT WORST SCORE: " + str(self.worst_score))
            #  last is still the best score
            new_content_array[0] = last
            self.worst_score = self.secondBest
            # sets the current score to the second best
            self.secondBest = int(score)
            # add the second best score to the content_list
            new_content_array[1] = self.secondBest
            # secondbest in this case becomes the 3rd best
            new_content_array[2] = self.worst_score
            print(str(new_content_array))

        if int(score) < last & int(score) < self.secondBest & int(score) > self.worst_score:
            new_content_array[0] = last
            new_content_array[1] = self.secondBest
            # sets new worst score to the current score
            self.worst_score = int(score)
            new_content_array[2] = self.worst_score
            # print("updated array: " + str(new_content_array))

        if last < int(score):  # if the current score is higher than the previous best
            # add score to the first line because it is the best
            new_content_array[0] = score
            # last is now the second score
            self.secondBest = int(last)
            # since last is the second score, it is the second line in the array
            new_content_array[1] = self.secondBest
            new_content_array[2] = self.worst_score

        if (int(score) < last) & (int(score) < self.secondBest) & (int(score) < self.worst_score):
            # if current score is worse than everything
            # all score values are the same, nothing changes
            # score is the worse score in this case
            new_content_array[0] = last
            new_content_array[1] = self.secondBest
            self.worst_score = new_content_array[2]
            new_content_array[2] = self.worst_score

        return last

    def display_frame(self, screen):
        global new_content_array
        # First, clear the screen to black. Don't put other drawing commands
        screen.fill(BLACK)
        # --- Drawing code should go here
        if self.game_over or self.game_won:
            if self.about:
                display_surface = pygame.display.set_mode((screen_width, screen_height))
                font = pygame.font.Font('freesansbold.ttf', 32)
                menutext1 = font.render('Pacman is a game that has a maze with', True, red)
                menutext2 = font.render('enemy ghosts, pac-dots, and powerups', True, red)
                menutext3 = font.render('The ghosts roam the maze trying to defeat', True, red)
                menutext4 = font.render('Pac-Man, who eats ghosts with powerups.', True, red)
                menutext5 = font.render('If any ghosts hit Pac-Man, the game ends.', True, red)
                menutext6 = font.render('When all dots are collected, you win!', True, red)

                # setting up rectangles for the lines of text
                textRect = menutext1.get_rect()
                textRect2 = menutext2.get_rect()
                textRect3 = menutext2.get_rect()
                textRect4 = menutext2.get_rect()
                textRect5 = menutext5.get_rect()
                textRect6 = menutext5.get_rect()

                # set the center of the rectangular object.
                # The width correlates with indentation.
                # The height can't be the same because if it was it would blit over each other
                # values were height were determined just by guess and check
                textRect.center = (screen_width // 2, screen_height // 2.5)
                textRect2.center = (screen_width // 2, screen_height // 2.2)
                textRect3.center = (screen_width // 2, screen_height // 1.9)
                textRect4.center = (screen_width // 2, screen_height // 1.7)
                textRect5.center = (screen_width // 2, screen_height // 1.5)
                textRect6.center = (screen_width // 2, screen_height // 1.35)

                # display rendered text on surface
                display_surface.blit(menutext1, textRect)
                display_surface.blit(menutext2, textRect2)
                display_surface.blit(menutext3, textRect3)
                display_surface.blit(menutext4, textRect4)
                display_surface.blit(menutext5, textRect5)
                display_surface.blit(menutext6, textRect6)
            else:
                # go back to the main menu
                self.menu.display_frame(screen)
                # updates the score when you go back to the main menu, not just
                # when you enter the Score Screen
                self.updateScore(self.score, self.secondBest, self.worst_score)

                if self.finalScoreScreen:
                    # FINAL SCORE CODE NEXT 4 LINES
                    display_surface = pygame.display.set_mode((screen_width, screen_height))
                    font = pygame.font.Font('freesansbold.ttf', 32)
                    finalScoreMessage = font.render("Final Score: " + str(self.score), True, green)
                    display_surface.blit(finalScoreMessage, [275, 20])
                    self.updateScore(self.score, self.secondBest, self.worst_score)

                    # printing the score messages
                    bestScoreMessage = font.render("Best Score: " + str(new_content_array[0]), True, green)
                    # scores will match when the current best has been recently set
                    display_surface.blit(bestScoreMessage, [275, 50])
                    # print("new content array in other loop" + str(new_content_array))
                    secondBestScoreMsg = font.render("Second Best Score: " + str(new_content_array[1]), True, green)
                    display_surface.blit(secondBestScoreMsg, [275, 80])
                    thirdBestScoreMsg = font.render("Third Best Score: " + str(new_content_array[2]), True, green)
                    display_surface.blit(thirdBestScoreMsg, [275, 110])
                else:
                    # go back to the main menu
                    self.menu.display_frame(screen)

        else:
            # --- Draw the game here ---
            self.horizontal_blocks.draw(screen)
            self.vertical_blocks.draw(screen)
            draw_environment(screen)
            self.dots_group.draw(screen)
            self.enemies.draw(screen)
            self.powerups.draw(screen)
            screen.blit(self.player.image, self.player.rect)
            # screen.blit(self.enemies.image, self.enemies)
            # Render the text for the score
            text = self.font.render("Score: " + str(self.score), True, green)
            # Put the text on the screen
            screen.blit(text, [120, 20])

        if self.game_won:
            # go to game won screen
            self.game_over = True
            # self.menu.display_frame(self.gameWonScreen)
            self.gameWonScreen = True
            if self.gameWonScreen:
                display_surface = pygame.display.set_mode((screen_width, screen_height))
                font = pygame.font.Font('freesansbold.ttf', 32)
                winMessage = font.render("Congrats! You win! ", True, green)
                display_surface.blit(winMessage, [250, 210])
                winMessage2 = font.render("Press s to return to menu ", True, green)
                display_surface.blit(winMessage2, [250, 240])
            else:
                # go back to the main menu
                self.menu.display_frame(screen)
                print("TEST")

        # update the screen with what is drawn.
        pygame.display.flip()

    def display_message(self, screen, message, color=(255, 0, 0)):
        label = self.font.render(message, True, color)
        # Get the width and height of the label

        width = label.get_width()
        height = label.get_height()
        # Determine the position of the label
        posX = (screen_width/ 2) - (width / 2)
        posY = (screen_height / 2) - (height / 2)
        # Draw the label onto the screen
        screen.blit(label, (posX, posY))


class Menu(object):
    state = 0

    def __init__(self, items, font_color=(0, 0, 0), select_color=(255, 0, 0), ttf_font=None, font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font, font_size)

    def display_frame(self, screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                label = self.font.render(item, True, self.select_color)
            else:
                label = self.font.render(item, True, self.font_color)

            width = label.get_width()
            height = label.get_height()

            posX = (screen_width / 2) - (width / 2)
            # t_h: total height of text block
            t_h = len(self.items) * height
            posY = (screen_height / 2) - (t_h / 2) + (index * height)

            screen.blit(label, (posX, posY))

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) - 1:
                    self.state += 1