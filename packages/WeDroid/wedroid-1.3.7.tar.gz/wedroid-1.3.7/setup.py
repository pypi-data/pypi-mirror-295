#  Copyright (c) 2019. Steven@oddineers.co.uk

import setuptools
from wedroid import core as wedroid

with open("README.md", "r") as fh:
    long_description = fh.read()

domain = 'https://oddineers.co.uk/applications/'
setuptools.setup(
    name="WeDroid",
    version=wedroid.__version__,
    author="Steven",
    author_email="steven@oddineers.co.uk",
    description="A weather announcement agent that summarises weather in realtime using OpenWeatherMaps; "
                "Features additional support for Android devices using Termux & Tasker.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='weather development, owm',
    url=domain + 'wedroid',
    packages=setuptools.find_packages(
        include=['wedroid'],
        exclude=['tests', 'docs', 'wedroid.settings'],
    ),
    license_files=('LICENSE',),
    install_requires=[
        'certifi>=2024.7.4',
        'chardet>=5.2.0',
        'charset-normalizer>=3.3.2',
        'geojson>=2.5.0',
        'idna>=3.8',
        'pyowm>=3.3.0',
        'PySocks>=1.7.1',
        'requests>=2.32.3',
        'setuptools>=74.0.0',
        'urllib3>=2.2.2',
    ],
    requires_python=">=3.9",
    entry_points={
        'console_scripts': [
            'wedroid=wedroid.core:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        "Operating System :: OS Independent",
        'License :: OSI Approved :: Apache Software License',
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Internet",
        "Topic :: Utilities",
    ],
    project_urls={
        'Documentation': domain + 'wedroid#docs',
        'Say Thanks!': domain + 'wedroid#donate',
        'Source': 'https://gitlab.com/oddineers-public/wedroid',
        'Tracker': 'https://gitlab.com/oddineers-public/wedroid/-/issues',
    },
    package_data={
        '': ['log_config.ini', 'weather.ini', 'translations/announcements.json', 'translations/weather.json'],
    },
    include_package_data=True,
    exclude_package_data={
        'wedroid': ['settings.py', 'settings.json'],
    }
)
