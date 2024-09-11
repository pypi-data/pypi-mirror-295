from setuptools import setup, find_packages

def read_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='brrrData',
    version='0.1.0',
    description='A data processing tool for Excel files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Felix Arvidsson',
    author_email='felix.arvidsson@gmail.com',
    url='https://github.com/felix-arvidsson/brrrDataProcessor/',
    packages=find_packages(),
    install_requires=read_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'brrrdata=brrrData.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
