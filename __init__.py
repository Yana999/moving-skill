import logging
from mycroft import MycroftSkill, intent_file_handler
from mycroft_bus_client import MessageBusClient, Message
import sys
import rclpy
from mycroft_bus_client import MessageBusClient, Message



class Moving(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        print('Setting up client to connect to a local mycroft instance')
        self.client = MessageBusClient()
        self.client.run_in_thread()
        self.fail_message = 'не удалось определить направление движения'
        # rclpy.init()
        # node = MovingNode()

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
            self.client.emit(Message('moving', data={'direction': 3}))
        if (utt in ["влево", "лево", "налево"]):
            direct = "Едем налево"
            logging.info(direct)
            self.client.emit(Message('moving', data={'direction': 2}))
        if (utt in ["вперед", "прямо"]):
            direct = "Едем прямо"
            logging.info()
            self.client.emit(Message('moving', data={'direction': 1}))
        if (utt in ["назад"]):
            direct = "Едем назад"
            logging.info(direct)
            self.client.emit(Message('moving', data={'direction': 4}))
        if (utt in ["стой", "стоять", "остановись", "стоп"]):
            direct = "Стоим"
            logging.info(direct)
            self.client.emit(Message('moving', data={'direction': 5}))
        self.speak(direct)

        # if(direction != self.fail_message):
        #     minimal_client = MovingNode()
        #     response = minimal_client.send_request(direction)
        #     minimal_client.get_logger().info(
        #     'Result of sending movment direction: %d' % response.sum)

def create_skill():
    return Moving()


# class MovingNode(Node):
#
#     def __init__(self):
#         super().__init__("moving_skill_node")
#         self.cli = self.create_client(AddTwoInts, 'send_direction')
#         while not self.cli.wait_for_service(timeout_sec=1.0):
#             self.get_logger().info('service not available, waiting again...')
#         self.req = AddTwoInts.Request()
#         self.get_logger().info("Moving node has been started")
#
#     def send_direction_command(self, direction):
#         msg =
#         self.future = self.cli.call_async(self.req)
#         rclpy.spin_until_future_complete(self, self.future)
#         return self.future.result()
