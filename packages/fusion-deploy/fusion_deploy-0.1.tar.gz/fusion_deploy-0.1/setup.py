from setuptools import setup, find_packages

setup(
    name='fusion_deploy',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'fusion-deploy=fusion_deploy.fusion_deploy:main',
        ],
    },
    author='Michael Sanchez',
    author_email='michael.sanchez@lucidworks.com',
    description='A CLI tool to deploy Fusion 5 to GKE',
    url='https://github.com/lilocruz/fusion_deploy',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)