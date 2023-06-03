import logging

from mycroft import MycroftSkill, intent_file_handler
import requests


class Moving(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.url = 'http://192.168.1.25:8000/moving?direction='

    @intent_file_handler('moving.intent')
    def handle_moving(self, message):
        utt = message.data.get('utterance')
        utt = str(utt)
        utt = utt[6:]
        logging.info("Полученный текст: " + utt)
        direct = "Не могу распознать направление"
        if (utt in ["вправо", "право", "направо"]):
            direct = "Едем направо"
            r = requests.get(self.url + 'right')
            print('Получен ответ: ' + r.text)
        if (utt in ["влево", "лево", "налево"]):
            direct = "Едем налево"
            r = requests.get(self.url + 'left')
            print('Получен ответ: ' + r.text)
        if (utt in ["вперед", "прямо"]):
            direct = "Едем прямо"
            r = requests.get(self.url + 'forward')
            print('Получен ответ: ' + r.text)
        if (utt in ["назад"]):
            direct = "Едем назад"
            r = requests.get(self.url + 'backward')
            print('Получен ответ: ' + r.text)
        if (utt in ["стой", "стоять", "остановись", "стоп"]):
            direct = "Стоим"
            r = requests.get(self.url + 'stop')
            print('Получен ответ: ' + r.text)
        logging.info(direct)
        self.speak(direct)


def create_skill():
    return Moving()


# if __name__ == '__main__':
#     a = Moving()
#     utt = "робот налево"
#     a.handle_moving(utt)
#     utt = 'робот направо'
#     a.handle_moving(utt)
#     utt = 'робот прямо'
#     a.handle_moving(utt)
