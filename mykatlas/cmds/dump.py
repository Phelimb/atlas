#! /usr/bin/env python
from pymongo import MongoClient
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")
import datetime
import logging
logger = logging.getLogger(__name__)


from mongoengine import connect

from ga4ghmongo.schema import Variant
from mykatlas.panelgeneration import AlleleGenerator
from mykatlas.panelgeneration import make_variant_probe


def get_non_singelton_variants(db_name):
    client = MongoClient('localhost', 27017)
    db = client[db_name]
    collection = db['call']
    results = collection.aggregate([{"$match": {}},
                                    {"$group": {"_id": {"variant": "$variant"},
                                                "count": {"$sum": 1}}},
                                    {"$match": {"count": {"$gt": 1}}}])
    variants = [r["_id"]["variant"] for r in results]
    return variants


def run(parser, args):
    db_name = 'atlas-%s' % (args.db_name)
    DB = connect(db_name)
    if args.verbose:
        logger.setLevel(level=logging.DEBUG)
    else:
        logger.setLevel(level=logging.ERROR)
    al = AlleleGenerator(
        reference_filepath=args.reference_filepath,
        kmer=args.kmer)
    _variant_ids = get_non_singelton_variants(db_name)
    for variant in Variant.snps(id__in=_variant_ids).order_by("start"):
        variant_panel = make_variant_probe(al, variant, args.kmer, DB=DB)
        sys.stdout.write(
            ">ref-%s?num_alts=%i&ref=%s\n" %
            (variant_panel.variant.var_hash, len(
                variant_panel.alts), variant_panel.variant.reference.id))
        sys.stdout.write("%s\n" % variant_panel.ref)
        for a in variant_panel.alts:
            sys.stdout.write(">alt-%s\n" % variant_panel.variant.var_hash)
            sys.stdout.write("%s\n" % a)
