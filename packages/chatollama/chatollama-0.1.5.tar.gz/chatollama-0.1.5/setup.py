from setuptools import setup, find_packages

setup(
    name='chatollama',
    version='0.1.5',
    author='Matthew Sanchez',
    author_email='xxspicymelonxx@gmail.com',
    description='A simple interface for running chat based ollama models in code',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=[
        'ollama',
    ],
)
