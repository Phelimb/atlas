#  Genotyping (atlas genotype)


Atlas can currently genotype small variants, SNPs, INDELs as well as typing gene versions within a gene family. 

## 1. Download a probe set

*M. tuberculosis* SNP probe set: https://www.dropbox.com/s/vmaqfmeiqeka7jk/panel_tb_k31_2016-03-18.fasta.gz?dl=1

#### Or build your own 

	 See ["Building a probeset:](https://mykrobe-atlas.readme.io/docs/building-a-probe-set) 



## Genotype using a probe set



	 usage: atlas genotype [-h] [-k kmer] [--tmp TMP] [--skeleton_dir SKELETON_DIR]
	                      [--mccortex31_path MCCORTEX31_PATH] [-q]
	                      [--expected_depth expected depth] [-f]
	                      [--ignore_filtered IGNORE_FILTERED]
	                      sample seq [seq ...] panels [panels ...]
	
	positional arguments:
	  sample                sample id
	  seq                   sequence files (fastq or bam)
	  panels                panels
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -k kmer, --kmer kmer  kmer length (default:21)
	  --tmp TMP             tmp directory (default: /tmp/)
	  --skeleton_dir SKELETON_DIR
	                        directory for skeleton binaries
	  --mccortex31_path MCCORTEX31_PATH
	                        Path to mccortex31
	  -q, --quiet           do not output warnings to stderr
	  --expected_depth expected depth
	                        expected depth
	  -f, --force           Force rebuilding of binaries
	  --ignore_filtered IGNORE_FILTERED
	                        don't include filtered genotypes 
To genotype using the variant probe set on sample `:sample`

	 atlas genotype :sample sample_*.fastq.gz  panel_tb_k31_2016-03-18.fasta.gz 
Output: 



	 ...
	"variant_calls": {
	            "rpoB_N438S-AAC761118AGT": {
	                "info": {
	                    "filter": "PASS",
	                    "contamination_depths": [],
	                    "coverage": {
	                        "alternate": {
	                            "percent_coverage": 45.0,
	                            "median_depth": 0.0,
	                            "min_non_zero_depth": 1.0
	                        },
	                        "reference": {
	                            "percent_coverage": 100.0,
	                            "median_depth": 44.0,
	                            "min_non_zero_depth": 36.0
	                        }
	                    },
	                    "expected_depths": [
	                        56.0
	                    ]
	                },
	                "_cls": "Call.VariantCall",
	                "genotype": [
	                    0,
	                    0
	                ],
	                "genotype_likelihoods": [
	                    -5.135130090343647,
	                    -99999999.0,
	                    -99999999.0
	                ]
	            },
	  ...
	} 


## Genotype gene panel

E.g. Ecoli/Kleb AMR gene families



https://www.dropbox.com/s/s8131cil1bh44mj/gn-amr-genes.fasta.gz?dl=1





	 atlas genotype :sample sample_*.fastq.gz  gn-amr-genes.fasta.gz 


	 ...
		"sequence_calls": {
	   	..."tem": {
	                "info": {
	                    "copy_number": 7.3,
	                    "contamination_depths": [],
	                    "version": "1",
	                    "coverage": {
	                        "percent_coverage": 100.0,
	                        "median_depth": 73.0,
	                        "min_non_zero_depth": 60.0
	                    },
	                    "expected_depths": [
	                        10
	                    ]
	                },
	                "_cls": "Call.SequenceCall",
	                "genotype": [
	                    1,
	                    1
	                ],
	                "genotype_likelihoods": [
	                    -579.4562725801134,
	                    -294.3685931838587,
	                    -103.68092850339738
	                ]
	            }
	        },
		...
	... 
