from setuptools import setup, find_packages

setup(
    name='nyu-depth-v2',
    version='0.0.2',
    description='NYUv2 Dataset for PyTorch.',
    author='Beomseo Choi',
    author_email='beomseo0707@gmail.com',
    url='https://github.com/BeomseoChoi/NYUv2_Dataset_Pytorch.git',
    install_requires=['torch', 'torchvision', 'numpy', 'opencv-python', 'h5py', 'tqdm', 'einops', 'pathlib'],
    packages=find_packages(exclude=[]),
    keywords=['beomseo choi', 'beomseo0707', 'nyuv2 datasets', 'nyuv2', 'nyu depth'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
