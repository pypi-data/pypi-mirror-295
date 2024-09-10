from setuptools import setup, find_packages

setup(
    name='quantaforgepylib',  # Replace with your package’s name
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    author='Smisch',  
    author_email='ceo@quantaforge.dev',
    description='A library of fancy python tools',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',

)