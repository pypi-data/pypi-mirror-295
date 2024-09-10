# setup.py

from setuptools import setup, find_packages

setup(
    name='trendline',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
    ],
    description='A library for calculating trendlines for financial data.',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/trendline',  # Update with your repository URL if available
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
