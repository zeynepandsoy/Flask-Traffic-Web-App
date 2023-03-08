from setuptools import setup

setup(
    name='traffic_app',
    packages=['traffic_app'],
    include_package_data=True,
    install_requires=[
            'flask',
    ],
)