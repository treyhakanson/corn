from setuptools import setup

setup(
    name='Corn',
    version='0.1',
    long_description=open('README.md').read(),
    packages=['corn'],
    install_requires=[
        'opencv-contrib-python'
    ]
)
