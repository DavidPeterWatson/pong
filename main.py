from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.core.window import Window

import kivy

# current kivy version
kivy.require('2.0.0')

# main game widget


class PongGame(Widget):
    ball = ObjectProperty(None)
    player_left = ObjectProperty(None)
    player_right = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        # get joystick events first
        Window.bind(on_joy_hat=self.on_joy_hat)
        Window.bind(on_joy_axis=self.on_joy_axis)
        Window.bind(on_joy_button_up=self.on_joy_button_up)
        Window.bind(on_joy_button_down=self.on_joy_button_down)

    # handle joystick axis event
    def on_joy_axis(self, win, stickid, axisid, value):

        if stickid == 0 and axisid == 3:
            self.player_right.center_y = value / 32767 * self.height / 2 + self.height / 2

        if stickid == 1 and axisid == 3:
            self.player_left.center_y = value / 32767 * self.height / 2 + self.height / 2

        print(f'stick:{stickid} axis:{axisid} value:{value}')

    # handle joystick hat event
    def on_joy_hat(self, win, stickid, hatid, value):
        print(f'stick:{stickid} hatid:{hatid} value:{value}')
        pass

    # handle joystick button down event
    def on_joy_button_down(self, win, stickid, buttonid):
        print(f'stick:{stickid} buttonid:{buttonid}')
        pass

    # handle joystick button up event
    def on_joy_button_up(self, win, stickid, buttonid):
        print(f'stick:{stickid} buttonid{buttonid}')
        pass

    # serve the ball from the center of the screen
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    # update the location of the ball. Basic physics engine
    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player_left.bounce_ball(self.ball)
        self.player_right.bounce_ball(self.ball)

        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player_right.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player_left.score += 1
            self.serve_ball(vel=(-4, 0))

    # move the paddles when the screen is touched
    def on_touch_move(self, touch):
        if touch.x < self.width/3:
            self.player_left.center_y = touch.y
        if touch.x > self.width - self.width/3:
            self.player_right.center_y = touch.y

# The high level application object


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

# ball widget. Similar to a scratch sprite


class PongBall(Widget):

    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # referencelist property so we can use ball.velocity as a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ``move`` function will move the ball one step. This will be called in equal intervals to animate the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


# paddle widget
class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            speedup = 1.1
            offset = 0.02 * Vector(0, ball.center_y-self.center_y)
            ball.velocity = speedup * (offset - ball.velocity)


# starting point for a python script. We use it to start the PongApp
if __name__ == '__main__':
    PongApp().run()
