from setuptools import setup, find_packages

setup(
    name="ready2order-api-wrapper",
    version="0.1.8",  # Incremented version number
    packages=find_packages(),  # Automatically discover all modules
    install_requires=[
        "requests",
        "pandas",  # Include pandas since it's used in your modules
    ],
    author="Joan Arau",
    author_email="arau.j@zinnfiguren.de",
    description="A Python wrapper for the Ready2Order API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Wilhelm-Schweizer/ready2order_api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)