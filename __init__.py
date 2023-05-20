import logging
from mycroft import MycroftSkill, intent_file_handler


class Moving(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('moving.intent')
    def handle_moving(self, message):
        utt = message.data.get('utterance')
        utt = str(utt)
        utt = utt[6:]
        logging.info("Полученный текст: " + utt)
        if (utt in ["вправо", "право", "направо"]):
            logging.info("Едем направо")
        if (utt in ["влево", "лево", "налево"]):
            logging.info("Едем налево")
        if (utt in ["вперед", "прямо"]):
            logging.info("Едем прямо")
        if (utt in ["назад"]):
            logging.info("Едем назад")
        if (utt in ["стой", "стоять", "остановись", "стоп"]):
            logging.info("Стоим")
        self.speak_dialog('moving')


def create_skill():
    return Moving()

