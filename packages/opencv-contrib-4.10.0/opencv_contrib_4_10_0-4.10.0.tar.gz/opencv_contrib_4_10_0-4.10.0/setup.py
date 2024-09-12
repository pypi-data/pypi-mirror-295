from setuptools import setup, find_packages
import codecs
import os




VERSION = '4.10.0'
DESCRIPTION = 'opencv_contrib-4.10.0'


# Setting up
setup(
    name="opencv_contrib-4.10.0",
    version=VERSION,
    author="Malyoneeeeer",
    author_email="<malyoneeeeer@yahoo.com>",
    description=DESCRIPTION,
    include_package_data=True,
    packages=['libname'],
    package_data={'libname': ['models/*.*']},
    install_requires=['opencv-python'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
