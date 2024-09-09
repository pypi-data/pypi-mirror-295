import json
from setuptools import setup, find_packages # type:ignore
from pathlib import Path

with open("data.json", "r", encoding="utf-8") as f: data: dict[str, str|list[str]] = json.load(f)

version: str = str(data["version"])
this_directory = Path(__file__).parent
long_description: str = (this_directory / "README.md").read_text()

default_description: str = f"""
# Project
This is my simple python project, which does some simple stuff:
    - Logging
    - Sending data
    - Pinging
    - Getting data (passwords, ...)
    - Displaying notifications
    - Modifying strings
    - Checking connections
    - ...

    
## Functions
Following funcitons are included:
    - {"\n   - ".join(sorted(i.replace("_", " ").capitalize() for i in data["all"]))}


## Settings
You can manage some things in the settings file of the project,
which is directly in the parent folder of it.


## Conclusion
This is a simple package, that performs various tasks,
for that I am too lazy to do them. If you use this package
and do some silly stuff with it, I am not responsible for that!

If you have any questions, just join the discord channel:
https://discord.gg/HvwFgC54UJ

However, this project is very simple, but effective.
"""

setup(
    author="AJ-Holzer",
    description="A simple module which does some simple stuff. Don't make something illegal ;)  Join our discord channel: https://discord.gg/HvwFgC54UJ",
    long_description=long_description,
    default_description=default_description,
    url="https://github.com/AJ-Holzer/AJ-Module",
    license="MIT",
    name='ajpack',
    version=version,
    packages=find_packages(),
    install_requires=[
        "pyzipper",
        "opencv-python",
        "requests",
        "Pillow",
        "keyboard",
        "pywin32",
        "psutil",
        "winshell",
        "plyer",
        "customtkinter",
        "cryptography",
        "pycryptodome",
        "pygame",
        "pynput",
        "pystray"
    ],
    entry_points={
        'console_scripts': [
            # Commands
        ],
    },
)