from setuptools import setup, find_packages

setup(
    name='cybersentry',  
    version='0.1.0',
    packages=find_packages(),  
    install_requires=[
        'aiohttp',
        'beautifulsoup4',  
        'dnspython',
        'colorama',
        'pyOpenSSL',
        'aiodns',
        'subfinder',
        'tqdm'
    ],
    author='Luca Lorenzi',  
    author_email='info@orizon.one',  
    description='Advanced Cybersecurity Intelligence Tool  ',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Lxsanto/cybersentry/tree/main/cybersentry', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
