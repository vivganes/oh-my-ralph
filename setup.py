from setuptools import setup, find_packages

setup(
    name="ralphy",
    version="0.1.0",
    description="A Python project for ralphy.",
    author="vivganes",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.7",
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vivganes/ralphy",
    project_urls={
        "Homepage": "https://github.com/vivganes/ralphy",
        "Repository": "https://github.com/vivganes/ralphy"
    },
)
