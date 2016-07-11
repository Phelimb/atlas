from __future__ import print_function
import sys
from mykatlas.cortex.server import WebServer
from mykatlas.cortex.server import McCortexQuery
from mykatlas.cortex.server import GraphWalker
from mykatlas.cortex.server import query_mccortex
from mykatlas.utils import get_params
import socket
import json
from pprint import pprint
import logging
from Bio import SeqIO
import argparse

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
from mykatlas.cmds.genotype import run_main as run_genotype


class PathDetails(object):

    def __init__(self, start_kmer, last_kmer, length, skipped=0, v=""):
        self.start_kmer = start_kmer
        self.last_kmer = last_kmer
        self.length = length
        self.skipped = skipped
        self.version = v
        self.repeat_kmers = {}

    def __eq__(self, pd):
        return self.start_kmer == pd.start_kmer and self.last_kmer == pd.last_kmer and self.length == pd.length and self.skipped == pd.skipped

    def set_repeat_kmers(self, repeat_kmers):
        if not self.repeat_kmers:
            self.repeat_kmers = repeat_kmers
        else:
            raise ValueError("Already set repeat kmers")


def get_repeat_kmers(record, k):
    # Process repeat kmers
    kmers = {}
    kmers_seq = []
    for i in range(len(record.seq) - k + 1):
        _kmers = [str(record.seq[i:i + k]),
                  str(record.seq[i:i + k].reverse_complement())]
        for kmer in _kmers:
            kmers_seq.append(kmers_seq)
            if kmer in kmers:
                c = max(kmers[kmer].keys()) + 1
                kmers[kmer][c] = str(record.seq[i + 1:i + k + 1])
            else:
                kmers[kmer] = {}
                kmers[kmer][1] = str(record.seq[i + 1:i + k + 1])
    return kmers


def find_start_kmer(seq, mcq, k):
    skipped = 0
    for i in range(len(seq) - k + 1):
        kmer = seq[i:i + k]
        q = mcq.query(kmer)
        if q.data and q.depth > 1:
            return kmer, skipped
        skipped += 1
    return None, -1


def choose_best_assembly(paths):
    paths.sort(key=lambda x: x["min_non_zero_depth"], reverse=True)
    current_best = paths[0]
    for path in paths[1:]:
        if path["min_non_zero_depth"] < current_best["min_non_zero_depth"]:
            return current_best
        elif path["min_non_zero_depth"] == current_best["min_non_zero_depth"]:
            if path["median_depth"] > current_best["median_depth"]:
                current_best = path
    return current_best


def get_paths_for_gene(gene_name, gene_dict, gw):
    paths = {}
    current_prots = []
    for pd in gene_dict["pathdetails"]:
        try:
            path_for_pd = gw.breath_first_search(
                N=pd.length,
                seed=pd.start_kmer,
                end_kmers=[
                    pd.last_kmer],
                known_kmers=gene_dict["known_kmers"],
                repeat_kmers=pd.repeat_kmers,
                N_left=pd.skipped)
            if path_for_pd:
                keep_p = []
                for p in path_for_pd:
                    p["seed_version"] = pd.version
                    if p["prot"] not in current_prots:
                        keep_p.append(p)
                        current_prots.append(p["prot"])
                if keep_p:
                    if len(keep_p) > 1:
                        raise NotImplementedError()
                    else:
                        paths[pd.version] = keep_p[0]
        except ValueError as e:
            logger.error(e)
    return paths


def check_args(args):
    if args.seq is None and args.ctx is None:
        raise ValueError("Requires either -1 or -c to be set")
    if args.seq and args.ctx:
        raise ValueError("Only -1 or -c to be set")
    if args.seq and not args.ctx:
        raise NotImplementedError(
            "Input raw sequence data not yet supported. Please build the binary with `mccortex build` and run with -c")


def run(parser, args):
    genes = {}
    skip_list = {"tem": ["191", "192"],
                 "oxa": ["12", "14", "33"],
                 "shv": ["12", "6"]
                 }
    check_args(args)
    if args.seq:
        build_binary()
    if args.also_genotype:
        _out_dict = run_genotype(parser, args)
    else:
        _out_dict = {}
        _out_dict[args.sample] = {}
    _out_dict[args.sample]["paths"] = {}
    out_dict = _out_dict[args.sample]["paths"]
    wb = WebServer(
        port=0,
        args=[
            args.ctx],
        memory=args.memory,
        mccortex_path=args.mccortex31_path)
    logger.debug("Loading binary")
    wb.start()
    logger.debug("Walking the graph")
    gw = GraphWalker(proc=wb.mccortex, kmer_size=args.kmer, print_depths=True)
    with open(args.probe_set, 'r') as infile:
        for i, record in enumerate(SeqIO.parse(infile, "fasta")):
            repeat_kmers = get_repeat_kmers(record, args.kmer)
            params = get_params(record.id)
            gene_name = params.get("name", i)
            version = params.get("version", i)
            if gene_name not in genes:
                logger.debug("Loading kmer data for %s" % (gene_name))
            last_kmer = str(record.seq)[-args.kmer:]
            start_kmer, skipped = find_start_kmer(
                str(record.seq), gw.mcq, args.kmer)
            if gene_name not in genes:
                genes[gene_name] = {}
                genes[gene_name]["pathdetails"] = []
                genes[gene_name]["known_kmers"] = ""
            if version not in skip_list.get(gene_name, []) and start_kmer:
                pd = PathDetails(start_kmer, last_kmer, len(record.seq),
                                 skipped=skipped, v=version)
                pd.set_repeat_kmers(repeat_kmers)
                genes[gene_name]["pathdetails"].append(pd)

            if gene_name in genes:
                genes[gene_name]["known_kmers"] += "%sN" % str(record.seq)

    for gene_name, gene_dict in genes.items():
        logger.debug("Walking graph with seeds defined by %s" % gene_name)
        paths = get_paths_for_gene(gene_name, gene_dict, gw)
        if args.show_all_paths:
            out_dict[gene_name] = paths.values()
        else:
            if len(paths.keys()) > 1:
                # choose best version
                best_path = choose_best_assembly(paths.values())
            elif len(paths.keys()) == 1:
                best_path = paths.values()[0]
            else:
                best_path = {"found": False}
            out_dict[gene_name] = [best_path]
    print (json.dumps(_out_dict, sort_keys=False, indent=4))
    logger.info("Cleaning up")
    if wb is not None:
        wb.stop()
