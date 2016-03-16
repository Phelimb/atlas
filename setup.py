from setuptools import setup
from pip.req import parse_requirements
import atlas.version
install_reqs = parse_requirements('requirements.txt')
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='atlas',
    version='0.0.1',
    packages=[
        'atlas',
        'atlas.cmds',
        'atlas.pheno',
        'atlas.typing',
        'atlas.typing.typer',
        'atlas.typing.models',,
        'atlas.stats',
        'atlas.cortex',
        'atlas.metagenomics'],
    license='MIT',
    url='http://github.com/phelimb/atlas',
    description='.',
    author='Phelim Bradley',
    author_email='wave@phel.im',
    install_requires=reqs,
    entry_points={
            'console_scripts': [
                'atlas = atlas.atlas_main:main',
            ]})
