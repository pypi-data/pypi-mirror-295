from setuptools import setup, find_packages

setup(
    name='pychatbgp',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['requests>=2.24.0'],  # If you have dependencies, list them here
    author='Thomas Holterbach and Thomas Alfroy',
    author_email='contact@bgproutes.io',
    description='A Python library to get BGP data from the ChatBGP API',
    url='https://github.com/yourusername/pychatbgp',  # Update this to your repo URL
    classifiers=[ ],
    python_requires='>=3.6'
)
