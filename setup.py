#!/usr/bin/env python
import re
import os
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install_scripts import install_scripts
import configparser

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

def update_aws_cli_alias(command_subclass):
    """
    A decorator for classes subclassing one of the setuptools commands.
    It modifies the run() method so that it prints a friendly greeting.
    """
    orig_run = command_subclass.run
    CLI_DIR = os.path.expanduser(os.path.join('~', '.aws', 'cli'))

    def create_alias(config: configparser.ConfigParser):
        if not config.has_section('toplevel'):
            config.add_section('toplevel')
        config['toplevel']['console'] = '!aws-console'
        config['toplevel']['credential-process-from-system'] = '!aws-credential-process-from-system'

    def update_aws_cli_alias_file():
        if not os.path.isdir(CLI_DIR):
            os.makedirs(CLI_DIR)
        cli_alias_full_path = os.path.join(CLI_DIR, 'alias')
        config = configparser.ConfigParser()

        if os.path.isfile(cli_alias_full_path):
            config.read(cli_alias_full_path)

        create_alias(config)

        with os.fdopen(os.open(cli_alias_full_path, os.O_WRONLY | os.O_CREAT, 0o600), 'w') as f:
            f.truncate()
            config.write(f)
    
    def modified_run(self):
        orig_run(self)
        update_aws_cli_alias_file()

    command_subclass.run = modified_run
    return command_subclass

@update_aws_cli_alias
class CustomDevelopCommand(develop):
    pass

@update_aws_cli_alias
class CustomInstallScriptsCommand(install_scripts):
    pass


setup(
    name='aws_console',
    version=find_version('aws_console', '__init__.py'),
    description='AWS Console Login Utility',
    keywords=[
        'aws',
        'aws-sdk',
        'aws-cli',
        'aws-authentication',
        'aws-sdk-python',
        'aws-auth'
    ],
    long_description=read("README.md"),
    packages=find_packages(),
    cmdclass={
        'develop': CustomDevelopCommand,
        'install_scripts': CustomInstallScriptsCommand
    },
    entry_points={
        'console_scripts': [
            'aws-console = aws_console:aws_console',
            'aws-credential-process-from-system = aws_console:aws_credential_process_from_system'
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
