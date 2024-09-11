from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="dio_image_processing_project",
    version="0.0.1",    
    author="Dpbm",
    author_email="dpbm136@gmail.com",
    description="A image processing library for DIO's bootcamp",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dpbm/image-processing-dio",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
