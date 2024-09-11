from setuptools import setup

setup(
    name='signer_zziqz',
    version='9.1.0',
    url='https://github.com/MohammedNajih/signer-zziqz.git',
    license='MIT',
    description='a python module for signing tiktokv',
    keywords='signing',
    long_description=open('README.md').read(),
    author='Mohamed Almuswi',
    author_email='mmaa58027@gmail.com',
    packages=['signer_zziqz'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'pycryptodome',
    ],
)
