from setuptools import setup, find_packages
from oh_my_ralph import __version__

setup(
    name="oh-my-ralph",
    version=__version__,
    description="An opinionated orchestrator for Ralph Wiggum loops",
    author="vivganes",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.10",
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vivganes/oh-my-ralph",
    project_urls={
        "Homepage": "https://github.com/vivganes/oh-my-ralph",
        "Repository": "https://github.com/vivganes/oh-my-ralph"
    },
)
