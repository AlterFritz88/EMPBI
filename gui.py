import PySimpleGUI as sg

sg.ChangeLookAndFeel('LightGreen')
#sg.SetOptions(element_padding=(0, 0))

# ------ Menu Definition ------ #
menu_def = [['Контроль', ['Режим', 'Кол Цикл', 'Вып', 'Печать']],
            ['Отладка', ['Этап Нач', 'Этап Кон', 'Шаг', 'Модификация', 'Режим', 'N пит', 'Кол Циклов', 'Выполнить'], ],
            ['Ручной Режим', ['ОбнулУСО', 'Пуск РГ', 'Пуск ЗУ', 'Цикл-УСО-РГ', 'Цикл-УСО-ВБ', 'Цикл-ПЭВМ-Мод', 'ИпцZUp', 'УпрZup']],
            ['Высветка', ['КоордРег', 'Чт/Зп Рг', 'КоордЗУ', 'Чт/Зп ЗУ', 'ЧтБуфВыд', 'Чтение этапа', 'ЧтениеНормДисп???']],
            ['Параметры', ['ОстНеисп', 'Пауза', 'Блок Инц Этап', 'Заглушка УСО', 'Поэтап Ост', 'Пошаг Ост', 'Мод Ост', 'Индикатор Сравнения', 'Блк.КПН', 'Блк. Диспеч', 'ЗпНнормДск', 'Бл.Zup']],
            ['Выход', 'Выход']]

# ------ GUI Defintion ------ #
layout = [
    [sg.Menu(menu_def )],
    [sg.In(size=(8,1), key='numerator')],
    [sg.Output(size=(250, 50))]
]

window = sg.Window("Программа ЭМ-ПБИ", default_element_size=(1, 1), auto_size_text=False, auto_size_buttons=True,
                   default_button_element_size=(1, 1)).Layout(layout)





# ------ Loop & Process button menu choices ------ #
while True:
    event, values = window.Read()
    if event == None or event == 'Выход':
        break
    print('Button = ', event)
    # ------ Process menu choices ------ #
    if event == 'About...':
        sg.Popup('About this program', 'Version 1.0', 'PySimpleGUI rocks...')
    elif event == 'Open':
        filename = sg.PopupGetFile('file to open', no_window=True)
        print(filename)