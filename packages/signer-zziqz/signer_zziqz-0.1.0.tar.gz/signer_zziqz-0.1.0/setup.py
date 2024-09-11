from setuptools import setup, find_packages

setup(
    name='signer-zziqz',
    version='0.1.0',
    author='MohamedNajih',
    author_email='mmaa58027@gmail.com',
    description='Signer TikTok.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MohammedNajih/signer-zziqz',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
)
