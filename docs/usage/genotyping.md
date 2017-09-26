#  Genotyping (atlas genotype)


Atlas can currently genotype small variants, SNPs, INDELs as well as typing gene versions within a gene family. 

## 1. Download a probe set

*M. tuberculosis* SNP probe set: https://www.dropbox.com/s/vmaqfmeiqeka7jk/panel_tb_k31_2016-03-18.fasta.gz?dl=1

#### Or build your own 

	 See ["Building a probeset:](https://mykrobe-atlas.readme.io/docs/building-a-probe-set) 



## Genotype using a probe set



	 usage: atlas genotype [-h] [-k kmer] [--tmp TMP] [--keep_tmp]
	                      [--skeleton_dir SKELETON_DIR]
	                      [--mccortex31_path MCCORTEX31_PATH] [-t THREADS]
	                      [-m MEMORY] [--expected_depth EXPECTED_DEPTH]
	                      [-1 seq [seq ...]] [-c ctx] [-f]
	                      [--ignore_filtered IGNORE_FILTERED] [--report_all_calls]
	                      [--expected_error_rate EXPECTED_ERROR_RATE]
	                      [--min_variant_conf MIN_VARIANT_CONF]
	                      [--min_gene_conf MIN_GENE_CONF]
	                      [--min_gene_percent_covg_threshold MIN_GENE_PERCENT_COVG_THRESHOLD]
	                      [-q]
	                      sample probe_set
	
	positional arguments:
	  sample                sample id
	  probe_set             probe_set
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -k kmer, --kmer kmer  kmer length (default:21)
	  --tmp TMP             tmp directory (default: tmp/)
	  --keep_tmp            Dont remove tmp files
	  --skeleton_dir SKELETON_DIR
	                        directory for skeleton binaries
	  --mccortex31_path MCCORTEX31_PATH
	                        Path to mccortex31
	  -t THREADS, --threads THREADS
	                        threads
	  -m MEMORY, --memory MEMORY
	                        memory for graph constuction
	  --expected_depth EXPECTED_DEPTH
	                        expected depth
	  -1 seq [seq ...], --seq seq [seq ...]
	                        sequence files (fasta,fastq,bam)
	  -c ctx, --ctx ctx     cortex graph binary
	  -f, --force           force
	  --ignore_filtered IGNORE_FILTERED
	                        don't include filtered genotypes
	  --report_all_calls    report all calls
	  --expected_error_rate EXPECTED_ERROR_RATE
	                        Expected sequencing error rate. Set to 0.15 for ONT
	                        genotyping.
	  --min_variant_conf MIN_VARIANT_CONF
	                        minimum genotype confidence for variant genotyping
	  --min_gene_conf MIN_GENE_CONF
	                        minimum genotype confidence for gene genotyping
	  --min_gene_percent_covg_threshold MIN_GENE_PERCENT_COVG_THRESHOLD
	                        all genes alleles found above this percent coverage
	                        will be reported (default 100 (only best alleles
	                        reported))
	  -q, --quiet           do not output warnings to stderr 
To genotype using the variant probe set on sample `:sample`. You can find the example-data in the git repo. https://github.com/phelimb/atlas

	 atlas genotype sample_id example-data/probe-set.fasta -1 example-data/example.fasta 
Output: 



	 {
	 "sample_id": {
	  "files": [
	   "example-data/example.fasta"
	  ], 
	  "variant_calls": {
	   "ca47617c08cbc2034560e3fc91c06ae165dc466b73b9c67908e4ee49fad0b32b": {
	    "info": {
	     "filter": "PASS", 
	     "contamination_depths": [], 
	     "conf": 7, 
	     "expected_depths": [
	      7
	     ], 
	     "coverage": {
	      "alternate": {
	       "percent_coverage": 100.0, 
	       "median_depth": 3.0, 
	       "min_non_zero_depth": 2.0
	      }, 
	      "reference": {
	       "percent_coverage": 100.0, 
	       "median_depth": 3.0, 
	       "min_non_zero_depth": 2.0
	      }
	     }
	    }, 
	    "_cls": "Call.VariantCall", 
	    "variant": null, 
	    "genotype": [
	     0, 
	     1
	    ], 
	    "genotype_likelihoods": [
	     -11.3077583974572, 
	     -4.405802435369161, 
	     -11.3077583974572
	    ]
	   }, 
	   "0b45c5098d4942d782f72ec8430464b622dbe38d246fa33116673c6e714053e2": {
	    "info": {
	     "filter": "PASS", 
	     "contamination_depths": [], 
	     "conf": 11, 
	     "expected_depths": [
	      7
	     ], 
	     "coverage": {
	      "alternate": {
	       "percent_coverage": 100.0, 
	       "median_depth": 5.0, 
	       "min_non_zero_depth": 2.0
	      }, 
	      "reference": {
	       "percent_coverage": 100.0, 
	       "median_depth": 8.0, 
	       "min_non_zero_depth": 3.0
	      }
	     }
	    }, 
	    "_cls": "Call.VariantCall", 
	    "variant": null, 
	    "genotype": [
	     0, 
	     1
	    ], 
	    "genotype_likelihoods": [
	     -17.683652185585395, 
	     -6.927600680492404, 
	     -29.9666858722517
	    ]
	   }, 
	   "557d63def65f2f3741d54ff76e28ccec9119ee1e105368bfe12cd652f94bfb9d": {
	    "info": {
	     "filter": "PASS", 
	     "contamination_depths": [], 
	     "conf": 13, 
	     "expected_depths": [
	      7
	     ], 
	     "coverage": {
	      "alternate": {
	       "percent_coverage": 100.0, 
	       "median_depth": 6.0, 
	       "min_non_zero_depth": 3.0
	      }, 
	      "reference": {
	       "percent_coverage": 100.0, 
	       "median_depth": 7.0, 
	       "min_non_zero_depth": 3.0
	      }
	     }
	    }, 
	    "_cls": "Call.VariantCall", 
	    "variant": null, 
	    "genotype": [
	     0, 
	     1
	    ], 
	    "genotype_likelihoods": [
	     -21.490314675355712, 
	     -8.026212969160511, 
	     -25.584659237577817
	    ]
	   }
	  }, 
	  "version": "v0.3.13-1-g37fddf0-dirty", 
	  "kmer": 21, 
	  "sequence_calls": {}, 
	  "filtered": [1, 1, 1], 
	  "genotypes": [1, 1, 1], 
	  "probe_set": "example-data/probe-set.fasta"
	 }
	}
	 
The key values to look at here are : 



"variant_calls" which give you information on the variant calls were made. Each key is the variant ID which is the hash of variant name (ref:pos:alt). and values give the data on the variant call. 



"genotypes":gives a list of genotypes of the variants in the probe set (1/0)

"filtered" : is a list of of booleans stating whether these variants pass the filters. 1=PASS 0=FILTERED.



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
