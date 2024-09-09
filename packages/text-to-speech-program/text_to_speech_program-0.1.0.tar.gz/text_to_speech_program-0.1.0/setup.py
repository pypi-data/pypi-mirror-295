#!/usr/bin/python3

from setuptools import setup, find_packages

setup(
    name='text_to_speech_program',
    version='0.1.0',
    description='A text-to-speech server and client using gtts and pydub',
    author='Fernando Pujaico Rivera',
    author_email='fernando.pujaico.rivera@gmail.com',
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
)
