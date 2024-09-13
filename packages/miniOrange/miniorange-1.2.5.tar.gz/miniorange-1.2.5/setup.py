from setuptools import setup, find_packages

VERSION = '1.2.5'
DESCRIPTION = 'OAuth Implementation With SSo'
LONG_DESCRIPTION = 'A library for OAuth2 authorization with MiniOrange'

# Setting up
setup(
    name="miniOrange",
    version=VERSION,
    author="Ayushi Agrawal",
    author_email="ashayuparth@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)