from setuptools import setup, find_packages

setup(
    name='TCRA',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'scipy',
        'folium',
    ],
    description='A Python package for estimating cyclone hazard parameters and calculating wind speeds at structure sites.',  # Make sure this is under 512 characters
    long_description=open('README.md').read(),  # Detailed description is handled by this field
    long_description_content_type='text/markdown',
    url='https://github.com/rxm562/TCRA.git',
    author='Ram Krishna Mazumder',
    author_email='rkmazumder@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    )