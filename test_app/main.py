
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty

class MainWidget(BoxLayout):
    
    first_number = StringProperty("0")
#    second_number = StringProperty("0")
    total = StringProperty("0")
    current_sign = ""

    def text_enter(self, widget):
        self.first_number = str(int(widget.text) + int(self.total))
    
    def clear(self):
        self.total = "0"

    def mult_number(self, widget):
        first_number = str(widget.text)
        total = str(float(self.total) * int(first_number))
        self.total = str(int(total)) if isinstance(total, int) else str(float(total))
        widget.text = str(0)

    def div_number(self, widget):
        first_number = str(widget.text)
        total = str(float(self.total) / int(first_number))
        self.total = str(int(total)) if isinstance(total, int) else str(float(total))
        widget.text = str(0)

    def add_number(self, widget):
        first_number = str(widget.text)
        total = str(float(self.total) + int(first_number))
        self.total = str(int(total)) if isinstance(total, int) else str(float(total))
        widget.text = str(0)

    def sub_number(self, widget):
        first_number = str(widget.text)
        total = str(float(self.total) - int(first_number))
        self.total = str(int(total)) if isinstance(total, int) else str(float(total))
        widget.text = str(0)

class MainApp(App):
    
    def build(self):
        return MainWidget()

if __name__ == "__main__":
    MainApp().run()