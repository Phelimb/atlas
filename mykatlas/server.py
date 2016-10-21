"""First API, local access only"""
import hug
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
import shutil


@hug.get()
def predict(file: hug.types.text):
    return {}


@hug.get(examples='file=333-08.fastq.gz', headers={'Access-Control-Allow-Origin', '*'})
def treeplace(file: hug.types.text, use_cache=1):
    use_cache = bool(int(use_cache))
    with open("RAxML_der_and_valbestTree.raxml3674", "r") as infile:
        tree = load(infile)[0]
    # print([n.name for n in tree.get_leaves()])
    # with open("/tmp/tree.nwk", "w") as infile:
    #     dump(tree, infile)
    verbose = True
    sample = file.split(".")[0]
    predictor_file = "data/%s" % file.replace(".fastq.gz", "_predictor.json")

    file = ["data/%s" % file]

    cp = CoverageParser(
        sample=sample,
        panel_file_paths=["panel_tb_k31_2016-07-04_no_singeltons.fasta"],
        seq=file,
        ctx=None,
        kmer=31,
        force=False,
        verbose=verbose,
        tmp_dir="/tmp/",
        skeleton_dir="atlas/data/skeletons/",
        threads=1,
        memory="1GB",
        mccortex31_path="mccortex31")
    if not use_cache:
        shutil.rmtree("/tmp/", ignore_errors=True)
    cp.run()
    expected_depth = cp.estimate_depth()
    with open(predictor_file, 'r') as infile:
        base_json = json.load(infile)
    # base_json = {sample: {}}
    base_json[sample][
        "probe_set"] = "panel_tb_k31_2016-07-04_no_singeltons.fasta"
    if file:
        base_json[sample]["files"] = file
    else:
        base_json[sample]["files"] = None
    base_json[sample]["kmer"] = 31
    base_json[sample]["version"] = __version__
    gt = Genotyper(
        sample=sample,
        expected_error_rate=0.05,
        expected_depths=[
            expected_depth],
        variant_covgs=cp.variant_covgs,
        gene_presence_covgs=cp.covgs["presence"],
        base_json=base_json,
        contamination_depths=[],
        ignore_filtered=False,
        report_all_calls=True,
        variant_confidence_threshold=0,
        sequence_confidence_threshold=1,
        min_gene_percent_covg_threshold=100)
    gt.run()
    # cp.remove_temporary_files()
    for sample, data in gt.out_json.items():
        AtlasGenotypeResult(
            sample, "atlas", data, force=False).add()

    base_json[sample]["version"] = __version__
    neighbours = Placer(
        tree, searchable_samples=[n.name for n in tree.get_leaves()]).place(
        sample, use_cache=False)
    base_json[sample]["neighbours"] = neighbours
    close_neighbours = []
    if neighbours:
        for i in range(10):
            close_neighbours.extend(list(neighbours[i].keys()))

    tree.prune_by_names(close_neighbours, inverse=True)
    base_json[sample]["tree"] = "((2741-05:1.1E-5,8038-07:1.1E-5):3.2E-5,(((9921-09:2.0E-5,C00016567:1.6E-5):2.0E-6,((4932-05:1.0E-6,2649-09:1.0E-6):1.0E-6,(3015-08:1.0E-6,((10325-06:1.0E-6,(209\
3-08:1.0E-6,(333-08:1.0E-6,(((10471-07:1.0E-6,9965-07:1.0E-6):1.0E-6,((((1520-10:1.0E-6,7445-09:1.0E-6):1.0E-6,(10094-12:1.0E-6,5277-08:1.0E-6):1.0E-6):1.0E-6,(((\
4740-11:1.0E-6,2320-12:1.0E-6):1.0E-6,(10057-10:1.0E-6,2043-09:1.0E-6):1.0E-6):1.0E-6,(8199-08:1.0E-6,(7093-11:1.0E-6,7440-08:1.0E-6):1.0E-6):1.0E-6):1.0E-6):1.0E\
-6,7035-08:1.0E-6):1.0E-6):1.0E-6,2499-12:1.0E-6):1.0E-6):1.0E-6):1.0E-6):1.0E-6,1880-09:1.0E-6):1.0E-6):1.0E-6):2.3E-5):1.0E-5,((TRL0070076-S27:2.2E-5,(TRL001881\
3-S15:1.9E-5,8182-10:1.3E-5):3.0E-6):2.0E-6,(((8053-05:1.7E-5,Bir-1167_June14:1.5E-5):5.0E-6,(6372-05:2.2E-5,((4781-04:1.0E-6,11818-03:1.0E-6):1.9E-5,C00010518:2.\
0E-5):1.0E-6):1.0E-6):1.0E-6,(((TRL0022753-S10:2.0E-6,(TRL0016123:1.0E-6,TRL0036775-S15:1.0E-6):1.0E-6):2.6E-5,(TRL0037347-S24:1.1E-5,TRL0046340-S3:1.0E-5):1.6E-5\
):1.0E-6,9677-10:2.7E-5):1.0E-6):1.0E-6):2.0E-6):2.1E-5);"  # dumps(tree)
    del base_json[sample]["genotypes"]
    del base_json[sample]["filtered"]
    del base_json[sample]["sequence_calls"]
    del base_json[sample]["variant_calls"]
    return base_json
