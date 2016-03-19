---
title: "Installation"
excerpt: ""
---
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent nec massa tristique arcu ferme.
[block:api-header]
{
  "type": "basic",
  "title": "1. Clone repo from github"
}
[/block]

[block:callout]
{
  "type": "info",
  "body": "git clone **--recursive** git@github.com:phelimb/atlas.git",
  "title": "Recursive git clone"
}
[/block]

[block:api-header]
{
  "type": "basic",
  "title": "2. Install requirements"
}
[/block]
## mccortex
[block:callout]
{
  "type": "warning",
  "body": "**NB: You must install the version of mccortex that comes with this repository**",
  "title": "Important!"
}
[/block]
	cd atlas
	cd mccortex
	make	
	export PATH=$PATH:$(pwd)/bin
	cd ..

## mongodb

Download relevant binaries from https://www.mongodb.org/downloads#production.
[block:api-header]
{
  "type": "basic",
  "title": "Install atlas (virtualenv recommended)"
}
[/block]
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