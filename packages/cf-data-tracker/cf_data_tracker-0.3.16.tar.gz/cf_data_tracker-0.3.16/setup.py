from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cf_data_tracker',
    version='0.3.16',  # Update the version number
    author='Rami, R. K',
    author_email='ramireddykowaluru@gmail.com',
    description='A package for managing raw and clean data tracker operations',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires='>=3.9',
    install_requires=[
        'boto3',
        'python-dotenv',
        'beautifulsoup4',
        'boto3',
        'botocore',
        'bs4',
        'certifi',
        'charset-normalizer',
        'idna',
        'jmespath',
        'python-dateutil',
        'python-dotenv',
        'requests',
        's3transfer==0.10.0',
        'six',
        'soupsieve',
        'urllib3',
    ],
)