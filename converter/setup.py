from setuptools import setup, find_packages

setup(
    name='file-converter',
    version='1.0.0',
    description='Convert between different file formats (CSV, Excel, JSON, TSV, TXT)',
    author='File Converter',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'file-converter=converter.cli:main',
        ],
    },
    install_requires=[
        'openpyxl>=3.0.0',
    ],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Utilities',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
