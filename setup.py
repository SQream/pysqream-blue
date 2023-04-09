from setuptools import setup, find_packages
from pysqream_blue.globals import __version__

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as req:
    requires = req.read().split('\n')[:-1]

setup_params = dict(
    name =          'pysqream-blue',
    version =       __version__,
    description =   'DB-API connector for SQream DB', 
    long_description_content_type = long_description,
    url = "https://github.com/SQream/pysqream-blue",
    author = "SQream",
    author_email = "info@sqream.com",
    packages = ["pysqream_blue", "protos"],
    classifiers = [
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    keywords = 'database db-api sqream sqreamdbV2',
    python_requires = '>=3.9',
    install_requires=requires
)

if __name__ == '__main__':
    setup(**setup_params)
