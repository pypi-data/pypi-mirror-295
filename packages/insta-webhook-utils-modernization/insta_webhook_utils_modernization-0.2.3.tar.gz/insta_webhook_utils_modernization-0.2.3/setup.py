import os

from Cython.Build import cythonize
from setuptools import setup, find_packages


def find_python_files(directory):
    return [os.path.join(root, file)
            for root, dirs, files in os.walk(directory)
            for file in files
            if file.endswith('.py') and not file.startswith('__init__')]


setup(
    name='insta_webhook_utils_modernization',
    version='0.2.3',
    packages=find_packages(),
    ext_modules=cythonize(find_python_files("insta_webhook_utils_modernization")),
    install_requires=[
        'Cython',
        'jsonschema',
        'pytz',
        "requests",
        "aiohttp"
    ],
    author='Sheikh Muhammed Shoaib',
    author_email='shoaib.sheikh@locobuzz.com',
    description='This package contains the utility functions for Instagram Webhook',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/LocoBuzz-Solutions-Pvt-Ltd/insta_webhook_utils_modernization',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
