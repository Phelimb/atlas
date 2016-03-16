Master : [![Build Status](https://travis-ci.com/Phelimb/atlas.svg?token=zS56Z2pmznVQKhUTxqcq&branch=master)](https://travis-ci.com/Phelimb/atlas)

Dev : [![Build Status](https://travis-ci.com/Phelimb/atlas.svg?token=zS56Z2pmznVQKhUTxqcq&branch=dev)](https://travis-ci.com/Phelimb/atlas)

## Installation

git clone **--recursive** git@github.com:Phelimb/atlas.git

### Install requirements mccortex
**NB: You must install the version of mccortex that comes with this repostitory**


	cd atlas
	cd mccortex
	make	
	export PATH=$PATH:$(pwd)/bin
	cd ..


## Install atlas
	
### Install atlas with virtualenv (recommended but optional)

#### Install virtualenv

	https://virtualenv.readthedocs.org/en/latest/installation.html

#### Create virtualenv 

	virtualenv venv

#### Activate the virtualenv

	source venv/bin/activate

You can deactivate at anytime by typing 'deactivate'. 


#### Install atlas


	python setup.py install


## Usage

	usage: atlas [-h] [--version] {add,dump-probes,make-probes,genotype} ...

	optional arguments:
	  -h, --help            show this help message and exit
	  --version             atlas version

	[sub-commands]:
	  {add,dump-probes,make-probes,genotype}
	    add                 adds a set of variants to the atlas
	    dump-probes         dump a panel of variant alleles
	    make-probes         make probes from a list of variants
	    genotype            genotype a sample using a probe set


### Paper, citation 

> [Bradley, Phelim, et al. "Rapid antibiotic-resistance predictions from genome sequence data for Staphylococcus aureus and Mycobacterium tuberculosis."Nature communications 6 (2015).](http://www.nature.com/ncomms/2015/151221/ncomms10063/full/ncomms10063.html)

Please cite us if you use atlas in a publication

All analysis in this paper was done with release [v0.1.3-beta](https://github.com/iqbal-lab/Mykrobe-predictor/releases/tag/v0.1.3-beta).


### Common issues

mccortex fails to make. 

Likely problem: Submodules have not been pulled with the repo. 

Solution : Run 
	
	git pull && git submodule update --init --recursive
	cd mccortex && make

