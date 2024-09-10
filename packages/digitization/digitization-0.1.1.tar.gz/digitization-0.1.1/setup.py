from setuptools import setup, find_packages

# Read the requirements from the requirements.txt file
def parse_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]

# List of dependencies
requirements = parse_requirements('requirements.txt')

setup(
    name='digitization',
    version='0.1.1',
    description='This SDK is for Data Digitization.',
    author='Sushree Sonali Panda',
    author_email='sushree.panda@zs.com',
    packages=find_packages(),  # This finds all packages and sub-packages
    install_requires=requirements,  # Reads dependencies from requirements.txt
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)