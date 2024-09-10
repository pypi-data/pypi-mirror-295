from setuptools import setup, find_packages

setup(
    name='quantsumore',
    version="1.2.1b1",  
    author='Cedric Moore Jr.',
    author_email='cedricmoorejunior5@gmail.com',
    description='A comprehensive Python library for scraping and retrieving real-time data across multiple financial markets, including cryptocurrencies, equities, Forex, treasury yields, and consumer price index (CPI) data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cedricmoorejr/quantsumore/tree/v1.2.1b1',
    project_urls={
        'Source Code': 'https://github.com/cedricmoorejr/quantsumore/releases/tag/v1.2.1-beta.1',
    },
    packages=find_packages(),
    package_data={
        'quantsumore': ['configuration/*.json', 'configuration/*.db'],
        'quantsumore': ['assets/*.ico', 'assets/*.png'],        
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pandas',
        'requests',
        'matplotlib',
        'pillow',
        'numpy',  
    ],
    license='MIT',
    include_package_data=True,
)
