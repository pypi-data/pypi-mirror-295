#!/usr/bin/python3

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8");

setup(
    name='text_to_speech_program',
    version='0.1.1',
    description='A text-to-speech server and client using gtts and pydub',
    author='Fernando Pujaico Rivera',
    author_email='fernando.pujaico.rivera@gmail.com',
    maintainer='Fernando Pujaico Rivera',
    maintainer_email='fernando.pujaico.rivera@gmail.com',
    url='https://github.com/trucomanx/text_to_speech_program',
    keywords="tts, gtts, server",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    packages=find_packages(),
    install_requires=[
        'Flask',
        'gtts',
        'pydub',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'tts-program-server=text_to_speech_program.server:main',
            'tts-program-client=text_to_speech_program.client:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    package_data={
        'text_to_speech_program': ['icons/text_to_speech_program.png'],
    },
    include_package_data=True,
    project_urls={  # Optional
        "Bug Reports": "https://github.com/trucomanx/text_to_speech_program/issues",
        "Funding": "https://trucomanx.github.io/en/funding.html",
        "Say Thanks!": "http://saythanks.io/to/example",
        "Source": "https://github.com/trucomanx/text_to_speech_program/",
    },
)
