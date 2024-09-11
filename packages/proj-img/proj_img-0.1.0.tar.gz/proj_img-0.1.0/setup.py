
from setuptools import setup, find_packages

setup(
    name='proj_img',
    version='0.1.0',
    description='A simple image processing package',
    author='leopxz',
    author_email='pxleonarddo@gmail.com',
    url='https://github.com/leopxz/processamento_de_imagens',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pillow',
        'opencv-python'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
