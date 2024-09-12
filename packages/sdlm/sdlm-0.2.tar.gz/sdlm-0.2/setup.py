from setuptools import setup, find_packages

with open("README.md", "r") as a:
    description = a.read()

setup(
    name='sdlm',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'requests>=2.32.3',
        'bs4>=0.0.2',
    ],
    entry_points={
        "console_scripts": [
            "sdlm = sdlm:main"
        ]
    },
    long_description=description,
    long_description_content_type="text/markdown",
)
