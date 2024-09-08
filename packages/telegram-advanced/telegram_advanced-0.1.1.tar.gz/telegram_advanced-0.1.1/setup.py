from setuptools import setup, find_packages

setup(
    name="telegram_advanced",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        # Add other dependencies here
    ],
    author="LCF",
    author_email="your.email@example.com",
    description="An advanced Telegram bot library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/telegram_advanced",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)