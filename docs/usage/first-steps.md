#  Building a variant database (atlas add)


See installation for install instructions 

## Download pre-made database



## ! mongod !

	 [mongod](https://docs.mongodb.org/manual/reference/program/mongod/) should be running in the background. 

## Download database of 3449 M. tuberculosis Variant Sets



Download data from https://www.dropbox.com/s/2qms89nb1y5ii1r/atlas-tb-2016-03-18.tar.gz?dl=1 



Run:

	 tar -zxvf  atlas-tb-2016-03-18.tar.gz
	mongorestore atlas-tb-2016-03-18  
You can query the database natively from the mongo shell (run `mongo`) but we recommend you use the [python interface](https://github.com/phelimb/ga4gh-mongo). 

## Or build your own database from VCFs

The variant database is inspired by the (GA4GH schema)[ga4gh.org/#/schemas]. Implementation available (here)[https://github.com/phelimb/ga4gh-mongo]

	 usage: atlas add [-h] [--db_name db_name] [-q] [-m METHOD] [-f]
	                 vcf reference_set
	
	positional arguments:
	  vcf                   a vcf file
	  reference_set         reference set
	
	optional arguments:
	  -h, --help            show this help message and exit
	  --db_name db_name     db_name
	  -q, --quiet           do not output warnings to stderr
	  -m METHOD, --method METHOD
	                        variant caller method (e.g. CORTEX)
	  -f, --force           Force recreate VariantSet 
To add a VCF to the database `db_name` run 

	 atlas add --db_name :db_name sample.vcf :reference_set_name 
	 atlas add --db_name :db_name --method freebayes sample.vcf :reference_set_name  
