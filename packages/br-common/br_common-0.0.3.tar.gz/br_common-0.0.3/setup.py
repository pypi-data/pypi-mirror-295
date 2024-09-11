from setuptools import setup, find_packages

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="br_common",
    version="0.0.3",
    author="Gaurav Mahale",
    author_email="gaurav.mahale@aventior.com",
    description="A python project common code package",
    long_description=long_description,  # Include long description
    long_description_content_type="text/markdown",  # Specify content type as markdown
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
