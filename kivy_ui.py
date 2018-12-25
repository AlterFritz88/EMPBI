from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.dropdown import DropDown


from kivy.lang import Builder
Builder.load_file('kivy_ui.kv')

class Main(AnchorLayout):
    pass

class Control(BoxLayout):
    pass

a = 'ОБОЛОЧКА'
class EMPBI(App):
    import time
    #app.root.ids._label.ids.mail_label.text = str(app.time.time())
    count_cirkles = 1
    def build(self):
        return Main()
    def print_out(self):
        print(self.count_cirkles)







if __name__ == "__main__":
    EMPBI().run()