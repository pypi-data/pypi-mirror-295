from setuptools import setup, find_packages

# Read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Get version without importing the package
def get_version():
    with open('src/datasience_methods/__init__.py', 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"').strip("'")
    raise RuntimeError('Unable to find version string.')

setup(
    name="datasience_methods",
    version=get_version(),
    author="Bratet",
    author_email="ahmedmrabet.002@gmail.com",
    description="A collection of useful data science methods",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bratet/datasience_methods",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0.0",
        "fuzzywuzzy>=0.18.0",
        "python-Levenshtein>=0.12.0",
        "jellyfish==0.9.0"
    ],
    extras_require={
        "dev": ["pytest>=6.0", "pytest-cov>=2.0"],
    },
)