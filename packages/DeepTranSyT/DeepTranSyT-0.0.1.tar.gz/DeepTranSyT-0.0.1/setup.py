from setuptools import setup, find_packages

setup(
    name='DeepTranSyT',
    version='0.0.1',
    description="Transporters annotation using LLM's",
    author='Gonçalo Apolinário Cardoso',
    author_email='goncalocardoso2016@gmail.com',
    packages=find_packages(),  
    install_requires=[ 
       "Bio==1.7.1",
       "biopython==1.83",
        "fair_esm==2.0.0",
        "matplotlib==3.9.2",    #"propythia==3.0.2",
        "numpy==1.26.4",
        "pandas==2.2.2",
        "pytorch_lightning==2.2.5",
        "scikit_learn==1.2.0",
        "tensorflow==2.17.0",
        "torch==2.3.0",
        "torchmetrics==1.4.0.post0"
    ],
    entry_points={
        'console_scripts': [
            'run-predictions=DeepTranSyT.main:main',
        ],
    },
)