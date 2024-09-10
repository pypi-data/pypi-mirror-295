from setuptools import setup, find_packages

setup(
    name="libaxion_dmx",
    version="1.0.0",
    description="A Python API for controlling Axion Lighting DMX controllers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Vrncanac",
    author_email="jana13eng@gmail.com",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
