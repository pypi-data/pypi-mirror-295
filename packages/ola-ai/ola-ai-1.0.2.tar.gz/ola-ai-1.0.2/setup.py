from setuptools import setup, find_packages
import os

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="ola-ai",
    version="1.0.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "PyYAML",
        "openai",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "ola=ola_cli.cli:main",  # Adjust this if your entry point is different
        ],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    # Other metadata like author, license, etc.
)
