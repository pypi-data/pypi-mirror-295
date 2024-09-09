from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of the README file
README = (Path(__file__).parent / 'README.md').read_text()

setup(
    name='santali_textts',
    version='0.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'santali-audio=santali_audio:main'
        ]
    },
    description='Convert Olchiki text into speech (Beta version)',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Shivnath Kisku',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
