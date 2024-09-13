from setuptools import setup, find_packages

# Read requirements.txt
with open('quantgrid_cli/requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='quantgrid-cli',
    version='0.1.3',
    author='Anthony Martin',
    author_email='contact@quantgrid.net',
    description='A CLI for managing QuantGrid projects and workflows',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://quantgrid.net',
    
    packages=find_packages(include=['quantgrid_cli', 'quantgrid_cli.*']),


    # Ensure package_data points to the correct directory
    package_data={
        'quantgrid_cli': ['boilerplate/*'],  # Make sure the boilerplate path is correct
    },
    include_package_data=True,
    
    # Install dependencies from requirements.txt
    install_requires=requirements,
    
    # Entry points for your CLI tools
    entry_points={
        'console_scripts': [
            'quantgrid=quantgrid_cli.cli:cli',  # Reference the correct function
            'qg=quantgrid_cli.cli:cli',
        ],
    },

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
