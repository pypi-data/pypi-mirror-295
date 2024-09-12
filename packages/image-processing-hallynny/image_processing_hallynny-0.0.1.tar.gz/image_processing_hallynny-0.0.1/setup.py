from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing_hallynny",
    version="0.0.1",
    author="Hallynnyh",
    description="Image Processing Package using Skimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hallynnyh/DESAFIOS_DIO/tree/main/image_processing_hallynny",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)