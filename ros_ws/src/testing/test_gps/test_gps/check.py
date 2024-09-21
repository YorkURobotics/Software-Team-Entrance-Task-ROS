import rclpy
from rclpy.node import Node

class Check(Node):
    def __init__(self):
        super().__init__("check")
        try:
            from interfaces.msg import Completed
            self.sub = self.create_subscription(Completed, "Dish",self.subscribercallback,10)
        except:
            self.get_logger().info("Could not subscribe to topic 'Dish' with message type 'Completed'. Is your message incorrectly defined?")

        self.latlist = [51.42754807863913, 51.418060772879215, 51.41858702708693, 51.42454029940619, 51.42418848521761, 51.42479313788859, 51.41894613172539, 51.42749428205108, 51.41743366375074, 51.422489426910865, 51.43126995445112, 51.42453312979298, 51.43035368379396, 51.42685587893927, 51.41407277944937, 51.42881002718498, 51.42701444009575, 51.4317217323893, 51.41642220835387, 51.427850968864064, 51.41787213455907, 51.42966373557664, 51.432824767010175, 51.41531063209058, 51.43017122171494, 51.415800805250655, 51.421813655837845, 51.41811388168051, 51.427725457364055, 51.418650807576086, 51.418812354152806, 51.42495763333679, 51.4323702678898, 51.42596316420126, 51.417169225864896, 51.41732038632918, 51.43182933019334, 51.425500169297855, 51.413951136388384, 51.42972671566446, 51.42308523916145, 51.42295859701948, 51.427346461212586, 51.41410141020858, 51.42887321307377, 51.42624321298693, 51.419754123243884, 51.419745520795395, 51.416412082796064]
        self.heading = [208.1, 309.3, 338.6, 228.6, 134.4, 112.3, 0.8, 195.0, 46.6, 274.9, 190.9, 254.7, 212.9, 125.7, 35.0, 164.9, 232.8, 144.6, 29.5, 147.7, 48.7, 149.0, 196.8, 30.3, 162.3, 331.6, 76.3, 356.3, 139.4, 335.1, 47.3, 247.4, 179.2, 211.3, 326.6, 333.8, 209.3, 238.6, 333.2, 208.8, 92.4, 90.9, 209.0, 25.8, 149.1, 164.9, 52.0, 57.7, 349.5]
        self.distance = [588.3, 845.9, 512.1, 279.0, 208.0, 561.1, 437.0, 530.9, 880.1, 509.7, 949.5, 695.1, 989.5, 757.8, 1193.9, 682.5, 759.4, 1204.5, 823.9, 653.3, 843.4, 879.3, 1154.5, 974.4, 850.5, 894.2, 501.2, 530.6, 709.1, 518.0, 666.4, 599.6, 1054.6, 400.9, 759.8, 688.3, 1140.1, 558.1, 1111.6, 867.8, 547.7, 546.0, 567.5, 1083.0, 776.5, 387.2, 564.4, 652.5, 730.7]

    def subscribercallback(self,msg):
        try:
            i = self.latlist.index(msg.latitude)
            if((self.heading[i] == msg.heading) and (self.distance[i] == msg.distance)):
                self.get_logger().info("Correct")
            else:
                self.get_logger().info(f"Expected: {self.heading[i]}, {self.distance[i]} and received: {msg.heading}, {msg.distance}")
                self.get_logger().info("Incorrect")
        except:
            self.get_logger().info("Could not access message fields. Are your fields consistent with the outline?")

def main():
    rclpy.init()
    node = Check()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()