from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    test_gps_node = Node(
        package="test_gps",
        executable="test_gps",
    )

    check_node = Node(
        package="test_gps",
        executable="check"
    )

    ld.add_action(test_gps_node)
    ld.add_action(check_node)

    return ld