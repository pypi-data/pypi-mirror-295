from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Erico-Image-Processing",
    version="0.0.1",
    author="Erico Couto Jr.",
    author_email="erico.coutojr@gmail.com",
    description="## Descrição",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EricoCoutoJr/image-processing-package.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)