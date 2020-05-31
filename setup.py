from setuptools import setup, find_packages

setup(
    name="roll-for-stats",
    version="1.0.0",
    author="Colin Gray",
    author_email="colinta@colinta.com",
    url="https://github.com/colinta/roll",
    description="A library for rolling dice and collecting probability stats",
    long_description=open("README.md").read(),
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": ["roll = roll:main"]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Games/Entertainment :: Role-Playing",
        "Topic :: Games/Entertainment :: Multi-User Dungeons (MUD)",
        "Topic :: Games/Entertainment :: Turn Based Strategy",
        "Topic :: Utilities",
    ],
)
