from glob import glob
import os

from setuptools import find_packages, setup

package_name = 'aruco_detector'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        ('share/' + package_name + '/rviz', ['rviz/aruco_detector.config.rviz']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vol8k',
    maintainer_email='karol.bartnicki@onet.pl',
    description='Node that integrates OpenCV for ArUco marker detection, ID decoding and 3D pose esimation.',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'aruco_detector = aruco_detector.aruco_detector:main'
        ],
    },
)
