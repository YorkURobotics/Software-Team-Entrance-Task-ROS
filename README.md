# Software-Team-Entrance-Task

## Introduction

This task aims to create a simple ROS2 node that receives the current GPS location and calculates the distance and heading between the current location and multiple target locations. Once these distances and headings are calculated, you must publish them to their respective topics with a custom message that meets our testing criteria.

## Task Overview

To effectively operate our rover in the field, it's crucial to have the ability to calculate the distance and heading to objects of interest relative to the rover. This information is valuable for many applications such as aligning radio equipment and autonomous traversal. The responsibility of acquiring and publishing this information has fallen to you. Your task is to create a ROS2 node that performs this calculation and provides real-time updates to the rover's control system on the location of a communications dish based on the recieved position of the rover. Below you will find a breakdown of the critical components, requirements, and steps involved.

## Workplace Structure

Within the `ros_ws/src` directory, we store all of our ros packages grouped by their respective subsystem. The workspace for this task has the following subsystems and packages:

- `Navigation` - Contains all of the packages related to the localization of the rover

  - `launch_nav` - Contains the launch file that is used to launch all of the nodes related to navigation
  - `GPS` - Contains the node that is used to get the current GPS location of the rover (will not be used for this task as it needs a GPS module to work, instead you will be using `testing/test_gps` to simulate the GPS node)
  - `gps_distance` - **You must make this package**

- `testing` - Contains all of the packages related to testing different nodes of the rover

  - `launch_test` - Contains the launch file that is used to launch all of the nodes related to testing
  - `test_gps` - Contains the node that will be used to test the node created for this task

- `interfaces` - Contains all of the custom messages, services, and actions that are used within our workspace.
  - `msg` - Contains all of the custom messages that are used within our workspace.

## Requirements

- Do not build your package using symlink, if you do so the package will not build properly. If you do accidentally build using symlink, you can fix your build by deleting the build, install, and log files and rebuilding without symlink
- Must use ROS2 Humble
- Must be running on an Ubuntu 22.04 environment (can be a VM or WSL)
- Your ros2 node can be created in Python or C++.
- Your node must be added to the main launch file of the navigation subsystem (although you may launch your package using `bash ros2 run`.
- Use Git to clone the repository (you must make a local clone as your solution should not be public), and use commits to organize and label your changes. At the end, you should zip the directory (turning it into a compressed file) and submit it to the google forms submission link below.

## Task Breakdown

### 1. Creating a ros package

Firstly create a new ros package within the `ros_ws/src/Navigation` directory, this package should be named `gps_distance`.

### 2. Subscribing to current GPS location

Your node will receive [NavSatFix](https://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/NavSatFix.html) messages over the "GCS" topic, only the latitude and longitude fields are populated. You may gain some insight into the structure of the message by running `ros2 topic echo "GCS"` after the launch_test script has been launched using `ros2 launch lauch_test launch.launch.py`.

[Basic Pub/Sub](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)

### 3. Calculating distance and heading

The formula you will use for the arithmetic is called the [Haversine](https://en.wikipedia.org/wiki/Haversine_formula) formula for distance, this formula is used to compute the great-circle distance between two points on a sphere. An important consideration for the distance calculation is that the earth is not a perfect sphere, for this task, it will be assumed that we are operating at CIRC Summer which is held in Drumheller Alberta. The earth's radius at the operating site should be assumed to be 6365.766km. This radius is the sum of the altitude and radius for a given latitude.

You can use this for the Haversine formula:

$$
\text{radicand} = \sin^2\left(\frac{\Delta \text{lat}_r}{2}\right) + \cos(\text{lat1}_r) \cdot \cos(\text{lat2}_r) \cdot \sin^2\left(\frac{\Delta \text{lon}_r}{2}\right)
$$

$$
\text{distance} = 2 \cdot \text{Radius} \cdot \text{atan2}\left(\sqrt{\text{radicand}}, \sqrt{1 - \text{radicand}}\right) \times 1000
$$

To calculate the heading you may use the following function and add it to your code:

```python
def get_heading(longitude, latitude):
  lat1 = radians(latitude)
  lon1 = radians(longitude)
  lat2 = radians(51.42287924341543)
  lon2 = radians(-112.64106837507106)

  delta_lat = lat2 - lat1
  delta_lon = lon2 - lon1

  y = sin(delta_lon) * cos(lat2)
  x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(delta_lon)
  bearing = atan2(y, x)
  bearing = degrees(bearing)
  bearing = (bearing + 360) % 360
  heading = round(bearing, 1)
  return heading
```

#### Key constants

- Dish 51.42287924341543,-112.64106837507106
- Radius 6365.766km

### 4. Publishing distance and heading (with custom message)

Your output should be published to the “Dish” topic for every pair of GCS coordinates individually as they are received.
The format of your custom message must meet the message specifications exactly, otherwise, your work will not be able to be checked by the check node. The message should consist of four float64 fields named as follows “latitude”, “longitude”, “distance”, and “heading”. Where the “latitude” and “longitude” are the GCS coordinate pair of the rover received on the topic “GCS”, “distance” is the distance in meters rounded to one decimal point between the received rover GCS pair and the fixed dish coordinates (51.42287924341543,-112.64106837507106). “Heading” is the heading of the dish from the rover, this heading is measured in degrees off of true north rounded to one decimal point.

[Basic Pub/Sub](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)

<!-- Instructions for adding a custom message-->

The custom message must be named "Completed.msg", located under `ros_ws/src/interfaces/msg`, and must follow the format described above. There are more steps involved in adding a custom message, a good tutorial can be found [here](https://roboticsbackend.com/ros2-create-custom-message/).

### 5. Adding your node to the launch file

<!-- as it is right now this launch file already exists-->

Now that you have created the node, you must add it to the Navigation package launch file. The launch file should be named `launch.launch.py` and should be located within the `ros_ws/src/Navigation/launch` directory. There are additional steps when it comes to adding nodes to launch files other than editing the launch file itself, refer to the [official documentation](https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Creating-Launch-Files.html).

### 6. Testing

To test your node, you must launch both your launch file and the launch_test file. These should be launched in separate terminals.

`ros2 launch launch_test launch.launch.py`

`ros2 launch {yourlauchpackage} {yourlaunchfile}`

You should receive feedback in the terminal you ran launch_test in. This feedback is limited to message issues. If you are not receiving any messages from the check node in the terminal you ran launch_test in, it's likely you aren't publishing to "Dish". You may run `ros2 topic echo "Dish"` in a separate terminal to be sure.

## Submission

Once you have completed the task, you must submit your solution to the task by filling out the following form:
[YURS Software Entrance Task Submission](https://forms.gle/rt4sNMuXR9Ve1uSS7)

### Deliverables

- A link to a zip file (compressed file) that contains the repository holding your solution to the task (must have your changes organized as commits), the repo should contain the following:
  - A ros package named `gps_distance` within the `ros_ws/src/navigation` directory
  - A node within the `gps_distance` package that subscribes to "GCS" and for each GCS coordinate pair publishes the appropriate message to the "Dish" topic.
  - A launch file within the `ros_ws/src/Navigation/launch` directory which launches your node. <!-- specific naming optionally -->
- A link to a video of the output of the launch file created for this task. The video should show the terminals in which you launched the test launch file and your own, as well as the [rqt_graph](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html#rqt-graph)
