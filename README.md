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

### Make probes

(venv)-bash-4.1$ ./mykatlas/atlas_main.py make-probes --help
usage: atlas make-probes [-h] [--db_name db_name] [-q] [-v VARIANT] [-f FILE]
                         [-g GENBANK] [-k KMER]
                         reference_filepath

positional arguments:
  reference_filepath    reference_filepath

optional arguments:
  -h, --help            show this help message and exit
  --db_name db_name     db_name
  -q, --quiet           do not output warnings to stderr
  -v VARIANT, --variant VARIANT
                        Variant in DNA positions e.g. A1234T
  -f FILE, --file FILE  File containing variants as rows A1234T
  -g GENBANK, --genbank GENBANK
                        Genbank file containing genes as features
  -k KMER, --kmer KMER  kmer length

### Examples

	mykrobe make-probes -t example-data/staph-panel.txt -g BX571856.1.gb BX571856.1.fasta

	mykrobe make-probes -t example-data/tb-walker-2015-panel.txt -g data/NC_000962.3.gb data/NC_000962.3.fasta


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

