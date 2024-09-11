from setuptools import setup, find_packages
import codecs
import os




VERSION = '0.0.3'
DESCRIPTION = 'opencv facemodel'


# Setting up
setup(
    name="adeopencv",
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
