#  Installation


Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent nec massa tristique arcu ferme.

## 1. Clone repo from github



## ! Recursive git clone !

	 git clone **--recursive** git@github.com:phelimb/atlas.git 



## 2. Install requirements

## mccortex

## ! Important! !

	 **NB: You must install the version of mccortex that comes with this repository** 

	cd atlas

	cd mccortex

	make	

	export PATH=$PATH:$(pwd)/bin

	cd ..



## mongodb



Download relevant binaries from https://www.mongodb.org/downloads#production.

## Install atlas (virtualenv recommended)

## Install virtualenv



	https://virtualenv.readthedocs.org/en/latest/installation.html



## Create virtualenv 



	virtualenv venv



## Activate the virtualenv



	source venv/bin/activate



You can deactivate at anytime by typing 'deactivate'. 





## Install from 





	python setup.py install





## Usage





	optional arguments:



	[sub-commands]:

	  {add,dump-probes,make-probes,genotype}

	    add                 adds a set of variants to the atlas

	    dump-probes         dump a panel of variant alleles

	    make-probes         make probes from a list of variants

	    genotype            genotype a sample using a probe set
