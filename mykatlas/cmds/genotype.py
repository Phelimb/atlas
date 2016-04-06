# Read the kmer counts into a hash
from mykatlas.utils import check_args
from mykatlas.typing import Genotyper
from mykatlas.typing import CoverageParser
from mykatlas.version import __version__

from pprint import pprint
import json


def run_main(parser, args):
    args = parser.parse_args()
    verbose = True
    cp = CoverageParser(
        sample=args.sample,
        panel_file_paths=[args.probe_set],
        seq=args.seq,
        ctx=args.ctx,
        kmer=args.kmer,
        force=args.force,
        verbose=verbose,
        tmp_dir=args.tmp,
        skeleton_dir=args.skeleton_dir,
        threads=args.threads,
        mccortex31_path=args.mccortex31_path)
    cp.run()

    if args.expected_depth is None:
        args.expected_depth = cp.estimate_depth()

    base_json = {args.sample: {}}
    base_json[args.sample]["probe_set"] = args.probe_set
    base_json[args.sample]["files"] = args.seq
    base_json[args.sample]["kmer"] = args.kmer
    base_json[args.sample]["version"] = __version__
    gt = Genotyper(sample=args.sample, expected_depths=[args.expected_depth],
                   variant_covgs=cp.variant_covgs,
                   gene_presence_covgs=cp.covgs["presence"],
                   base_json=base_json,
                   contamination_depths=[],
                   ignore_filtered=args.ignore_filtered)
    gt.run()
    cp.remove_temporary_files()
    return gt.out_json


def run(parser, args):
    print(json.dumps(run_main(parser, args), indent=4))
