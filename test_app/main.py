
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.utils import platform
from kivy.properties import StringProperty, NumericProperty

if platform != "android":
    Config.set('graphics', 'width', '270')
    Config.set('graphics', 'height', '575')
Config.set('graphics', 'resizable', True)


BG_NORMAL = "resources/Light rectangle.png"
BG_DOWN = "resources/Dark rectangle.png"

class MainWidget(BoxLayout):
    
    first_number = StringProperty("0")
    second_number = StringProperty("0")
    total = StringProperty("0")
    equation = StringProperty("0")
    last_is_num = True

    def numeric_buttons(self, widget):
        for one in range(9):
            num_ = one + 1
            btn_ = Button(text=str(num_))
            btn_.background_normal = BG_NORMAL
            btn_.background_down = BG_DOWN
            btn_.border = (0, 0, 0, 0)
            btn_.id = f"btn_{num_}"
            btn_.font_size = 30
            self.press_btn(btn_, num_)
            widget.add_widget(btn_)
    
    def math_buttons(self, widget):
        for sign in ["+", "-", "*", "/"]:
            btn_ = Button(text=sign)
            btn_.background_normal = BG_NORMAL
            btn_.background_down = BG_DOWN
            btn_.border = (0, 0, 0, 0)
            btn_.font_size = 30
            self.press_btn(btn_, sign)
            widget.add_widget(btn_)
    
    def press_btn(self, btn, sign_or_num):
        btn.on_press = lambda: self.pressed(sign_or_num)

    def pressed(self, sign_or_num):
        if isinstance(sign_or_num, int):
            self.amend_number(sign_or_num)
        else:
            self.amend_sign(sign_or_num)
    
    def amend_number(self, num):
        if self.equation == "0":
            self.equation = str(num)
        else:
            self.equation += str(num)
        self.last_is_num = True

    def amend_sign(self, sign):
        if self.last_is_num:
            self.equation += f" {sign} "
            self.last_is_num = False
        else:
            self.equation = self.equation[:-3] + f" {sign} "

    def plus_minus(self):
        if self.equation.startswith("-"):
            self.equation = self.equation.lstrip("-")
        elif self.equation == "0":
            pass
        else:
            self.equation = f"-{self.equation}"

    def amend_zero(self):
        if self.equation == "0":
            pass
        else:
            self.equation += "0"

    def clear_equation(self):
        self.equation = "0"
    
    def equal(self):
        self.total = str(eval(self.equation))


class MainApp(App):
    
    def build(self):
        return MainWidget()

if __name__ == "__main__":
    MainApp().run()