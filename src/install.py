#!/usr/bin/env python3
import subprocess
import sys

required_packages = [
    'pandas',
    'yfinance',
    'numpy',
    'pytz'
]

def install_package(package):
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def main():
    for package in required_packages:
        try:
            __import__(package)
            print(f"{package} is already installed.")
        except ImportError:
            install_package(package)

if __name__ == '__main__':
    main()
