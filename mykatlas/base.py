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

sequence_parser_mixin = argparse.ArgumentParser(add_help=False)
sequence_parser_mixin.add_argument(
    'sample',
    type=str,
    help='sample id')
sequence_parser_mixin.add_argument(
    'seq',
    type=str,
    help='sequence files (fastq or bam)',
    nargs='+')
sequence_parser_mixin.add_argument(
    '-k',
    '--kmer',
    metavar='kmer',
    type=int,
    help='kmer length (default:21)',
    default=DEFAULT_KMER_SIZE)
sequence_parser_mixin.add_argument(
    '--tmp',
    help='tmp directory (default: /tmp/)',
    default="/tmp/")
sequence_parser_mixin.add_argument(
    '--skeleton_dir',
    help='directory for skeleton binaries',
    default="atlas/data/skeletons/")
sequence_parser_mixin.add_argument(
    '--mccortex31_path',
    help='Path to mccortex31',
    default="mccortex31")
