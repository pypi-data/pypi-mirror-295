from setuptools import setup, find_packages

setup(
    name='Resource-Packer',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'assetpack=Source.AssetPack:main'
        ]
    },
    install_requires=[
    ],
    author='R00tDroid',
    description='A commandline tool to convert assets into source code',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/R00tDroid/ResourcePacker',
    license='MIT',
)
