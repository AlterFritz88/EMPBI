from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.dropdown import DropDown
from kivy.clock import Clock
from driver import do_prog, get_info_for_send, etap_processor
import time

import threading


from kivy.lang import Builder
Builder.load_file('kivy_ui.kv')

class Main(AnchorLayout):
    pass

class Control(BoxLayout):
    pass

a = 'ОБОЛОЧКА'
class EMPBI(App):
    import time
    #self.root.ids._label.ids.mail_label.text = str(app.time.time())
    count_cirkles = 1
    my_data = []
    screen_data =[]
    screen_etalons = []
    potok = None

    def build(self):
        #Main.ids._label.ids.mail_label.text = str(self.time.time())

        #Clock.schedule_interval(self.show, 0.1)
        #print(Main.ids._main)
        #Clock.schedule_interval(self.do_program, 0.5)
        return Main()


    def print_out(self):
        print(self.count_cirkles)
        print(self.root.ids._label.ids._data.adapter.data)


    def do_program(self):
        co = 0
        data = get_info_for_send()

        for i in range(self.count_cirkles):
            for j in data:

                get_ans = etap_processor(j[-1], j[1])
                self.screen_data = get_ans
                self.screen_etalons = [x + str(time.time()) for x in j[-1]]
                time.sleep(0.3)
                print('count do:', co)
                print(get_ans)
                co += 1

                #Clock.schedule_interval(self.show, 0.1)
                self.show()




    def upd_ltxt(self):
        self.potok = threading.Thread(target=self.do_program)
        self.potok.start()





    def show(self):
        self.root.ids._label.ids._income_data.adapter.data = self.screen_data
        self.root.ids._label.ids._etalon_data.adapter.data = self.screen_etalons
        print('показываю')
        #print(self.root.ids._label.ids._income_data.adapter.data)


    #done(data, self.count_cirkles)










if __name__ == "__main__":
    EMPBI().run()