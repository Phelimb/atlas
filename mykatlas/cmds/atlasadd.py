import logging
import os
import csv
import json
from mongoengine import connect
from mongoengine import NotUniqueError
from mongoengine import OperationError
from mongoengine import DoesNotExist
from pymongo import MongoClient

from mykatlas.utils import check_args
from ga4ghmongo.schema import VariantCallSet
from ga4ghmongo.schema import VariantSet
from ga4ghmongo.schema import Variant
from ga4ghmongo.schema import VariantCall

from mykatlas._vcf import VCF
GLOBAL_VARIANT_SET_NAME = "global_atlas"

"""Adds variants to the database"""

logger = logging.getLogger(__name__)
client = MongoClient()


class AtlasGenotypeResult(object):

    def __init__(self, sample, method, data,force= False):
        self.sample = sample
        self.method = method
        self.data = data
        self.call_set = None
        self.force = force

    def add(self):
        self._create_call_sets()
        self._create_calls()

    def _create_call_sets(self):
        try:
            self.call_set = VariantCallSet.create_and_save(
                name="_".join(
                    [
                        self.sample,
                        self.method]),
                variant_sets=[self.global_variant_set],
                sample_id=self.sample,
                info={
                    "variant_caller": self.method})
        except NotUniqueError:
            if self.force:
                # logger.info("There is already a call set for sample %s with method %s but add has been called with --force so this callset is being removed from the DB" %
                #     (self.sample, self.method))
                cs = VariantCallSet.objects.get(name="_".join([
                        self.sample,
                        self.method]))
                VariantCall.objects(call_set = cs).delete()
                cs.delete()
                self._create_call_sets()
            else:
                raise ValueError(
                    "There is already a call set for sample %s with method %s " %
                    (self.sample, self.method))

    def _create_calls(self):
        calls = []
        for var_hash, call in self.data["variant_calls"].items():
            var_hash = var_hash[:64]
            v = Variant.objects.get(var_hash=var_hash)
            c = VariantCall.create(
                variant=v,
                call_set=self.call_set,
                genotype=call["genotype"],
                genotype_likelihoods=call["genotype_likelihoods"],
                info=call["info"])
            calls.append(c)
        VariantCall.objects.insert(calls)

    @property
    def global_variant_set(self):
        return VariantSet.objects.get(name=GLOBAL_VARIANT_SET_NAME)


def run(parser, args):
    args = parser.parse_args()
    args = check_args(args)
    if args.quiet:
        logger.setLevel(logging.ERROR)
    else:
        logger.setLevel(logging.INFO)
    DBNAME = 'atlas-%s' % (args.db_name)
    db = client[DBNAME]
    connect(DBNAME)
    logger.debug("Using DB %s" % DBNAME)

    for f in args.jsons:
        with open(f, 'r') as inf:
            data = json.load(inf)
        for sample, calls in data.items():
            AtlasGenotypeResult(sample, "atlas", calls, force = args.force).add()
