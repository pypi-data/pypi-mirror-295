from setuptools import setup, find_packages

# Read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


def parse_requirements(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

requirements = parse_requirements('requirements.txt')


setup(
    name="nuclearowl", 
    version="1.1.0",  
    description="A lib handling nuclear imaging data and Ai applications on top of it",  # Brief description of your package
    long_description=long_description,  
    long_description_content_type="text/markdown",  
    url="https://github.com/eser-chr/nuclearowl",  
    author="eser-chr",  
    author_email="chriseseroglou@gmail.com",  
    license="MIT",  
    classifiers=[  
        "Development Status :: 3 - Alpha",  
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="nuclear imaging, medical imaging, python, AI(wow), segmentation",  
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),  
    python_requires=">=3.7", 
    install_requires=requirements,
    package_data={  
        "": ["data/*.dat"],  
    }
)
