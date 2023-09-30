#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='aws_console',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'aws-console = aws_console.main:main'
        ]
    },
    install_requires=[
        'boto3'
    ],
    author='Snigdhajyoti Ghosh',
    author_email='snigdhasjg@users.noreply.github.com',
    description='AWS Console Login Utility',
    url='https://github.com/snigdhasjg/aws-console',
    license="MIT License",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
)
