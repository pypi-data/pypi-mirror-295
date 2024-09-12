from setuptools import setup, find_packages

setup(
    name='PN_DTW_FE',
    version='0.9.0',
    packages=find_packages(),
    install_requires=[

    ],
    entry_points={
        'console_scripts': [
            'PNdtwFE=PN_DTW_FE.main:run_pndtwfe',
            'SeedConsistency=PN_DTW_FE.main:run_seedconsistency',
        ],
    },
    author='Md Khairul Islam, Prof Hairong Wei',
    author_email='hairong@mtu.edu',
    description='A package for gene expression analysis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/PN_DTW_FE',  # Update with the actual URL if available
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10.3',
)
