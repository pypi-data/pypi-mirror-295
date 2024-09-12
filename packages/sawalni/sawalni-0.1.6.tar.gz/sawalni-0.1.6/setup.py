from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="sawalni",
    version="0.1.6",
    author="Omar Kamali",
    author_email="api@sawalni.com",
    description="Official Python SDK for the Sawalni API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=["sawalni", "sawalni.*"]),
    package_data={"sawalni": ["*.py"]},
    include_package_data=True,
    install_requires=[
        "requests",
        "aiohttp",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.7",
    keywords="nlp language processing embedding translation identification api sdk moroccan darija arabic multilingual low-resource languages",
)
