import logging
from mycroft import MycroftSkill, intent_file_handler
import websocket, rel
from threading import Event, Thread



class Moving(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.url = "ws://192.168.1.25:8181/"
        self.localhost = "ws://localhost:8000/"
        self.header = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0'}
        websocket.enableTrace(True)
        self.client = websocket.WebSocketApp(self.url,
                                             on_message=Moving.on_message,
                                             on_error=Moving.on_error,
                                             on_close=Moving.on_close,
                                             on_open=Moving.on_open,
                                             header=self.header)
        self.client.run_forever(dispatcher=rel, reconnect=25)
        self.fail_message = 'fail'

    def run_forever(self):
        """Start the websocket handling."""
        self.started_running = True
        self.client.run_forever()

    def run_in_thread(self):
        """Launches the run_forever in a separate daemon thread."""
        t = Thread(target=self.run_forever)
        t.daemon = True
        t.start()
        return t

    @intent_file_handler('moving.intent')
    def handle_moving(self, message):
        utt = message
        utt = str(utt)
        utt = utt[6:]
        logging.info("Полученный текст: " + utt)
        direct = "Не могу распознать направление"
        if (utt in ["вправо", "право", "направо"]):
            direct = "Едем направо"
            self.client.send('{"op": "publish", "topic": "hello_ros2", "msg": {"data": "right"}}')
        if (utt in ["влево", "лево", "налево"]):
            direct = "Едем налево"
            self.client.send('{"op": "publish", "topic": "hello_ros2", "msg": {"data": "left"}}')
        if (utt in ["вперед", "прямо"]):
            direct = "Едем прямо"
            self.client.send('{"op": "publish", "topic": "hello_ros2", "msg": {"data": "forward"}}')
        if (utt in ["назад"]):
            direct = "Едем назад"
            self.client.send('{"op": "publish", "topic": "hello_ros2", "msg": {"data": "backward"}}')
        if (utt in ["стой", "стоять", "остановись", "стоп"]):
            direct = "Стоим"
            self.client.send('{"op": "publish", "topic": "hello_ros2", "msg": {"data": "stop"}}')
        logging.info(direct)
        self.speak(direct)

    def on_message(ws, message):
        try:
            logging.info("Got msg: ", message)
            pass
        except:
            logging.warning('error occured - ignorring')

    def on_error(ws, error):
        print("received error as {}".format(error))

    def on_close(ws, *args):
        logging.info("Connection with driving module is closed")

    def on_open(ws):
        ws.send('{"op": "advertise", "topic": "hello_ros2", "type": "std_msgs/String"}')
        logging.info("Open connection with driving module")


def create_skill():
    return Moving()





# if __name__ == '__main__':
#     a = Moving()
#     # utt = "робот налево"
#     # a.handle_moving(utt)
#     # utt = 'робот направо'
#     # a.handle_moving(utt)
#     utt = 'робот прямо'
#     a.handle_moving(utt)
