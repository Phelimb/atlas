#  Building a probe set (atlas {make-probes, dump-probes})


You can create a variant probe set in two ways.

## 1. 'Dumping' the Variant database

`atlas dump-probes`

	 usage: atlas dump-probes [-h] [--db_name db_name] [-q] [--kmer kmer] [--force]
	                         [-v]
	                         reference_filepath
	
	positional arguments:
	  reference_filepath  reference_filepath
	
	optional arguments:
	  -h, --help          show this help message and exit
	  --db_name db_name   db_name
	  -q, --quiet         do not output warnings to stderr
	  --kmer kmer         kmer length
	  --force
	  -v, --verbose 


	 atlas dump-probes reference_set.fasta > variant_probe_set.fasta 
This will generate a probe set for each variant in the database. The resulting fasta file will look like the following:

	 >ref-37d2eea6a23d526cbee4e00b901dc97885a88e7aa8721432b080dcc342b459ce?num_alts=10&ref=56cf2e4ca9fefcd2b15de4d6
	TCGCCGCAGCGGTTGGCAACGATGTGGTGCGATCGCTAAAGATCACCGGGCCGGCGGCACCAT
	...
	TCGCCGCAGCGGTTGGCAACGATGTGGTGCAATCGCTAAAGATCACCGGGCCGGCGGCATCAT
	>alt-37d2eea6a23d526cbee4e00b901dc97885a88e7aa8721432b080dcc342b459ce
	TCGCCGCAGCGGTTGGCAACGATGTGGTGCAATCGCTAAAGATCACCGGGCCGGCGGCACGAT
	>ref-2dab6387a677ac17f6bc181f47235a4196885723b34ceff3a05ffcbfd6834347?num_alts=10&ref=56cf2e4ca9fefcd2b15de4d6
	CTGTCGCTGGGAAGAGCGAATACGTCTGGACCAGGACGGGCTACCCGAACACGATATCTTTCG
	>alt-2dab6387a677ac17f6bc181f47235a4196885723b34ceff3a05ffcbfd6834347
	... 
Where you have a series of variants represented as a set of alleles. The reference allele followed by multiple alternate alleles. You will end up with multiple alternate alleles if there are other variants that fall within k of the target variant. 



Each variant is referenced by a `var_hash` with is the hash of ":ref:pos:alt" which is indexed in the database and can be used to query for Variant object.



See `atlas genotype` to use these probes to genotype a new sample. 

## 2. Building a custom probe set

`atlas make-probes` allows you to build a probe set using Variants that are not already in the database. 

	 usage: atlas make-probes [-h] [--db_name db_name] [-q] [-v VARIANT] [-f FILE]
	                         [-g GENBANK] [-k KMER] [--no-backgrounds]
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
	  --no-backgrounds      Build probe set against reference only ignoring nearby
	                        variants 
Example usages: 



## Build a variant probe set defined based on reference co-ordinates (1-based)



First, define your variants for which you want to build probes. Columns are 



ref/gene pos ref alt alphabet

	 ref     2522798 G       T       DNA
	ref     3785555 A       G       DNA
	ref     839793  C       A       DNA
	ref     2734398 C       G       DNA
	ref     3230861 T       A       DNA
	ref     1018694 A       T       DNA 


	 atlas make-probes --db_name :db_name -f variants.txt ref.fa > variant_probe_set.fa 
## Build a variant probe set defined based on gene co-ordinates (1-based)



You can also define your variants in terms of gene coordinates in amino acid or DNA space.

	 rpoB    S431X   PROT
	rpoB    F425X   PROT
	embB    M306X   PROT
	rrs     C513X   DNA
	gyrA    D94X    PROT
	gid     P75L    PROT
	gid     V88A    PROT
	katG    S315X   PROT 
To do this you must provide a genbank file defining the position of the variants in the reference (-g (GENBANK) )

	 atlas make-probes --db_name :db_name -f aa_variants.txt -g ref.gb  ref.fa> gene_variant_probe_set.fa 
