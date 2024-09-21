from setuptools import find_packages, setup

package_name = 'test_gps'

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
    maintainer='Filip',
    maintainer_email='filipp@my.yorku.ca',
    description='Publishes simulated GCS coordinates and checks for arithmatic consistency',
    license='Copyright York University Robotics Society',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'test_gps = test_gps.test_gps:main', 
            'check = test_gps.check:main'
        ],
    },
)
