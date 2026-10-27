# Aruco Detector ROS 2 Jazzy Package

This ROS 2 package provides the `aruco_detector` node, which detects ArUco markers in a camera video stream using OpenCV. It estimates the 3D pose and ID of each marker, publishes TF2 transforms, and outputs an annotated image stream.

A complete launch file is included to start the entire pipeline - from the camera driver to the 3D visualization in RViz2—with a single command.

## Requirements

Before running the package, ensure you have the following dependencies installed:

* ROS 2 Jazzy
* `ros-jazzy-v4l2-camera` 
* `ros-jazzy-cv-bridge` 
* `ros-jazzy-tf2-ros` 
* `ros-jazzy-tf2-transformations`
* `ros-jazzy-geometry-msgs`
* `ros-jazzy-sensor-msgs`

You can install the camera driver using your package manager, for example:
```bash
sudo apt install ros-jazzy-v4l2-camera
```

### Important: Camera Calibration
For accurate 3D pose estimation, **your camera must be properly calibrated**. 
* The node requires accurate camera parameters provided via the `camera_info` topic.
* If your camera is not calibrated, it is highly recommended to calibrate it first using the official ROS 2 calibration tool:
```bash
sudo apt install ros-jazzy-camera-calibration

ros2 run camera_calibration cameracalibrator --pattern charuco --size <cols>x<rows> --square <square_size_in_meters> --charuco_marker_size <marker_size_in_meters> --aruco_dict <dict_name> --no-service-check image:=/image_raw
```

## Node Details: `aruco_detector`

### Subscribed Topics
* `/image_raw` (`sensor_msgs/msg/Image`): The raw image stream from the camera.
* `/camera_info` (`sensor_msgs/msg/CameraInfo`): The camera calibration metadata.

### Published Topics
* `/aruco_image` (`sensor_msgs/msg/Image`): The image stream overlayed with detected marker borders, axes, and IDs.

### TF2 Transforms
* Broadcaster: Publishes the 3D coordinate frame (`tf2`) for each detected ArUco marker relative to the camera frame, using the marker ID as the frame name (e.g., `aruco_2`).

## How to Build

1. Clone this repository into your ROS 2 workspace (`ros2_ws/src`).
2. Source your ROS 2 environment.
3. Build the package using `colcon`:

```bash
cd ~/ros2_ws
colcon build --packages-select aruco_detector
source install/setup.bash
```

## Running the Complete Pipeline

The package includes a unified launch file that automates the entire setup. Executing this file will:
1. Start the `v4l2_camera` node to stream live video.
2. Launch the `aruco_detector` node to process the frames.
3. Open `rviz2` pre-loaded with a custom configuration.

To launch everything, run:
```bash
ros2 launch aruco_detector aruco_detector.launch.py
```