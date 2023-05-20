from mycroft import MycroftSkill, intent_file_handler


class Moving(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('moving.intent')
    def handle_moving(self, message):
        self.speak_dialog('moving')


def create_skill():
    return Moving()

