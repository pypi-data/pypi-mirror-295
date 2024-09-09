import setuptools
from pathlib import Path


def get_install_requirements():
    """
    Extract packages from requirements.txt file to list

    Returns:
        list: list of packages
    """
    fname = Path(__file__).parent / 'requirements.txt'
    targets = []
    if fname.exists():
        with open(fname, 'r') as f:
            targets = f.read().splitlines()
    return targets

setuptools.setup(name='cisco-eth-switch-poe',
                 version='0.0.1',
                 description='python package for cisco ethernet switch POE management',
                 url='https://bitbucket.org/opsys_tech/cisco-eth-switch-poe/src/master/',
                 download_url='https://bitbucket.org/opsys_tech/cisco-eth-switch-poe/src/master/',
                 author='dmitry.borovensky',
                 install_requires=get_install_requirements(),
                 author_email='dmitry.borovensky@opsys-tech.com',
                 packages=setuptools.find_packages(exclude=("test",)),
                 zip_safe=False)
