from setuptools import setup, find_packages

setup(
    name='cronos_chain_client',
    version='0.1.0',
    description='A Python client for interacting with the Cronos Chains',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cronos-labs/cronos-chain-client/tree/main/py', 
    author='rarcifa',
    author_email='rarcifa@gmail.com',
    license='MIT',
    packages=find_packages(),  
    install_requires=[],  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
