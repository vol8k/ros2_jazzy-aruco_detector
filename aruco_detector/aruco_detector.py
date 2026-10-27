import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image, CameraInfo
import message_filters

from cv_bridge import CvBridge
import cv2

import tf2_ros

from scipy.spatial.transform import Rotation as R
from geometry_msgs.msg import TransformStamped

import numpy as np

class ArucoDetector(Node):

    MARKER_SIZE = 0.075

    def __init__(self):
        super().__init__('aruco_detector')
        self._bridge = CvBridge()
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
        self.aruco_params = cv2.aruco.DetectorParameters_create()

        self._msg_raw_image = message_filters.Subscriber(self, Image, '/image_raw')
        self._msg_camera_info = message_filters.Subscriber(self, CameraInfo, '/camera_info')

        self._aruco_img_publisher = self.create_publisher(Image, '/image_aruco', 10)

        self._tf2_broadcaster = tf2_ros.TransformBroadcaster(self)

        self.ts = message_filters.ApproximateTimeSynchronizer(
            [self._msg_raw_image, self._msg_camera_info],
            10,
            0.1
        )

        self.ts.registerCallback(self.detect_callback)

    def detect_callback(self, msg_image, msg_camera_info):
        camera_matrix = np.array(msg_camera_info.k).reshape((3, 3))
        dist_coeffs = np.array(msg_camera_info.d)
        cv2_img = self._bridge.imgmsg_to_cv2(msg_image, 'bgr8')
        corners, ids, rejected = cv2.aruco.detectMarkers(cv2_img, self.aruco_dict, parameters=self.aruco_params)

        if ids is not None:
            cv2.aruco.drawDetectedMarkers(cv2_img, corners, ids)

            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                corners, 
                self.MARKER_SIZE, 
                camera_matrix, 
                dist_coeffs
            )

            for i, id in enumerate(ids.flatten()):
                self._broadcast_tf2(id, tvecs[i][0], rvecs[i][0])

                cv2.drawFrameAxes(
                    cv2_img, 
                    camera_matrix, 
                    dist_coeffs, 
                    rvecs[i], tvecs[i], 
                    0.05 
                )

                x = tvecs[i][0][0] * 100
                y = tvecs[i][0][1] * 100
                z = tvecs[i][0][2] * 100

                text = f"X:{x:.1f} Y:{y:.1f} Z:{z:.1f} cm"

                pixel_x = int(corners[i][0][0][0])
                pixel_y = int(corners[i][0][0][1])

                cv2.putText(
                    cv2_img,
                    text, 
                    (pixel_x, pixel_y - 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 0, 0),
                    1,
                    cv2.LINE_AA
                )

        ros2_msg_img = self._bridge.cv2_to_imgmsg(cv2_img, 'bgr8')
        self._aruco_img_publisher.publish(ros2_msg_img)


    def _broadcast_tf2(self, id, tvec, rvec):
        rot_matrix, _ = cv2.Rodrigues(rvec)
        r = R.from_matrix(rot_matrix)
        quaternion = r.as_quat()

        t = TransformStamped()

        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'camera_color_optical_frame'
        t.child_frame_id = f'aruco_{id}'

        t.transform.translation.x = tvec[0]
        t.transform.translation.y = tvec[1]
        t.transform.translation.z = tvec[2]

        t.transform.rotation.x = quaternion[0]
        t.transform.rotation.y = quaternion[1]
        t.transform.rotation.z = quaternion[2]
        t.transform.rotation.w = quaternion[3]

        self._tf2_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)

    aruco_detector = ArucoDetector()

    rclpy.spin(aruco_detector)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    aruco_detector.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
