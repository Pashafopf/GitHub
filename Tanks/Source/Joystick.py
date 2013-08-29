import pygame
class JoyStick:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

        pygame.init()



    # -------- Main Program Loop -----------
    while done==False:
        # EVENT PROCESSING STEP
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop

            # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")


        # Get count of joysticks
        joystick_count = pygame.joystick.get_count()

        joysick.print(screen, "Number of joysticks: {}".format(joystick_count) )
        joysick.indent()

        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            joysick.print(screen, "Joystick {}".format(i) )
            joysick.indent()

            # Get the name from the OS for the controller/joystick
            name = joystick.get_name()
            joysick.print(screen, "Joystick name: {}".format(name) )

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other.
            axes = joystick.get_numaxes()
            joysick.print(screen, "Number of axes: {}".format(axes) )
            joysick.indent()

            for i in range( axes ):
                axis = joystick.get_axis( i )
                joysick.print(screen, "Axis {} value: {:>6.3f}".format(i, axis) )
            joysick.unindent()

            buttons = joystick.get_numbuttons()
            joysick.print(screen, "Number of buttons: {}".format(buttons) )
            joysick.indent()

            for i in range( buttons ):
                button = joystick.get_button( i )
                joysick.print(screen, "Button {:>2} value: {}".format(i,button) )
            joysick.unindent()

            # Hat switch. All or nothing for direction, not like joysticks.
            # Value comes back in an array.
            hats = joystick.get_numhats()
            joysick.print(screen, "Number of hats: {}".format(hats) )
            joysick.indent()

            for i in range( hats ):
                hat = joystick.get_hat( i )
                joysick.print(screen, "Hat {} value: {}".format(i, str(hat)) )
            joysick.unindent()

            joysick.unindent()


        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 20 frames per second
        clock.tick(20)

        # Close the window and quit.
        # If you forget this line, the program will 'hang'
        # on exit if running from IDLE.
        pygame.quit ()



    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, (0,0,0))
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


