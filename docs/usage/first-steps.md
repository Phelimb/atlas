---
title: "Building a variant database (atlas add)"
excerpt: ""
---
See installation for install instructions 
[block:api-header]
{
  "type": "basic",
  "title": "Download pre-made database"
}
[/block]

[block:callout]
{
  "type": "info",
  "title": "mongod",
  "body": "[mongod](https://docs.mongodb.org/manual/reference/program/mongod/) should be running in the background."
}
[/block]
## Download database of 3449 M. tuberculosis Variant Sets

Download data from https://www.dropbox.com/s/2qms89nb1y5ii1r/atlas-tb-2016-03-18.tar.gz?dl=1 

Run:
[block:code]
{
  "codes": [
    {
      "code": "tar -zxvf  atlas-tb-2016-03-18.tar.gz\nmongorestore atlas-tb-2016-03-18 ",
      "language": "shell"
    }
  ]
}
[/block]
You can query the database natively from the mongo shell (run `mongo`) but we recommend you use the [python interface](https://github.com/phelimb/ga4gh-mongo). 
[block:api-header]
{
  "type": "basic",
  "title": "Or build your own database from VCFs"
}
[/block]
The variant database is inspired by the (GA4GH schema)[ga4gh.org/#/schemas]. Implementation available (here)[https://github.com/phelimb/ga4gh-mongo]
[block:code]
{
  "codes": [
    {
      "code": "usage: atlas add [-h] [--db_name db_name] [-q] [-m METHOD] [-f]\n                 vcf reference_set\n\npositional arguments:\n  vcf                   a vcf file\n  reference_set         reference set\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --db_name db_name     db_name\n  -q, --quiet           do not output warnings to stderr\n  -m METHOD, --method METHOD\n                        variant caller method (e.g. CORTEX)\n  -f, --force           Force recreate VariantSet",
      "language": "shell"
    }
  ]
}
[/block]
To add a VCF to the database `db_name` run 
[block:code]
{
  "codes": [
    {
      "code": "atlas add --db_name :db_name sample.vcf :reference_set_name",
      "language": "shell"
    }
  ]
}
[/block]
Use the --method argument to specify the variant caller or pipeline used (if you'll have multiple Call Sets per sample)
[block:code]
{
  "codes": [
    {
      "code": "atlas add --db_name :db_name --method freebayes sample.vcf :reference_set_name ",
      "language": "text"
    }
  ]
}
[/block]