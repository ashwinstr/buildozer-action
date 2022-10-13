
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty

class MainWidget(BoxLayout):
    
    first_number = StringProperty("0")
    second_number = StringProperty("0")
    total = StringProperty("0")
    current_math = ""

    def text_enter(self, widget):
        self.first_number = str(int(widget.text) + int(self.total))
    
    def enter(self, widget):
        if self.current_math == "+":
            self.first_number = self.second_number
            self.total = str(int(self.first_number) + int(widget.text))


    def add_number(self, widget):
        self.current_math = "+"
        self.first_number = self.total = widget.text
        widget.text = "0"

class MainApp(App):
    
    def build(self):
        return MainWidget()

if __name__ == "__main__":
    MainApp().run()
