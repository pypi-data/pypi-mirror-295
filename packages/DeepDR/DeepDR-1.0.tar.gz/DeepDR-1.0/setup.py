from setuptools import setup, find_packages

setup(
    name='DeepDR',
    version='v1.0',
    description='A deep learning library for drug response prediction',
    packages=find_packages(),
    keywords=[
        'Drug response',
        'Deep learning',
        'Python library'
    ],
    install_requires=[
        'torch>=1.10.0',
        'torchvision>=0.11.0',
        'torchaudio>=0.10.0',
        'joblib',
        'rdkit',
        'openpyxl',
        'pubchempy',
        'wandb',
        'torch_geometric>=2.0.3',
        'torch_scatter',
        'torch_sparse',
        'torch_cluster',
        'torch_spline_conv'
    ],
    include_package_data=True,
    package_data={'': ['DefaultData/*']},
    author='Zhengxiang Jiang, and Pengyong Li',
    author_email='21009101410@xidian.edu.cn',
    license='Apache 2.0'
)
