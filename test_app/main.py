
import decimal

from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.utils import platform
from kivy.properties import StringProperty, ObjectProperty
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.config import Config

Config.set('graphics', 'resizable', True)

SPACING = 10
PADDING = 10

PEWTER_BLUE = (144/255, 175/255, 197/255, 1)
TEAL_BLUE = (51/255, 107/255, 135/255, 1)
BLUE = (81/255, 102/255, 130/255, 1)

GREENLY = (111/255, 185/255, 143/255, 1)
GREEN_RAIN = (44/255, 120/255, 115/255, 1)

LIGHT_PINK = (255/255, 168/255, 168/255, 1)
DARK_PINK = (185/255, 74/255, 74/255, 1)


SHADOW = (42/255, 49/255, 50/255, 1)

current_color_scheme = "blue"

class RoundedButton(Button):

    color_id = StringProperty("blue")

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
            self.img.color = [1, 1, 1, 1]
            self.img.size = sp(self.width), sp(self.height)
            self.img.center = self.center
            self.img.pos = self.pos
        elif self.color_id == "green_color":
            self.pos = self.parent.pos
            self.size = self.parent.size
            self.button_color.rgba = GREENLY
            self.on_press=lambda: self.color_change()
            self.rect.pos = self.pos
            r_tl, r_tr, r_br, r_bl = self.rect.radius
            self.rect.radius = [0, 0, r_br, r_bl]
            self.rect.size = self.size
            self.font_size = min(sp(min(self.width, self.height)/3), sp(80))
            return
        elif self.color_id == "blue_color":
            parent_pos_x, parent_pos_y = self.parent.pos
            self.pos = parent_pos_x + self.parent.width, parent_pos_y
            self.size = self.parent.size
            self.button_color.rgba = PEWTER_BLUE
            self.on_press=lambda: self.color_change()
            self.rect.pos = self.pos
            r_tl, r_tr, r_br, r_bl = self.rect.radius
            self.rect.radius = [0, 0, r_br, r_bl]
            self.rect.size = self.size
            self.font_size = min(sp(min(self.width, self.height)/3), sp(80))
            return
        elif self.color_id == "red_color":
            parent_pos_x, parent_pos_y = self.parent.pos
            self.pos = parent_pos_x + 2*self.parent.width, parent_pos_y
            self.size = self.parent.size
            self.button_color.rgba = LIGHT_PINK
            self.on_press=lambda: self.color_change()
            self.rect.pos = self.pos
            r_tl, r_tr, r_br, r_bl = self.rect.radius
            self.rect.radius = [0, 0, r_br, r_bl]
            self.rect.size = self.size
            self.font_size = min(sp(min(self.width, self.height)/3), sp(80))
            return
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.font_size = min(sp(min(self.width, self.height)/3), sp(80))
    
    def on_press(self):
        self.button_color.rgba = [75/255, 75/255, 75/255, 1]

    def on_release(self):
        global current_color_scheme
        if self.color_id == "green_color":
            color_ = GREENLY
        elif self.color_id == "blue_color":
            color_ = PEWTER_BLUE
        elif self.color_id == "red_color":
            color_ = LIGHT_PINK
        elif current_color_scheme == "green":
            color_ = GREEN_RAIN
        elif current_color_scheme == "blue":
            color_ = TEAL_BLUE
        elif current_color_scheme == "red":
            color_ = DARK_PINK
        else:
            color_ = TEAL_BLUE
        self.button_color.rgba = color_

    def color_change(self, *args):
        global current_color_scheme
        main = self.parent.parent
        num_buttons = main.ids['num_buttons']
        math_buttons = main.ids['math_buttons']
        list_ = []
        list_.extend(num_buttons.children)
        list_.extend(math_buttons.children)
        for btn in list_:
            if self.color_id == "green_color":
                color_ = GREEN_RAIN
                current_color_scheme = "green"
                Window.clearcolor = GREENLY
            elif self.color_id == "blue_color":
                color_ = TEAL_BLUE
                current_color_scheme = "blue"
                Window.clearcolor = PEWTER_BLUE
            elif self.color_id == "red_color":
                color_ = DARK_PINK
                current_color_scheme = "red"
                Window.clearcolor = LIGHT_PINK
            btn.button_color.rgba = color_
            

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

class FloatingButtons(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        btn_1 = RoundedButton()
        btn_1.color_id = "green_color"
        btn_1.pos = 0, 0
        self.add_widget(btn_1)
        btn_2 = RoundedButton()
        btn_2.color_id = "blue_color"
        btn_2.pos = Window.width/3, 0
        self.add_widget(btn_2)
        btn_3 = RoundedButton()
        btn_3.color_id = "red_color"
        btn_3.pos = 2*Window.width/3, 0
        self.add_widget(btn_3)


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
            app = App.get_running_app()
            root = app.root
            ans = self.ids.total_ans
            try:
                total = eval(self.equation)
                if ans.texture_size[0]*len(str(total)) >= root.width:
                    total = "%.e" % total
                self.total = str(total)
            except Exception as e:
                print(e)
                self.total = "ERROR !!!"

    def get_ids(self):
        return self.ids


class MainApp(App):
    
    def build(self):
        Window.clearcolor = PEWTER_BLUE
        return MainWidget()

if __name__ == "__main__":
    MainApp().run()
