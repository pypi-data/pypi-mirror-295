from setuptools import setup, find_packages

setup(
    name='boursocrawling',
    version='1.0.0',
    author='Alexandre Delaisement',
    author_email='',
    description='A module for getting Boursorama Data',
    long_description='A module to get Boursorama stock data, recommendation, and search engine.',
    long_description_content_type='text/markdown',
    url='https://github.com/AlexandreDela/boursocrawling',
    packages=['boursocrawling'],
      package_dir={'boursocrawling': 'src/boursocrawling'},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',

    ],
    keywords='finance',
    python_requires='>=3.8',
    install_requires=[
        "bs4",
        "numpy>=1.21.0",
        "matplotlib>=3.3.0",
        "requests",
        "pytest >= 8.1.1"
    ],
    project_urls={
        'Source': 'https://github.com/AlexandreDela/boursocrawling',
    },
)