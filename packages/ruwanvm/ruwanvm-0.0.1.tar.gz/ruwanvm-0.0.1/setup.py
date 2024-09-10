from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'ruwanvm cli clients'
LONG_DESCRIPTION = 'ruwanvm cli use to various miscellaneous tasks'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="ruwanvm",
    version=VERSION,
    author="Ruwan Vimukthi",
    author_email="ruwanvm@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(include=['ruwanvm', 'ruwanvm.misc']),
    install_requires=[
        'pytz>=2024.1',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        'Operating System :: OS Independent',
    ]
)
