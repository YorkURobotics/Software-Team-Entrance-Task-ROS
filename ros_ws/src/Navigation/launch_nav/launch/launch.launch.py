from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    # This is an example of the proper structure
    # check = Node(
    #     package="gps_distance",
    #     executable="completeSoftwareOnboarding",
    # )

    # ld.add_action(check)
    
    # Your code here

    return ld