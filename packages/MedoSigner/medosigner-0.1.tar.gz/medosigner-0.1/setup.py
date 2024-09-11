from setuptools import setup, find_packages
setup(
    name='MedoSigner',
    version='0.1',
    packages=find_packages(),
    description='A brief description of my library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MohammedNajih/signer-zziqz', 
    author='Mohamed Almuswi',
    author_email='mmaa58027@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', 
)
