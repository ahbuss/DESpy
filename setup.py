from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='DESpy',
    version='1.0.0',
    packages=['simkit', 'simkit.examples'],
    url='https://github.com/ahbuss/DESpy',
    license='Apache 2.0 License',
    author='Arnold Buss',
    author_email='abuss@nps.edu',
    description='Support for DES Modeling using Event Graphs',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
