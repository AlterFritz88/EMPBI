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
from kivy.properties import ListProperty


from kivy.lang import Builder
Builder.load_file('kivy_ui.kv')

class Main(AnchorLayout):
    pass

class Control(BoxLayout):
    pass

class EMPBI(App):
    #self.root.ids._label.ids.mail_label.text = str(app.time.time())
    count_cirkles = 1
    my_data = []
    screen_data =[]
    screen_etalons = []
    srav_res = []
    potok = None
    pause_time = 0.1
    etap_nach = 1
    etap_kon = 1
    shag = 0
    mod = 0
    rezim = 1
    cycles = 1
    mod_indicate = 0
    cycles_indicator = 1
    shag_indicate = 0
    etap_indicate = 1
    norma = True

    test_list = [1,2,2, 133]


    def build(self):
        #Main.ids._label.ids.mail_label.text = str(self.time.time())
        #print(Main.ids)
        self.data = [{'row_id': x, 'text': str(x)} for x in range(16)]
        return Main()


    def print_out(self):
        print(self.count_cirkles)
        print(self.root.ids)
        print(self.root.ids.choices)


    def do_program(self):
        data = get_info_for_send()

        for i in range(self.count_cirkles):
            for j in range(len(data)):
                get_ans = etap_processor(data[j][-1], data[j][1])
                self.screen_data = get_ans
                self.screen_etalons =  data[j][-1]
                self.srav_res = ['Норма' if x == y else 'Не норма' for x, y in zip(self.screen_data,self.screen_etalons)]
                time.sleep(self.pause_time)
                if 'Не норма' in self.srav_res:
                    self.norma = 'Не Норма'
                else:
                    self.norma = 'Норма'
                self.cycles_indicator = i
                if len(data[j][0]) > 2:
                    self.mod_indicate = data[j][0][2]
                else:
                    self.mod_indicate = 0
                self.shag_indicate = data[j][0][1]

                if j == 0:
                    init_etap = 1
                else:
                    if data[j][0][0] != data[j-1][0][0]:
                        init_etap += 1
                self.etap_indicate = init_etap
                print(j)
                self.show()

    def do_otladka(self):
        self.etap_nach = self.check_enter(self.root.ids._etap_info.ids._etap_nach.text)
        self.etap_kon = self.check_enter(self.root.ids._etap_info.ids._etap_kon.text)
        self.shag  = self.check_enter(self.root.ids._etap_info.ids._shag.text)
        self.mod = self.check_enter(self.root.ids._etap_info.ids._mod.text)
        self.rezim = self.check_enter(self.root.ids._etap_info.ids._rezim.text)
        self.cycles = self.check_enter(self.root.ids._etap_info.ids._cycles.text)
        data = get_info_for_send()
        data_cut = []

        counter = 1
        for etap in range(len(data)):
            print(data[etap])
            if self.mod == 0 and self.shag > 0 and self.etap_kon == counter and data[etap][0][1] == self.shag+1:
                break

            if etap > 0:
                if data[etap][0][0] != data[etap-1][0][0]:
                    counter += 1
                if counter in range(self.etap_nach, self.etap_kon+1):
                    data_cut.append(data[etap])
            if etap == 0:
                if counter in range(self.etap_nach, self.etap_kon+1):
                    data_cut.append(data[etap])
            if self.mod != 0 and self.shag != 0:
                if counter == self.etap_kon and data[etap][0][1] == self.shag and data[etap][0][2] == self.mod:
                    break
        for i in data_cut:
            print(i)

        for i in range(self.cycles):
            for j in range(len(data_cut)):
                get_ans = etap_processor(data_cut[j][-1], data_cut[j][1])
                self.screen_data = get_ans
                self.screen_etalons = data_cut[j][-1]
                self.srav_res = ['Норма' if x == y else 'Не норма' for x, y in
                                 zip(self.screen_data, self.screen_etalons)]
                time.sleep(self.pause_time)
                if 'Не норма' in self.srav_res:
                    self.norma = 'Не Норма'
                else:
                    self.norma = 'Норма'
                self.cycles_indicator = i
                if len(data_cut[j][0]) > 2:
                    self.mod_indicate = data_cut[j][0][2]
                else:
                    self.mod_indicate = 0
                self.shag_indicate = data_cut[j][0][1]

                if j == 0:
                    init_etap = self.etap_nach
                else:
                    if data_cut[j][0][0] != data_cut[j - 1][0][0]:
                        init_etap += 1
                self.etap_indicate = init_etap
                print(j)
                self.show()


    def upd_ltxt(self):
        self.potok = threading.Thread(target=self.do_program)
        self.potok.start()

    def otladka(self):
        self.potok = threading.Thread(target=self.do_otladka)
        self.potok.start()


    def show(self):
        self.root.ids._label.ids._income_data.adapter.data = self.screen_data
        self.root.ids._label.ids._etalon_data.adapter.data = self.screen_etalons
        self.root.ids._label.ids._result.adapter.data = self.srav_res
        self.root.ids._indicate.ids._norma.text = self.norma
        self.root.ids._indicate.ids._cycles_indicate.text = str(self.cycles_indicator + 1)
        self.root.ids._indicate.ids._mod_indicate.text = str(self.mod_indicate)
        self.root.ids._indicate.ids._shag_indicate.text = str(self.shag_indicate)
        self.root.ids._indicate.ids._etap_indicate.text = str(self.etap_indicate)
        print('показываю')
        #print(self.root.ids._label.ids._income_data.adapter.data)


    def check_enter(self, string):
        if len(string) > 0:
            return int(string)
        else:
            return 1


if __name__ == "__main__":
    EMPBI().run()