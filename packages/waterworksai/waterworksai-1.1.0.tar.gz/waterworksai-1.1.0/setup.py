from setuptools import setup, find_packages

setup(
    name='waterworksai',
    version='1.1.0',
    author='D. Rehn',
    description='The official waterworks.ai python API package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),  # Automatically find the packages in your project
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',  # Specify your required Python version
)

