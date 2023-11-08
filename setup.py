#!/usr/bin/env python
import re
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='aws_console',
    version=find_version('aws_console', '__init__.py'),
    description='AWS Console Login Utility',
    keywords = [
        'aws',
        'aws-sdk',
        'aws-cli',
        'aws-authentication',
        'aws-sdk-python',
        'aws-auth'
    ],
    long_description=read("README.md"),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'aws-console = aws_console:aws_console',
            'aws-system-credential = aws_console:aws_system_credential'
        ]
    },
    install_requires=[
        'boto3>=1.28',
        'pyperclip>=1.8,<1.9',
        'keyring>=24.2,<24.3'
    ],
    author='Snigdhajyoti Ghosh',
    author_email='snigdhajyotighos.h@gmail.com',
    url='https://github.com/snigdhasjg/aws-console',
    license="MIT License",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities'
    ],
)
