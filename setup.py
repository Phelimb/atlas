from setuptools import setup
from setuptools.command.install import install as DistutilsInstall
import subprocess
import os
from mykatlas.version import __version__
__version__ = __version__[1:].split("-")[0]


class MyInstall(DistutilsInstall):

    def run(self):
        mccortex_dir = os.path.dirname(os.path.realpath(__file__))+"/mccortex"
        subprocess.call(
            ["make", "clean"], cwd=mccortex_dir)
        subprocess.call(
            ["make"], cwd=mccortex_dir)
        print("Moving mccortex from %s to %s" %
              (mccortex_dir, os.environ.get('VIRTUAL_ENV', '/usr/local/')))
        subprocess.call(
            ["cp", "bin/mccortex31", "%s/bin/" % os.environ.get('VIRTUAL_ENV', '/usr/local/')], cwd=mccortex_dir)
        DistutilsInstall.run(self)

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
        'mykatlas.cortex',
        'mykatlas.analysis'],
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
            'atlas = mykatlas.atlas_main:main',
        ]},
    cmdclass={'install': MyInstall})
