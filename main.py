from audio_transcript import result
import os
#import urlib.request
url = "https://translated.turbopages.org/proxy_u/en-ru.ru.9a6ffa55-62bb097a-7595f4d2-74722d776562/http/www.nirsoft.net/utils/nircmd.zip"
speech_words = result.split(' ')
print(speech_words)
#f = open('words.txt', 'r')
word = 'открыть'
#words_variants = [word.replace('\n', '') for word in f]

class Commands():
        def open_monitor_keyboard(self):
                os.system('%SystemRoot%\system32\osk.exe')

        def turn_on_sound(self):
                pass

        def turn_off_sound(self):
                pass

        def sub(self, first_n, second_n):
                print(first_n - second_n)

obj = Commands()
#Проверка на принадлежность к командам
commands = {1: {'открыть экранную клавиатуру': obj.open_monitor_keyboard,
             'откройте экранную клавиатуру': obj.open_monitor_keyboard,
            'откроете экранную клавиатуру': obj.open_monitor_keyboard,
            'открой экранную клавиатуру': obj.open_monitor_keyboard,
            'откроем экранную клавиатуру': obj.open_monitor_keyboard,},

            2: {'выключить звук': obj.turn_off_sound,
            'выключи звук': obj.turn_off_sound,
            'выключишь звук': obj.turn_off_sound,
            'выключите звук': obj.turn_off_sound,
            'выключим звук': obj.turn_off_sound,},

            3: {'включить звук': obj.turn_on_sound,
            'включим звук': obj.turn_on_sound,
            'включишь звук': obj.turn_on_sound,
            'включите звук': obj.turn_on_sound,
            'включи звук': obj.turn_on_sound,},

            4: {'Вычитание': obj.sub}}
list_commands = [command for command in commands.keys() if command != 'Вычитание']
'''
def dict_of_commands(commands):
    commands_words = [(key, command.split(' ')) for key in commands.keys() for command in commands[key].keys()]
    #print(commands_words)
    a = {(x, y[0]):'None' if len(y) == 1 else sub_of_dict_commands(y[1:]) for x,y in commands_words}
    return a
def sub_of_dict_commands(commands):
    commands_words = [commands]
    #print(commands_words)
    result = {x[0]: 'None' if len(x) == 1 else sub_of_dict_commands(x[1:]) for x in commands_words}
    return result
def command_conformity(words, commands, potential_command=[], potential_word = {1:'', 2: '', 3: '', 4: ''}, correct=0):
    try:
        word = words[0]
    except:
        return(potential_word, potential_command)
    available_commands = dict_of_commands(commands)
    mapping = [(key, len(list(filter(lambda x: x[0] == x[1], zip(key[1], word)))) / len(key[1]))
               for key in available_commands.keys()]

    for i in mapping:
        if i[1] == 1 and not(i[0] in potential_command):
            correct += 1
            potential_word[i[0]] = potential_word[i[0]] + word
        elif i[1] >= 0.6 and not(i[0] in potential_command):
            correct += 0.5
            potential_command.append(i[0])
    command_conformity(words[1:], commands[])

commands_list = [commands[x] for x in commands.keys()]
'''
def is_command():
    commands_count = []
    for key in commands.keys():
        for i in commands[key]:
            if i in result.lower():
                commands_count.append((key, i))
                break

    if not commands_count:
        result_speech = compare_words(speech_words)
        commands_count = [(x,list(commands[x])[0]) for x in result_speech.keys() if result_speech[x] >=1]
        return (commands_count, 0)
    else:
        return (commands_count, 1)


def compare_words(words, possible_commands={x:0 for x in commands.keys()}):
    try:
        word = words[0]
    except:
        #print('here_2')
        print(possible_commands)
        return possible_commands
    for key in commands.keys():
        for command in commands[key]:
            stop_com = False
            for com_word in command.split(' '):
                common_chars = list(filter(lambda x: x[0] == x[1], zip(com_word, word)))
                print((len(common_chars) / len(com_word), 'word --- ', com_word, 'my word is ---- ', word))
                if (len(common_chars) / len(com_word)) >= 0.5:
                    possible_commands[key] += 1
                    stop_com = True
                    break
            if stop_com: break
    return compare_words(words[1:], possible_commands=possible_commands)

def sending_result():
    result = is_command()
    try:
        if result[1] == 1:
            for i in








#try:
 #       commands[result]()
#except:
  #      potential_commands = [command for command in list_commands if command in result.lower()]
   #     print(potential_commands)

print(is_command())
