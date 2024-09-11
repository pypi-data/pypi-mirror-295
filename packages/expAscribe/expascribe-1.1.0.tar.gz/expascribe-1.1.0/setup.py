from setuptools import setup, find_packages

setup(
    name='expAscribe',
    version='1.1.0',
    author='$3@6iRd5h0r3',
    description='DAG casual discovery and analysis',
    #long_description=open('README.md').read(),
    #long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    install_requires=[
        'causal_learn==0.1.3.8',
        'causalnex==0.12.1',
        'dagma==1.1.1',
        'dowhy==0.11.1',
        'matplotlib==3.8.4',
        'networkx==3.2.1',
        'numpy==1.23.0',
        'pandas==1.5.3',
        'python_igraph==0.11.6',
        'scikit_learn==1.5.1',
        'scipy==1.11.4',
        'statsmodels==0.14.2',
        'torch==2.4.0',
        'bayesian-optimization==1.4.2',
    ],
)
