from setuptools import setup, find_packages


setup(
    name='kupiapi',
    version='1.0.10',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    author="Vojtech Orava",
    author_email="vojtech.orava@gmail.com",
    description="Scraper API for extracting product data from kupi.cz",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/vorava/kupiapi",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
