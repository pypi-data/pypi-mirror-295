from setuptools import setup, find_packages

setup(
    name='AKFDTD',
    version='0.2.2',
    author="Alexander V. Korovin",
    author_email="a.v.korovin73@gmail.com",
    url='http://avkor.epizy.com',  # Homepage URL
    # packages=find_packages(),
    packages=['FDTD'],
    package_dir={
    'FDTD': './FDTD',
    },  # Optional: specify the root directory of your package
    include_package_data=True,  # Include files specified in MANIFEST.in
    # package_data={
        # '': ['./tests/*.py'],  # Include test files
        # '': ['./images/*.png', './images/*.jpg'],  # Include all PNG and JPG files in the images directory
    # },
    install_requires=[
        'numpy',
        'matplotlib',
        ],  # Add any dependencies here
    description='Finite difference time domain simulation (for slit diffraction)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='MIT',  # License type
)
