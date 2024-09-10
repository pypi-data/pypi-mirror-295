from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='bvlogger',
    version='1.0.4',
    author='Your Name',
    author_email='your.email@example.com',
    description='A brief description of your project',
    long_description=long_description,
    long_description_content_type='text/markdown', 
    url='https://github.com/yourusername/bvlogger',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)