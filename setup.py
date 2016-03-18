from setuptools import setup
from mykatlas.version import __version__
setup(
    name='mykatlas',
    version=__version__,
    packages=[
        'mykatlas',
        'mykatlas.cmds',
        'mykatlas.typing',
        'mykatlas.typing.typer',
        'mykatlas.typing.models',
        'mykatlas.stats',
        'mykatlas.cortex'],
    license='MIT',
    url='http://github.com/phelimb/atlas',
    description='.',
    author='Phelim Bradley',
    author_email='wave@phel.im',
    install_requires=[
            'future',
            'Biopython',
            'mongoengine',
            'pyvcf',
            'ga4ghmongo'],
    entry_points={
        'console_scripts': [
            'atlas = atlas.atlas_main:main',
        ]})
