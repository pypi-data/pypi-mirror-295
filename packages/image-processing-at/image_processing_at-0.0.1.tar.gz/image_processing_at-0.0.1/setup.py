from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing_at",
    version="0.0.1",
    author="Arthur Ticianeli",
    description="A package to process images",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arthurticianeli/image_processing",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.6",
)