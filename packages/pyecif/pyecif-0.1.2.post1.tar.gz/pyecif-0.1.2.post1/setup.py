from setuptools import find_packages, setup

setup(
    name='pyecif',
    version='0.1.2.post1',
    packages=find_packages(),
    include_package_data=True,
    description='ECIF file format tools for Python.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Cui Yaning',
    author_email='emotionor@gmail.com',
    url='https://github.com/emotionor/ecif',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        'numpy>=1.18.5',
        'pandas>=2.0.0',
        'pymatgen>=2023.8.10',
        'gemmi',
    ],
    data_files=['README.md'],
)