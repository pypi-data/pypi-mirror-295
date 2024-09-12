from setuptools import setup, find_packages

setup(
    name="rainbows",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1,<3.0.0",
    ],
    author="rainbow-coalition",
    # author_email="your.email@example.com",
    description="brrr",
    long_description=
    "brrrrrrrrrrr",
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/rainbows",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
