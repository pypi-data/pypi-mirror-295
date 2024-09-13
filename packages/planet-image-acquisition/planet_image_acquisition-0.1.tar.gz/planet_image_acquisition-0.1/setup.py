from setuptools import setup, find_packages

# Read the contents of requirements.txt
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='planet_image_acquisition',
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,
    author='Megharaj Neupane',
    author_email='neupanemegh888@gmail.com',
    description='A package for acquiring and processing Planet images',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/planet_image_acquisition',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)