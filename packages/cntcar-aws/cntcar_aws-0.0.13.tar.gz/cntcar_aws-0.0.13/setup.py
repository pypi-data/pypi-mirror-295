from setuptools import setup, find_packages

setup(
    name='cntcar_aws',
    version='0.0.13',
    description='Python library for AWS services used in ConectCar projects',
    long_description_content_type="text/markdown",
    long_description='README.md',
    author='Marcos Lemes',
    classifiers=[
                "Development Status :: 3 - Alpha",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.8"],
    packages=find_packages(),
    install_requires=[
        'boto3',
        'croniter'
    ]
)