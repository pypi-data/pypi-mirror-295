from setuptools import setup, find_packages

setup(
    name='axologgle',
    version='1.0.0',
    description='Logging tools but cooler',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/LiterallyAxo/AxoLoggle',
    author='Axo',
    author_email='axo@itsaxo.lol',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=['colorama'],
)
