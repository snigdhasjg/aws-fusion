import inquirer
import boto3
import os
import sys


def setup(subparsers, parent_parser):
    summary = 'Switching between aws config'
    parser = subparsers.add_parser('config-switch', description=summary, help=summary, parents=[parent_parser])

    switch_subparsers = parser.add_subparsers(dest='switch_command', required=True, help='Available switch commands')

    profile_switch_summary = "Switch between available aws profile"
    profile_switch_parser = switch_subparsers.add_parser('profile', description=profile_switch_summary, help=profile_switch_summary, parents=[parent_parser])
    profile_switch_parser.set_defaults(func=switch_profile)

    region_switch_summary = "Switch between available aws region"
    region_switch_parser = switch_subparsers.add_parser('region', description=region_switch_summary, help=region_switch_summary, parents=[parent_parser])
    region_switch_parser.set_defaults(func=switch_region)


def switch_profile(args):
    session = boto3.Session(region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION")), profile_name=os.getenv("AWS_PROFILE"))
    available_profiles = session.available_profiles

    questions = [
        inquirer.List(
            "profile",
            message="Choose a profile",
            choices=available_profiles,
            default=session.profile_name,
            carousel=True
        ),
    ]

    answers = inquirer.prompt(questions, theme=inquirer.themes.GreenPassion())
    profile = answers.get('profile')
    command = '$env:' if sys.platform == 'win32' else 'export '
    print(f'{command}AWS_PROFILE="{profile}"')


def switch_region(args):
    session = boto3.Session(region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION")), profile_name=os.getenv("AWS_PROFILE"))
    available_regions = session.get_available_regions('ec2')

    questions = [
        inquirer.List(
            "region",
            message="Choose a region",
            choices=available_regions,
            default=session.region_name,
            carousel=True
        ),
    ]

    answers = inquirer.prompt(questions, theme=inquirer.themes.GreenPassion())
    region = answers.get('region')
    command = '$env:' if sys.platform == 'win32' else 'export '
    print(f'{command}AWS_REGION="{region}"')
