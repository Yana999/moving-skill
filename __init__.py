import logging
from mycroft import MycroftSkill, intent_file_handler
from mycroft_bus_client import MessageBusClient, Message


class Moving(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        print('Setting up client to connect to a local mycroft instance')
        self.client = MessageBusClient()
        self.client.run_in_thread()

    @intent_file_handler('moving.intent')
    def handle_moving(self, message):
        utt = message.data.get('utterance')
        utt = str(utt)
        utt = utt[6:]
        logging.info("Полученный текст: " + utt)
        print('Sending speak message...')
        direct = "Не могу распознать направление"
        if (utt in ["вправо", "право", "направо"]):
            direct = "Едем направо"
            logging.info(direct)
            self.client.emit(Message('speak', data={'direction': 3}))
        if (utt in ["влево", "лево", "налево"]):
            direct = "Едем налево"
            logging.info(direct)
            self.client.emit(Message('speak', data={'direction': 2}))
        if (utt in ["вперед", "прямо"]):
            direct = "Едем прямо"
            logging.info()
            self.client.emit(Message('speak', data={'direction': 1}))
        if (utt in ["назад"]):
            direct = "Едем назад"
            logging.info(direct)
            self.client.emit(Message('speak', data={'direction': 4}))
        if (utt in ["стой", "стоять", "остановись", "стоп"]):
            direct = "Стоим"
            logging.info(direct)
            self.client.emit(Message('speak', data={'utterance': 'Hello World'}))
        self.speak(direct)


def create_skill():
    return Moving()

