#! /usr/bin/env python
# from pynteractive import PhyloTree
import json
import pickle
from mykatlas.treeplacing import Node
from mykatlas.treeplacing import Leaf
from mykatlas.treeplacing import Placer
from mykatlas.treeplacing import newick2json
from mykatlas.version import __version__

from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from mongoengine import connect
import argparse
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def walk(node):
    children = []
    for child in node['children']:
        if child["type"] == "node":
            childrens = walk(child)
            children.append(Node(children=childrens))
        else:
            children.append(Leaf(child["name"]))
    return children


# def load_tree_if_required(args):
#     if args.tree is not None:
#         try:
#             root = pickle.load(open(args.tree, "rb"))
#         except KeyError:
#             with open(args.tree, 'r') as infile:
#                 tree_nwk_string = infile.read()
#             tree = newick2json(Tree(args.tree))
#             children = walk(tree)
#             root = Node(children)
#     else:
#         root = None
#     return root


def run(parser, args):
    connect('atlas-%s' % (args.db_name))
    root = None  # load_tree_if_required(args)
    base_json = {args.sample: {}}
    base_json[args.sample]["version"] = __version__
    neighbours = Placer(
        root, searchable_samples_file=args.searchable_samples).place(
        args.sample, use_cache=not args.no_cache)
    base_json[args.sample]["neighbours"] = neighbours
    print(json.dumps(base_json, indent=4))
