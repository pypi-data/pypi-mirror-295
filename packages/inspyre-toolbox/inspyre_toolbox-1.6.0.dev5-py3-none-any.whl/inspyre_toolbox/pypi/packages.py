import subprocess
import sys


def up_to_date(name):
    latest_version = str(
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', f'{name}==random'],
            capture_output=True,
            text=True,
        )
    )

    latest_version = latest_version[latest_version.find('(from versions:') + 15:]
    latest_version = latest_version[:latest_version.find(')')]
    latest_version = latest_version.replace(' ', '').split(',')[-1]

    current_version = str(
        subprocess.run(
            [sys.executable, '-m', 'pip', 'show', f'{name}'],
            capture_output=True,
            text=True,
        )
    )

    current_version = current_version[current_version.find('Version:') + 8:]
    current_version = current_version[:current_version.find(
            '\\n')].replace(' ', '')

    return latest_version == current_version
