from setuptools import setup, find_packages
from weapondetector import __version__

setup(
    name='weapondetector',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6, <4',
    entry_points={
        "console_scripts": [
            "weapondetector=weapondetector.main:main"
        ],
    },
)
