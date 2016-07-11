from __future__ import print_function
import os
import argparse


class ArgumentParserWithDefaults(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(ArgumentParserWithDefaults, self).__init__(*args, **kwargs)
        self.add_argument(
            "-q",
            "--quiet",
            help="do not output warnings to stderr",
            action="store_true",
            dest="quiet")

DEFAULT_KMER_SIZE = os.environ.get("KMER_SIZE", 21)
DEFAULT_DB_NAME = os.environ.get("DB_NAME", "atlas")

sequence_or_graph_parser_mixin = argparse.ArgumentParser(add_help=False)
sequence_or_graph_parser_mixin.add_argument(
    'sample',
    type=str,
    help='sample id')
sequence_or_graph_parser_mixin.add_argument(
    '-k',
    '--kmer',
    metavar='kmer',
    type=int,
    help='kmer length (default:21)',
    default=DEFAULT_KMER_SIZE)
sequence_or_graph_parser_mixin.add_argument(
    '--tmp',
    help='tmp directory (default: /tmp/)',
    default="/tmp/")
sequence_or_graph_parser_mixin.add_argument(
    '--keep_tmp',
    help="Dont remove tmp files",
    action="store_true")
sequence_or_graph_parser_mixin.add_argument(
    '--skeleton_dir',
    help='directory for skeleton binaries',
    default="atlas/data/skeletons/")
sequence_or_graph_parser_mixin.add_argument(
    '--mccortex31_path',
    help='Path to mccortex31',
    default="mccortex31")
sequence_or_graph_parser_mixin.add_argument(
    '-t',
    '--threads',
    type=int,
    help='threads',
    default=1)
sequence_or_graph_parser_mixin.add_argument(
    '-m',
    '--memory',
    type=str,
    help='memory for graph constuction',
    default="1GB")
sequence_or_graph_parser_mixin.add_argument(
    '--expected_depth',
    type=int,
    help='expected depth',
    default=None)


SEQUENCE_FILES_HELP_STRING = 'sequence files (fasta,fastq,bam)'
sequence_parser_mixin = argparse.ArgumentParser(
    parents=[sequence_or_graph_parser_mixin], add_help=False)
sequence_parser_mixin.add_argument(
    'seq',
    type=str,
    help=SEQUENCE_FILES_HELP_STRING,
    nargs='+')

sequence_or_binary_parser_mixin = argparse.ArgumentParser(
    parents=[sequence_or_graph_parser_mixin], add_help=False)
sequence_or_binary_parser_mixin.add_argument(
    '-1',
    '--seq',
    metavar='seq',
    type=str,
    nargs='+',
    help=SEQUENCE_FILES_HELP_STRING)
sequence_or_binary_parser_mixin.add_argument(
    '-c',
    '--ctx',
    metavar='ctx',
    type=str,
    help='cortex graph binary')

probe_set_mixin = argparse.ArgumentParser(add_help=False)
probe_set_mixin.add_argument(
    'probe_set',
    metavar='probe_set',
    type=str,
    help='probe_set')

force_mixin = argparse.ArgumentParser(add_help=False)
force_mixin.add_argument(
    '-f',
    '--force',
    action='store_true',
    help='force')

genotyping_mixin = argparse.ArgumentParser(add_help=False)
genotyping_mixin.add_argument(
    '--ignore_filtered',
    help="don't include filtered genotypes",
    default=False)
genotyping_mixin.add_argument(
    '--report_all_calls',
    help="report all calls",
    action='store_true',
    default=False)
genotyping_mixin.add_argument(
    "--min_variant_conf",
    help="minimum genotype confidence for variant genotyping",
    default=0, type=int)
genotyping_mixin.add_argument(
    "--min_gene_conf",
    help="minimum genotype confidence for gene genotyping",
    default=1, type=int)
