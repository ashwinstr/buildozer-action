
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.utils import platform
from kivy.properties import StringProperty
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.config import Config

Config.set('graphics', 'resizable', True)

SPACING = 10
PADDING = 20
PEWTER_BLUE = (144/255, 175/255, 197/255, 1)
TEAL_BLUE = (51/255, 107/255, 135/255, 1)
BLUE = (81/255, 102/255, 130/255, 1)
SHADOW = (42/255, 49/255, 50/255, 1)

BG_NORMAL = "resources/Light rectangle.png"
BG_DOWN = "resources/Dark rectangle.png"

class RoundedButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        with self.canvas.before:
            self.button_color = Color(rgba=TEAL_BLUE)
            self.rect = RoundedRectangle(radius=[dp(20)])
        img = self.img = Image(color=[0, 0, 0, 0])
        self.add_widget(img)
        Clock.schedule_once(self.on_size)

    def on_size(self, *args):
        if self.text == " ":
            self.img.source = "resources/backspace.png"
            self.img.center = self.center
            self.img.color = [1, 1, 1, 1]
            self.img.pos = self.pos
            self.img.size = self.size
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.font_size = sp(min(self.width, self.height)/2)
    
    def on_press(self):
        self.button_color.rgba = [75/255, 75/255, 75/255, 1]

    def on_release(self):
        self.button_color.rgba = TEAL_BLUE


class NumButtons(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = dp(PADDING)
        self.spacing = dp(SPACING)
        self.cols = 3
        self.rows = 4
        self.size_hint = 1, 0.75
        for one in range(9):
            btn_ = RoundedButton()
            btn_.text = str(one + 1)
            self.add_widget(btn_)
        for one in ["+/-", "0", "C"]:
            btn_ = RoundedButton()
            btn_.text = one
            self.add_widget(btn_)

class MathButtons(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spacing = dp(SPACING)
        self.cols = 2
        self.rows = 4
        self.size_hint = 1, 2/3
        for sign in ["+", "-", "*", "/", "(", ")", " ", "="]:
            btn_ = RoundedButton()
            btn_.text = sign
            self.add_widget(btn_)


class ComputeBox(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.colors = Color(rgba=SHADOW)
            self.rect = RoundedRectangle(radius=[dp(50), dp(50), 0, 0])
        Clock.schedule_once(self.on_size)

    def on_size(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.width, self.height + dp(50)


class MainWidget(BoxLayout):
    
    total = StringProperty("0")
    equation = StringProperty("0")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.press)

    def press(self, *args):
        widget = self.ids['num_buttons']
        for btn in widget.children:
            btn.bind(on_press=lambda btn: self.num_pressed(btn.text))
        math_widget = self.ids['math_buttons']
        for btn in math_widget.children:
            btn.bind(on_press=lambda btn: self.math_pressed(btn.text))

    def num_pressed(self, num):
        if num == "+/-":
            if self.equation.startswith("-"):
                self.equation = self.equation.lstrip("-")
            elif self.equation == "0":
                pass
            else:
                self.equation = f"-{self.equation}"
        elif num == "C":
            self.equation = "0"
        else:
            if self.equation == "0":
                self.equation = str(num)
            else:
                self.equation += str(num)

    def math_pressed(self, sign):
        last_ = self.equation[-1]
        print(self.equation[-3:])
        if sign in ["+", "-", "*", "/"]:
            if last_.isdigit():
                self.equation += f" {sign} "
                self.last_is_num = False
            else:
                self.equation = self.equation[:-3] + f" {sign} "
        elif sign == " ":
            if len(self.equation) == 1:
                self.equation = "0"
            elif len(self.equation) >= 2 and last_.isdigit():
                self.equation = self.equation[:-1]
            else:
                self.equation = self.equation[:-3]
        elif sign == "(":
            if not last_.isdigit():
                self.equation += " ( "
        elif sign == ")":
            if last_.isdigit() or self.equation[-3:] == " ) ":
                self.equation += " ) "
        elif sign == "=":
            try:
                self.total = str(eval(self.equation))
            except:
                self.total = "ERROR !!!"

class MainApp(App):
    
    def build(self):
        Window.clearcolor = PEWTER_BLUE
        if platform != 'android':
            Window.size = 1080, 2340
        return MainWidget()

if __name__ == "__main__":
    MainApp().run()