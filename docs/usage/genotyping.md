---
title: "Genotyping (atlas genotype)"
excerpt: ""
---
Atlas can currently genotype small variants, SNPs, INDELs as well as typing gene versions within a gene family. 
[block:api-header]
{
  "type": "basic",
  "title": "1. Download a probe set"
}
[/block]
*M. tuberculosis* SNP probe set: https://www.dropbox.com/s/vmaqfmeiqeka7jk/panel_tb_k31_2016-03-18.fasta.gz?dl=1
[block:callout]
{
  "type": "info",
  "title": "Or build your own",
  "body": "See [\"Building a probeset:](https://mykrobe-atlas.readme.io/docs/building-a-probe-set)"
}
[/block]

[block:api-header]
{
  "type": "basic",
  "title": "Genotype using a probe set"
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "usage: atlas genotype [-h] [-k kmer] [--tmp TMP] [--skeleton_dir SKELETON_DIR]\n                      [--mccortex31_path MCCORTEX31_PATH] [-q]\n                      [--expected_depth expected depth] [-f]\n                      [--ignore_filtered IGNORE_FILTERED]\n                      sample seq [seq ...] panels [panels ...]\n\npositional arguments:\n  sample                sample id\n  seq                   sequence files (fastq or bam)\n  panels                panels\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -k kmer, --kmer kmer  kmer length (default:21)\n  --tmp TMP             tmp directory (default: /tmp/)\n  --skeleton_dir SKELETON_DIR\n                        directory for skeleton binaries\n  --mccortex31_path MCCORTEX31_PATH\n                        Path to mccortex31\n  -q, --quiet           do not output warnings to stderr\n  --expected_depth expected depth\n                        expected depth\n  -f, --force           Force rebuilding of binaries\n  --ignore_filtered IGNORE_FILTERED\n                        don't include filtered genotypes",
      "language": "text"
    }
  ]
}
[/block]
To genotype using the variant probe set on sample `:sample`
[block:code]
{
  "codes": [
    {
      "code": "atlas genotype :sample sample_*.fastq.gz  panel_tb_k31_2016-03-18.fasta.gz",
      "language": "shell"
    }
  ]
}
[/block]
Output: 

[block:code]
{
  "codes": [
    {
      "code": "...\n\"variant_calls\": {\n            \"rpoB_N438S-AAC761118AGT\": {\n                \"info\": {\n                    \"filter\": \"PASS\",\n                    \"contamination_depths\": [],\n                    \"coverage\": {\n                        \"alternate\": {\n                            \"percent_coverage\": 45.0,\n                            \"median_depth\": 0.0,\n                            \"min_non_zero_depth\": 1.0\n                        },\n                        \"reference\": {\n                            \"percent_coverage\": 100.0,\n                            \"median_depth\": 44.0,\n                            \"min_non_zero_depth\": 36.0\n                        }\n                    },\n                    \"expected_depths\": [\n                        56.0\n                    ]\n                },\n                \"_cls\": \"Call.VariantCall\",\n                \"genotype\": [\n                    0,\n                    0\n                ],\n                \"genotype_likelihoods\": [\n                    -5.135130090343647,\n                    -99999999.0,\n                    -99999999.0\n                ]\n            },\n  ...\n}",
      "language": "json"
    }
  ]
}
[/block]

[block:api-header]
{
  "type": "basic",
  "title": "Genotype gene panel"
}
[/block]
E.g. Ecoli/Kleb AMR gene families

https://www.dropbox.com/s/s8131cil1bh44mj/gn-amr-genes.fasta.gz?dl=1


[block:code]
{
  "codes": [
    {
      "code": "atlas genotype :sample sample_*.fastq.gz  gn-amr-genes.fasta.gz",
      "language": "shell"
    }
  ]
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "...\n\t\"sequence_calls\": {\n   \t...\"tem\": {\n                \"info\": {\n                    \"copy_number\": 7.3,\n                    \"contamination_depths\": [],\n                    \"version\": \"1\",\n                    \"coverage\": {\n                        \"percent_coverage\": 100.0,\n                        \"median_depth\": 73.0,\n                        \"min_non_zero_depth\": 60.0\n                    },\n                    \"expected_depths\": [\n                        10\n                    ]\n                },\n                \"_cls\": \"Call.SequenceCall\",\n                \"genotype\": [\n                    1,\n                    1\n                ],\n                \"genotype_likelihoods\": [\n                    -579.4562725801134,\n                    -294.3685931838587,\n                    -103.68092850339738\n                ]\n            }\n        },\n\t...\n...",
      "language": "json"
    }
  ]
}
[/block]