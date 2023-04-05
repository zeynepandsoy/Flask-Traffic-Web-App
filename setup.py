from setuptools import setup, find_packages

setup(
  name="traffic_app",
  packages=find_packages(), # or packages=['traffic_app'],
  include_package_data=True,
  install_requires=[
    "flask",
    "flask-wtf",
    "flask-sqlalchemy",
    "Flask-WTF",
    "flask-marshmallow",
    "marshmallow-sqlalchemy",
    "flask-login",
    "pandas",
    "requests",
  ],
)
