from setuptools import setup, find_packages

setup(
    name='randize',
    version='1.0.3',
    author='Vladimir',
    author_email='funquenop@gmail.com',
    description='Ultimate Python Randomizer Library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/BlazeDevelop/randize',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pytz',
        'uuid',
        'datetime'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
