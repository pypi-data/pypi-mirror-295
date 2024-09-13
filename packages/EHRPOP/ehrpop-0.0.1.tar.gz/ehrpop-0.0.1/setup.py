from setuptools import setup, find_packages

setup(
    name='EHRPOP',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'EHRPOP': ['all_codes.json'],
    },
    install_requires=[
        'numpy','plotly','pandas','regex'
    ],
    author='AZZAG Houssem Eddine',
    author_email='houssem-eddine.azzag@univ-amu.fr',
    description='SNDS Patients caracterzations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/HoussemNeuer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
