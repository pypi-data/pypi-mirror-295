from setuptools import setup, find_packages

setup(
    name="rainbows",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1,<3.0.0",
    ],
    author="rainbow-coalition",
    # author_email="your.email@example.com",
    description="A simple client for the Rainbows API",
    long_description=
    "This library provides a simple interface to interact with the Rainbows API.",
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/rainbows",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
