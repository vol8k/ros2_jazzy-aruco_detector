from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='v4l2_camera',
            executable='v4l2_camera_node',
            parameters=[{
                'video_device': '/dev/video0',
            }]
        ),

        Node(
            package='aruco_detector', 
            executable='aruco_detector', 
            output='screen'
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', os.path.join(get_package_share_directory('aruco_detector'), 'rviz', 'aruco_detector.config.rviz')],
            output='screen'
        )
    ])