#импорт необходимых библиотек
from PyQt5 import QtCore, QtWidgets
import os
import re
import webbrowser
import sys
import speech_recognition as sr
from sound import Sound

class Window(QtWidgets.QWidget):
        def __init__(self, parent=None):
            QtWidgets.QWidget.__init__(self, parent)
            #настройки размера окна
            self.WIDTH = 300
            self.HEIGHT = 70
            self.resize(self.WIDTH, self.HEIGHT)

            #добавление кнопок и надписей
            self.added = QtWidgets.QGridLayout()
            self.label = QtWidgets.QLabel('Say Something!')
            self.label.setAlignment(QtCore.Qt.AlignHCenter)
            self.btnSay = QtWidgets.QPushButton("Начать запись")
            self.layout = QtWidgets.QGridLayout()
            self.layout.addWidget(self.label, 0, 0)
            self.layout.addWidget(self.btnSay, 1, 0)
            self.setLayout(self.layout)

            self.commands = {1: (['открыть экранную клавиатуру',
                                'откройте экранную клавиатуру',
                                'откроете экранную клавиатуру',
                                'открой экранную клавиатуру',
                                'откроем экранную клавиатуру'], self.open_monitor_keyboard),

                            2: (['выключить звук',
                                'выключи звук',
                                'выключишь звук',
                                'выключите звук',
                                'выключим звук'], self.turn_off_sound),

                            3: (['включить звук',
                                'включим звук',
                                'включишь звук',
                                'включите звук',
                                'включи звук'], self.turn_on_sound),

                            4: (r'(-?\d*[,]?\d*)(-)(-?\d*[,]?\d*)', self.sub),

                            5: (['открыть диспетчер задач',
                                'открой диспетчер задач',
                                'откройте диспетчер задач',
                                'откроете диспетчер задач',
                                'откроем диспетчер задач'], self.task_manager),

                            6: (['открой панель управления',
                                'открыть панель управления',
                                'откроете панель управления',
                                'откроем панель управления',
                                'откройте панель управления'], self.open_control),

                            7: (['поиск в интернете',
                                'поискать в интернете',
                                'поищи в интернете',
                                'поищем в интернете'], self.search),

                            8: (['закрытие голосового ассистента',
                                 'завершение работы',
                                 'закрой голосового ассистента',
                                 'закрыть голосовго ассистента',
                                 'закрытие голосового помощника',
                                 'закрой голосового помощника'], self.shut_down)}

            self.btnSay.clicked.connect(self.speech_record)
            self.btnSay.setStyleSheet("background-color:#2191fb;"
                                      "border-style: outset;"
                                      "border-width: 2px;"
                                      "border-radius: 10px;"
                                      "border-color: beige;"
                                      "font: bold 14px;"
                                      "min-width: 10em;"
                                      "padding: 6px;")
        def open_monitor_keyboard(self):
                os.system('%SystemRoot%\system32\osk.exe')

        def turn_on_sound(self):
            Sound.mute()
            if Sound.is_muted():
                    Sound.mute()

        def turn_off_sound(self):
            Sound.mute()

        def task_manager(self):
            os.system('taskmgr')

        def open_control(self):
            os.system('Control')

        def shut_down(self):
            QtWidgets.qApp.quit()

        def sub(self):
            signs = [1, 1]
            expression = re.search(self.commands[4][0], self.speech_command.replace(' ', '')).group()
            if re.fullmatch(r'-\d*,?\d*?-\d*,?\d*?', expression):
                signs[0] = -1
            elif re.fullmatch(r'-\d*,?\d*?--\d*,?\d*?', expression):
                signs[0] = -1
                signs[1] = -1
            elif re.fullmatch(r'\d*,?\d*?--\d*,?\d*?', expression):
                signs[1] = -1

            elements = list(filter(lambda x: x != '' and x != ' ', expression.replace(',', '.').split('-')))
            print(expression)
            print(elements)
            print(signs)
            label_sub = QtWidgets.QLabel(f'{expression} = {float(elements[0])*signs[0] - signs[1]*float(elements[1])}')
            self.added.addWidget(label_sub, 5, 0)
            self.layout.addLayout(self.added, 3, 0)


        def search(self):
            func = lambda text, commands: func(','.join(text.split(commands[0]+' ')), commands[1:]) if len(commands)>1 \
                else ','.join(text.split(commands[0]+' '))
            available_commands = [command for command in self.commands[7][0] if command in self.speech_command]
            print(func(self.speech_command, available_commands))
            requests = [non_empt for non_empt in func(self.speech_command, available_commands).split(',') if non_empt]
            print(requests)
            result = [webbrowser.open(f'https://yandex.ru/search/?text={request}') for request in requests]

        def sub_exception(self):
            try:
                print('maybe correct', re.search(self.commands[4][0], self.speech_command.replace(' ', '')).groups())
                return all(re.search(self.commands[4][0], self.speech_command.replace(' ', '')).groups())
            except:
                return False

        def is_command(self):
            func = lambda command: (command[0] if any([words in self.speech_command for words in command[1][0]]
                                                      if command[0] != 4 else [self.sub_exception()]) else '')
            result = list(map(func, self.commands.items()))

            return [num_com for num_com in result if num_com]


        def compare_words(self):
            print([(x[0], x[1][0]) for x in self.commands.items()])
            func_2 = lambda y, z: any([len([g for g in zip(z, word) if g[0] == g[1]])/len(word) >= 0.7 for word in y])
            func_1 = lambda command: (command[0] if any([func_2(words.split(' '), speech_word)  for words in command[1][0]
                                                    for speech_word in self.speech_words] if command[0] != 4
                                                        else [re.search(r'\d|-', self.speech_command)]) else '')
            result = list(map(func_1, self.commands.items()))
            return [num_com for num_com in result if num_com]

        def sending_result(self):
            result = self.is_command()
            if result:
                return [self.commands[x][1]() for x in result]

            compare_result = self.compare_words()
            if compare_result:
                #создает кнопки или предлагает вариант действия, если не было выполнена основная часть по поиску команд
                label = QtWidgets.QLabel('Возможны вы имели в виду')
                self.added.addWidget(label, 0, 0)
                for index in compare_result:
                        if index == 4 or index == 7:
                            label_47 = QtWidgets.QLabel(f'{"Вычитание двух чисел" if index == 4 else self.commands[index][0][0].capitalize()}')
                            self.added.addWidget(label_47, self.added.count()+1, 0)
                        else:
                            btn = QtWidgets.QPushButton(f'{self.commands[index][0][0]}')
                            btn.clicked.connect(lambda: self.commands[index][1]())
                            btn.setStyleSheet("background-color:#2191fb;"
                                          "border-style: outset;"
                                          "border-width: 2px;"
                                          "border-radius: 10px;"
                                          "border-color: beige;"
                                          "font: bold 14px;"
                                          "min-width: 10em;"
                                          "padding: 6px;")
                            self.added.addWidget(btn, self.added.count()+1, 0)



                self.layout.addLayout(self.added, 3, 0)
            else:
                #пишется надпись если в речи не было даже чего то связанного с командами
                label = QtWidgets.QLabel('Nothing was found')
                self.added = QtWidgets.QGridLayout()
                self.added.addWidget(label, 0, 1)
                self.layout.addLayout(self.added, 3, 0)

        def delete(self):
            #непосредственное удаление дополнительных кнопок и лейблов
            if self.layout.count() > 3:
                while self.added.count():
                    item = self.added.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                         widget.deleteLater()
                    else:
                        self.delete(item.layout())
            else:
                pass

        def speech_record(self):
            #очистка вывода с окна
            if self.layout.count() > 3:
                self.delete()

            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
            try:
                self.speech_command = r.recognize_google(audio, language="ru-RU").lower()
                self.speech_words = self.speech_command.split(' ')
                print("Вы сказали " + self.speech_command)
                self.sending_result()
            except sr.UnknownValueError:
                label = QtWidgets.QLabel('Речь не была распознана, повторите ещё раз')
                self.added = QtWidgets.QGridLayout()
                self.added.addWidget(label, 0, 1)
                self.layout.addLayout(self.added, 3, 0)



app = QtWidgets.QApplication([])
app.setStyle('Breeze')
window = Window()
window.setWindowTitle("Speech regonition")
window.show()
sys.exit(app.exec_())
