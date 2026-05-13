from setuptools import find_packages, setup
import os

package_name = 'lane_object_detection'

model_files = []
models_dir = os.path.join(os.path.dirname(__file__), 'models')
if os.path.isdir(models_dir):
    for f in os.listdir(models_dir):
        if f.endswith('.param') or f.endswith('.bin'):
            model_files.append(os.path.join('models', f))

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/models', model_files),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='you@example.com',
    description='Lane following via UNet NCNN on ROS 2 for Raspberry Pi 4.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'lane_following_node = lane_object_detection.publisher_node:main',
            'lane_viewer_node = lane_object_detection.subscriber_node:main',
        ],
    },
)
