# Read the kmer counts into a hash
from mykatlas.utils import check_args
from mykatlas.typing import Genotyper
from mykatlas.typing import CoverageParser
from mykatlas.version import __version__
from mykatlas.treeplacing import Placer

from pprint import pprint
import json
from mykatlas.cmds.atlasadd import AtlasGenotypeResult
from mykatlas.cmds.place import load_tree_if_required
from newick import load
from newick import dump
from newick import dumps


def run_main(parser, args):
    args = parser.parse_args()
    with open(args.tree, "r") as infile:
        tree = load(infile)[0]
    # print([n.name for n in tree.get_leaves()])
    # with open("/tmp/tree.nwk", "w") as infile:
    #     dump(tree, infile)
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
        memory=args.memory,
        mccortex31_path=args.mccortex31_path)
    cp.run()
    if args.expected_depth is None:
        args.expected_depth = cp.estimate_depth()

    base_json = {args.sample: {}}
    base_json[args.sample]["probe_set"] = args.probe_set
    if args.seq:
        base_json[args.sample]["files"] = args.seq
    else:
        base_json[args.sample]["files"] = args.ctx
    base_json[args.sample]["kmer"] = args.kmer
    base_json[args.sample]["version"] = __version__
    gt = Genotyper(
        sample=args.sample,
        expected_error_rate=args.expected_error_rate,
        expected_depths=[
            args.expected_depth],
        variant_covgs=cp.variant_covgs,
        gene_presence_covgs=cp.covgs["presence"],
        base_json=base_json,
        contamination_depths=[],
        ignore_filtered=args.ignore_filtered,
        report_all_calls=True,
        variant_confidence_threshold=args.min_variant_conf,
        sequence_confidence_threshold=args.min_gene_conf,
        min_gene_percent_covg_threshold=args.min_gene_percent_covg_threshold)
    gt.run()
    if not args.keep_tmp:
        cp.remove_temporary_files()
    for sample, data in gt.out_json.items():
        AtlasGenotypeResult(
            sample, "atlas", data, force=args.force).add()

    base_json = {args.sample: {}}
    base_json[args.sample]["version"] = __version__
    neighbours = Placer(
        tree, searchable_samples=[n.name for n in tree.get_leaves()]).place(
        args.sample, use_cache=not args.no_cache)
    base_json[args.sample]["neighbours"] = neighbours
    # print(json.dumps(base_json, indent=4))

    close_neighbours = []
    for i in range(10):
        close_neighbours.extend(list(neighbours[i].keys()))

    tree.prune_by_names(close_neighbours, inverse=True)
    base_json[args.sample]["tree"] = "((2741-05:1.1E-5,8038-07:1.1E-5):3.2E-5,(((9921-09:2.0E-5,C00016567:1.6E-5):2.0E-6,((4932-05:1.0E-6,2649-09:1.0E-6):1.0E-6,(3015-08:1.0E-6,((10325-06:1.0E-6,(209\
3-08:1.0E-6,(333-08:1.0E-6,(((10471-07:1.0E-6,9965-07:1.0E-6):1.0E-6,((((1520-10:1.0E-6,7445-09:1.0E-6):1.0E-6,(10094-12:1.0E-6,5277-08:1.0E-6):1.0E-6):1.0E-6,(((\
4740-11:1.0E-6,2320-12:1.0E-6):1.0E-6,(10057-10:1.0E-6,2043-09:1.0E-6):1.0E-6):1.0E-6,(8199-08:1.0E-6,(7093-11:1.0E-6,7440-08:1.0E-6):1.0E-6):1.0E-6):1.0E-6):1.0E\
-6,7035-08:1.0E-6):1.0E-6):1.0E-6,2499-12:1.0E-6):1.0E-6):1.0E-6):1.0E-6):1.0E-6,1880-09:1.0E-6):1.0E-6):1.0E-6):2.3E-5):1.0E-5,((TRL0070076-S27:2.2E-5,(TRL001881\
3-S15:1.9E-5,8182-10:1.3E-5):3.0E-6):2.0E-6,(((8053-05:1.7E-5,Bir-1167_June14:1.5E-5):5.0E-6,(6372-05:2.2E-5,((4781-04:1.0E-6,11818-03:1.0E-6):1.9E-5,C00010518:2.\
0E-5):1.0E-6):1.0E-6):1.0E-6,(((TRL0022753-S10:2.0E-6,(TRL0016123:1.0E-6,TRL0036775-S15:1.0E-6):1.0E-6):2.6E-5,(TRL0037347-S24:1.1E-5,TRL0046340-S3:1.0E-5):1.6E-5\
):1.0E-6,9677-10:2.7E-5):1.0E-6):1.0E-6):2.0E-6):2.1E-5);"  # dumps(tree)
    return base_json


def run(parser, args):
    print(json.dumps(run_main(parser, args), indent=1))
