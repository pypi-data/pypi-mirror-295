from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cybersentry',  
    version='0.1.4',
    packages=find_packages(),  
    install_requires=[
        'aiohttp>=3.7,<4.0',
        'beautifulsoup4>=4.9.3,<5.0',
        'dnspython>=2.0.0',
        'colorama>=0.4.0',
        'pyOpenSSL>=20.0.0',
        'aiodns>=3.0.0',
        'tqdm>=4.0.0',
        'greenlet<1.2',  
        'Cython>=0.29.0',
        'gevent==21.12.0',
        'setuptools>=40.8.0',
        'wheel>=0.34.0'
    ],
    author='Luca Lorenzi',  
    author_email='info@orizon.one',  
    description='Advanced Cybersecurity Intelligence Tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Lxsanto/cybersentry', 
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Security',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'cybersentry=cybersentry.core:run',  
        ],
    },
)