from tkinter import *   # connect the graphic library

# connect the modules that are responsible for time and random numbers
import time
import random

window = Tk()   # create a new object - a window with a game field
window.title('GameBall')  # make a window title - Games using the property of the Title object
window.resizable(None, None)   # prohibit changing the size of the window, for this we use the property of Resizable

# placing our game window above the rest of the windows on the computer so that other windows can not obscure it
window.wm_attributes('-topmost', 1)

# create a new canvas - 400 by 500 pixels, where we will draw the game
canvas = Canvas(window, width=500, height=400, highlightthickness=0)

canvas.pack()   # tell the canvas that each visible element will have its own separate coordinates

window.update()   # update the window with canvas


# describe the class Ball, which will be responsible for the ball
class Ball:

    # designer - it is called at the time of creating a new object based on this class
    def __init__(self, canvas, paddle, score, color):

        # We set the parameters of the object that convey to us in brackets at the time of creation
        self.canvas = canvas
        self.paddle = paddle
        self.score = score

        # color was needed so that we were painted over the whole ball
        # here appears a new property of ID, in which the internal name of the ball is stored
        # and also the Create_oval command, we create a circle with a radius of 15 pixels
        # and paint over the desired color
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)

        # place the ball at a point with coordinates 245,100
        self.canvas.move(self.id, 245, 100)

        # we set a list of possible directions for starting
        starts = [-2, -1, 1, 2]

        random.shuffle(starts)  # mix it

        # Choose the first of the mixed one - it will be the vector of the ball
        self.x = starts[0]

        # at the very beginning, it always falls down, so we reduce the value of the axis Y
        self.y = -2

        # Sharik recognizes his height and width
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

        # The property that is responsible for whether the bottom was reached or not.
        # Has not yet achieved, the meaning will be FALSE
        self.hit_bottom = False

    # We process the touch of the platform, for this we get 4 coordinates of the ball in the POS variable
    # (left upper and right lower points)
    def hit_paddle(self, pos):

        # We get the cords of the platform through the Paddle (platform) object
        paddle_pos = self.canvas.coords(self.paddle.id)

        # If the coordinates of the touch coincide with the coordinates of the platform
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:

                # We increase the score (the handler of this event will be described below)
                self.score.hit()

                return True   # Return the label that we successfully touched

        return False   # Return False - there was no touch

    # Process the Ballication of the Ball
    def draw_ball(self):

        # move the ball to the specified coordinates X and Y
        self.canvas.move(self.id, self.x, self.y)

        # remembered the new ball coordinates
        pos = self.canvas.coords(self.id)

        if pos[1] <= 0:  # If the ball falls from above
            self.y = 2  # set the fall in the next step = 2

        # If the ball with the right lower corner touched the bottom
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True  # We mark it in a separate variable

            # display a message and number of glasses
            canvas.create_text(250, 120, text='Sorry, You are lost', font=('Courier', 30), fill='blue')

        if self.hit_paddle(pos) == True:    # If there was a touch of the platform
            self.y = -2   # Send the ball upstairs

        if pos[0] <= 0:   # If touched the left wall
            self.x = 2  # We are moving to the right

        if pos[2] >= self.canvas_width:   # If touched the right wall
            self.x = -2   # We are moving to the left


class Paddle:   # Describing the Paddle class, which is responsible for the platforms
    def __init__(self, canvas, color):    # constructor
        canvas.create_text(250, 90, text='Click "Enter" to get started game', font=('Courier', 15), fill='blue')
        self.canvas = canvas    # canvas means that the platform will be drawn on our original canvas

        # Create a rectangular platform of 10 per 100 pixels, paint over the chosen color and get its inner name
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)

        # We set a list of possible starting positions of the platform
        start_1 = [40, 60, 90, 120, 150, 180, 200]
        random.shuffle(start_1)   # mix them
        self.starting_point_x = start_1[0]   # Select the first of the mixed

        # move the platform to the starting position
        self.canvas.move(self.id, self.starting_point_x, 300)

        # while the platform is not moving anywhere, so there are no changes on
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()   # Platform recognizes its width

        # set the press processor
        # If the arrow is pressed to the right, the Turn_Right () method is performed
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)    # If the arrow is left - turn_left ()
        self.started = False    # until the game has begun, so we are waiting

        # As soon as the player presses Enter, everything starts
        self.canvas.bind_all('<KeyPress-Return>', self.start_game)

    def turn_right(self, event):     # We are moving to the right
        self.x = 2  # We will shift to the right of 2 pixels along the axis x

    def turn_left(self, event):   # We are moving to the left
        self.x = -2   # We will shift to the left of 2 pixels along the axis x

    def start_game(self, event):    # The game begins
        self.started = True    # Change the value of the variable that is responsible for the start

    # Method that is responsible for the movement of the platform
    def draw_canvas(self):

        # We move our platform to a given number of pixels
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)   # We get the coordinates of the canvas
        if pos[0] <= 0:    # If we rested on the left border
            self.x = 0     # We stop
        elif pos[2] >= self.canvas_width:   # If you rested on the right border
            self.x = 0  # We stop


# Describe the Score class, which is responsible for displaying accounts
class Score:
    def __init__(self, canvas, color):    # constructor
        self.score = 0   # at the very beginning, the score is zero
        self.canvas = canvas     # We will use our canvas

        # Create an inscription that shows the current account,
        # we need it color and remember the internal name of this inscription
        self.id = canvas.create_text(450, 10, text=self.score, font=('Courier', 15), fill=color)

    def hit(self):    # Processing the platform touch
        self.score += 1   # We increase the score per unit
        self.canvas.itemconfig(self.id, text=self.score)    # We write a new account value


score = Score(canvas, 'brown')   # Create an object - yellow account
paddle = Paddle(canvas, 'gray')    # Create an object - a green platform
ball = Ball(canvas, paddle, score, 'purple')    # Create an object - purple ball
while not ball.hit_bottom:   # Until the ball has touched the bottom
    if paddle.started == True:   # If the game has begun and the platform can move
        ball.draw_ball()   # move the ball
        paddle.draw_canvas()   # move the platform
    window.update_idletasks()     # We update our playing field so that everything you need is to be drawn
    window.update()   # We update the game field, and look to ensure that everything that should have been done is done
    time.sleep(0.01)    # We freeze for one hundred seconds so that the movement of the elements looks smooth

# If the program has reached a long time, then the ball touched the bottom.
# We are waiting for 3 seconds, while the player reads the final inscription, and finish the game
time.sleep(3)
