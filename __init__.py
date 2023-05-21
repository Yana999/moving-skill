import logging
from mycroft import MycroftSkill, intent_file_handler
import sys
import rclpy
from mycroft_bus_client import MessageBusClient, Message



class Moving(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.fail_message = 'не удалось определить направление движения'
        rclpy.init()
        node = MovingNode()

    @intent_file_handler('moving.intent')
    def handle_moving(self, message):
        utt = message.data.get('utterance')
        utt = str(utt)
        utt = utt[6:]
        direction = self.fail_message
        logging.info("Полученный текст: " + utt)

        print("Sending " + direction + " to " + uri + "...")

        if (utt in ["вправо", "право", "направо"]):
            logging.info("Едем направо")
            direction = "право"

        if (utt in ["влево", "лево", "налево"]):
            logging.info("Едем налево")
            direction = "лево"

        if (utt in ["вперед", "прямо"]):
            logging.info("Едем прямо")
            direction = "прямо"

        if (utt in ["назад"]):
            logging.info("Едем назад")
            direction = "назад"

        if (utt in ["стой", "стоять", "остановись", "стоп"]):
            logging.info("Стоим")
            direction = "стоп"

        if(direction != self.fail_message):
            minimal_client = MovingNode()
            response = minimal_client.send_request(direction)
            minimal_client.get_logger().info(
            'Result of sending movment direction: %d' % response.sum)





def create_skill():
    return Moving()


class MovingNode(Node):

    def __init__(self):
        super().__init__("moving_skill_node")
        self.cli = self.create_client(AddTwoInts, 'send_direction')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()
        self.get_logger().info("Moving node has been started")

    def send_direction_command(self, direction):
        msg = 
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
