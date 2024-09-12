from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="simple_timer_plus",
    version="0.0.1",
    author="Orlando Gomes",
    author_email="gomes.oa@gmail.com",
    description="A simple timer to measure task durations.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/orlandoabreugomes/simple-timer",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.6',
)
