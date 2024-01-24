import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import numpy as np

class LidarFilterNode(Node):
    def __init__(self):
        super().__init__('lidar_filter_node')
        self.get_logger().info('Filter start')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            10
        )
        self.filtered_publisher = self.create_publisher(LaserScan, '/scan_filtered', 10)

    def lidar_callback(self, msg):
        for i in range(len(msg.ranges)):
            if msg.ranges[i] <= 0.3:
                msg.ranges[i] = np.nan
        self.get_logger().info('Filtered lidar data: {}'.format(msg.ranges))
        self.filtered_publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = LidarFilterNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
