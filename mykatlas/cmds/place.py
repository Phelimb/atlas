#! /usr/bin/env python
# from pynteractive import PhyloTree
import json
import pickle
from mykatlas.treeplacing import Node
from mykatlas.treeplacing import Leaf
from mykatlas.treeplacing import Placer
from mykatlas.treeplacing import newick2json
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from mongoengine import connect
import argparse
from ete2 import Tree
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


def load_tree_if_required(args):
    if args.tree is not None:
        try:
            root = pickle.load(open(args.tree, "rb"))
        except KeyError:
            with open(args.tree, 'r') as infile:
                tree_nwk_string = infile.read()
            tree = newick2json(Tree(args.tree))
            children = walk(tree)
            root = Node(children)
    else:
        root = None
    return root


def run(parser, args):
    connect('atlas-%s' % (args.db_name))
    root = load_tree_if_required(args)
    neighbours = Placer(root).place(args.sample, use_cache=not args.no_cache)
    if isinstance(neighbours, list):
        print "Nearest Neighbours are %s" % ",".join(neighbours)
    else:
        print "Nearest Neighbour is found to be %s" % neighbours

    # pickle.dump( root, open( "/tmp/tree.p", "wb" ) )
    # print "Dumped tree to /tmp/tree.p with cached queries. Use this tree
    # next time for faster results"

    # a=PhyloTree()
    # a.setData(')
    # a.view()
    # a.markClade(neighbours,'red')
    # while True:
    #     time.sleep(10)
