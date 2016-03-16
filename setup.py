from setuptools import setup
setup(
    name='mykatlas',
    version='0.0.1.3',
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
