from setuptools import setup, find_packages

setup(
    name="findatamarket",  # The name of your package
    version="0.8",
    author="Serkin Alexander",
    author_email="serkin.alexander@gmail.com",
    description="SDK for getting financial data from findata.market",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/serkin/findata-market",  # Replace with your package's URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'pandas'
    ],
)
