import logging
import socket
import json
from mycroft import MycroftSkill, intent_file_handler
import requests


class Moving(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.url = 'http://192.168.1.25:8000/moving?direction='
        self.TCP_IP = '192.168.1.101'
        self.TCP_PORT = 5005
        self.BUFFER_SIZE = 128
        self.MOVING_MESSAGE = json.dumps({'robotState': 'moving'})
        self.STOP_MESSAGE = json.dumps({'robotState': 'stop'})

    @intent_file_handler('moving.intent')
    def handle_moving(self, message):
        utt = message.data.get('utterance')
        utt = str(utt)
        utt = utt[6:]
        logging.info("Полученный текст: " + utt)
        direct = "Не могу распознать направление"
        if (utt in ["вправо", "право", "направо"]):
            self.send_message(self.MOVING_MESSAGE)
            direct = "Едем направо"
            r = requests.get(self.url + 'right')
            print('Получен ответ: ' + r.text)
            self.send_message(self.STOP_MESSAGE)
        if (utt in ["влево", "лево", "налево"]):
            self.send_message(self.MOVING_MESSAGE)
            direct = "Едем налево"
            r = requests.get(self.url + 'left')
            print('Получен ответ: ' + r.text)
            self.send_message(self.STOP_MESSAGE)
        if (utt in ["вперед", "прямо"]):
            self.send_message(self.MOVING_MESSAGE)
            direct = "Едем прямо"
            r = requests.get(self.url + 'forward')
            print('Получен ответ: ' + r.text)
            self.send_message(self.STOP_MESSAGE)
        if (utt in ["назад"]):
            self.send_message(self.MOVING_MESSAGE)
            direct = "Едем назад"
            r = requests.get(self.url + 'backward')
            print('Получен ответ: ' + r.text)
            self.send_message(self.STOP_MESSAGE)
        if (utt in ["стой", "стоять", "остановись", "стоп"]):
            self.send_message(self.MOVING_MESSAGE)
            direct = "Стоим"
            r = requests.get(self.url + 'stop')
            print('Получен ответ: ' + r.text)
            self.send_message(self.STOP_MESSAGE)
        logging.info(direct)
        self.speak(direct)

    def send_message(self, message):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.TCP_IP, self.TCP_PORT))
        s.sendall(bytes(message, encoding="utf-8"))
        data = s.recv(self.BUFFER_SIZE).decode('utf-8')
        return data

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
