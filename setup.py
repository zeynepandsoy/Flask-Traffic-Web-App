from setuptools import setup, find_packages

#check week-9-complete code to add more setup packages i.e. pandas..
setup(
  name="traffic_app",
  packages=find_packages(), #packages=['traffic_app'],
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
