import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from px4_msgs.msg import VehicleLocalPosition, VehicleStatus

POS_TOPIC = '/fmu/out/vehicle_local_position_v1'
STATUS_TOPIC = '/fmu/out/vehicle_status_v4'

class TelemetryNode(Node):
    def __init__(self):
        super().__init__('telemetry_node')

        qos = QoSProfile(
            reliability = ReliabilityPolicy.BEST_EFFORT, history = HistoryPolicy.KEEP_LAST, depth=1
        )

        self.create_subscription(VehicleLocalPosition, POS_TOPIC, self.local_position_callback, qos)
        self.create_subscription(VehicleStatus, STATUS_TOPIC, self.vehicle_status_callback, qos)

    def local_position_callback(self, msg):
        # PX4 NED -> ROS ENU
        self.get_logger().info(
            f'ENU x={msg.y:.2f} '
            f'y={msg.x:.2f} '
            f'z={-msg.z:.2f}')
        

    def vehicle_status_callback(self, msg):
        armed = msg.arming_state == 2
        self.get_logger().info(
            f'Armed: {armed}'
            f'(arming_state={msg.arming_state}, '
            f'nav_state={msg.nav_state})')



def main(args=None):
    rclpy.init(args=args)
    node = TelemetryNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()