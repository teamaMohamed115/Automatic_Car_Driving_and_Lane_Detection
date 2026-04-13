from setuptools import find_packages, setup

package_name = 'lane_object_detection'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='you@example.com',
    description='Lane and Object Detection via ROS 2 for Raspberry Pi 4.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'publisher_node = lane_object_detection.publisher_node:main',
            'subscriber_node = lane_object_detection.subscriber_node:main',
        ],
    },
)
