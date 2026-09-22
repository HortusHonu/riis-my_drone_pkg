import rclpy

from rclpy.node import Node
from std_msgs.msg import Float64

class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')
        self.pub = self.create_publisher(Float64, 'drone/status', 10) # Changed to a float to simulate 'altitude', in this case
        self.timer = self.create_timer(0.2, self.timer_callback)      # Changed to 10Hz (0.1 seconds 1/10)

    def timer_callback(self):
        msg = Float64()  # message data type much match the published topic, in this case drone/status
        msg.data = 10.0  # siulated altitude (float requires the decimal)
        self.pub.publish(msg)


def main(args=None):           
    rclpy.init(args=args)
    node = PublisherNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()