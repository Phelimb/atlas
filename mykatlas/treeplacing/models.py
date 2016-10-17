from __future__ import print_function
import json
import sys
import os
import logging
import operator
import csv
from os import path
from ga4ghmongo.schema import Variant
from ga4ghmongo.schema import VariantSet
from ga4ghmongo.schema import VariantCall
from ga4ghmongo.schema import VariantCallSet
from mongoengine import DoesNotExist
from mykatlas.utils import lazyprop
sys.path.append(path.abspath("../"))

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
import redis

r = redis.StrictRedis('redis')


class Placer(object):

    """Placer"""

    def __init__(self, root=None, searchable_samples=None):
        super(Placer, self).__init__()
        self.tree = root
        self.searchable_samples = searchable_samples

    def place(self, sample, use_cache=True):
        # return self.exhaustive_overlap(sample, use_cache=use_cache)
        return self.dissimilarity(sample, use_cache=use_cache)

    def walker(self, sample, verbose=False):
        logger.debug("Placing sample %s on the tree" % sample)
        variant_calls = VariantCall.objects(
            call_set=VariantCallSet.objects.get(
                sample_id=sample, info={"variant_caller": "atlas"}))
        logger.debug("Using %i variant calls" % len(variant_calls))
        return self.root.search(variant_calls=variant_calls)

    # @property
    # def searchable_samples(self):
    #     if self.tree is not None:
    #         return self.tree.samples
    #     elif self.searchable_samples_file:
    #         searchable_samples = []
    #         with open(self.searchable_samples_file, 'r') as infile:
    #             reader = csv.reader(infile)
    #             for row in reader:
    #                 searchable_samples.extend(row)
    #         return searchable_samples
    #     else:
    #         return VariantCallSet.objects().distinct("sample_id")

    @property
    def searchable_callsets(self):
        callset_ids = VariantCallSet.objects(
            sample_id__in=self.searchable_samples, info={
                "variant_caller": "atlas"}).distinct("id")
        return callset_ids

    def _get_confident_variant_id(self, call_set):
        return VariantCall.objects(
            call_set=call_set,
            info__conf__gt=1,
            info__filter="PASS").distinct('variant')

    def _query_call_sets_for_distinct_variants(self):
        return VariantCall._get_collection().aggregate([
            {"$match": {
                "call_set": {"$in": self.searchable_callsets}
            }
            },
            {"$group": {
                "_id": {"call_set": "$call_set"},
                "variants": {"$addToSet": "$variant"}
            }
            }
        ], allowDiskUse=True)

    def _parse_distinct_variant_query(self, variant_call_sets):
        call_set_to_distinct_variants = {}
        for vc in variant_call_sets:
            # Update dict
            call_set_id = str(vc.get("_id").get("call_set"))
            variant_id_list = [str(v) for v in vc.get("variants")]
            call_set_to_distinct_variants[call_set_id] = variant_id_list
        return call_set_to_distinct_variants

    def _within_N_matches(self, sample_to_distance_metrics, N=250):
        out = {}
        sorted_sample_to_distance_metrics_keys = sorted(
            sample_to_distance_metrics.keys(),
            key=lambda x: (
                sample_to_distance_metrics[x]['ratio'],
                sample_to_distance_metrics[x]['intersection_count'],
                -sample_to_distance_metrics[x]['symmetric_difference_count']),
            reverse=True)
        for i, k in enumerate(sorted_sample_to_distance_metrics_keys):
            # if sample_to_distance_metrics[k]["symmetric_difference_count"] <
            # N:
            out[i] = {k: sample_to_distance_metrics[k]}
        return out

    def _load_call_set_to_distinct_variants_from_cache(self):
        logger.info("Loading distinct_variants query from cache")
        with open("/tmp/call_set_to_distinct_variants_cache.json", 'r') as infile:
            return json.load(infile)

    def _dump_call_set_to_distinct_variants_to_cache(
            self, call_set_to_distinct_variants):
        with open("/tmp/call_set_to_distinct_variants_cache.json", 'w') as outfile:
            json.dump(call_set_to_distinct_variants, outfile)

    def _calculate_call_set_to_distinct_variants(self):
        logger.info("Running distinct_variants query in DB")
        variant_call_sets = self._query_call_sets_for_distinct_variants()
        call_set_to_distinct_variants = self._parse_distinct_variant_query(
            variant_call_sets)
        self._dump_call_set_to_distinct_variants_to_cache(
            call_set_to_distinct_variants)
        return call_set_to_distinct_variants

    def _get_call_set_to_distinct_variants(self, use_cache):
        if use_cache:
            try:
                call_set_to_distinct_variants = self._load_call_set_to_distinct_variants_from_cache()
            except (IOError, ValueError):
                logger.info("Couldn't find cached query")
                call_set_to_distinct_variants = self._calculate_call_set_to_distinct_variants()
        else:
            call_set_to_distinct_variants = self._calculate_call_set_to_distinct_variants()
        return call_set_to_distinct_variants

    def _get_variant_call_set(self, query_sample):
        try:
            query_sample_call_set = VariantCallSet.objects.get(
                sample_id=query_sample, info={"variant_caller": "atlas"})
            return query_sample_call_set
        except DoesNotExist:
            raise ValueError(
                "\n\n%s does not exist in the database. \n\nPlease run `atlas genotype --save` before `atlas place` " %
                query_sample)

    def _get_genotype_dict(self, use_cache):
        if use_cache:
            try:
                call_set_to_genotype_dict = self._load_call_set_to_genotype_dict_from_cache()
            except (IOError, ValueError):
                logger.info("Couldn't find cached query")
                call_set_to_genotype_dict = self._calculate_call_set_to_genotype_dict()
        else:
            call_set_to_genotype_dict = self._calculate_call_set_to_genotype_dict()
        return call_set_to_genotype_dict

    def _calculate_call_set_to_genotype_dict(self):
        out = {}
        for call_set in self.searchable_callsets:
            logger.info("Extracting genotypes %s" % call_set)
            genotypes_compare = self._get_genotypes(call_set_id=call_set)
            out[str(call_set)] = genotypes_compare
        self._dump_call_set_to_genotype_dict_to_cache(out)
        return out

    def _load_call_set_to_genotype_dict_from_cache(self):
        logger.info("Loading distinct_variants query from cache")
        with open("/tmp/call_set_to_genotype_dict_cache.json", 'r') as infile:
            return json.load(infile)

    def _dump_call_set_to_genotype_dict_to_cache(
            self, call_set_to_genotype_dict):
        with open("/tmp/call_set_to_genotype_dict_cache.json", 'w') as outfile:
            json.dump(call_set_to_genotype_dict, outfile)

    def dissimilarity(self, query_sample, use_cache=True):
        sample_to_distance_metrics = {}
        logger.info("Extracting genotypes for query and DB")
        for sample in self.searchable_samples:
            diff_count = 0
            if str(sample) != str(query_sample) and r.get(
                    "%s_atlas_gt" % sample):
                XOR_KEY = "XOR_%s_%s_atlas_gt" % (query_sample, sample)
                XOR_AND_KEY = XOR_KEY + "_filtered"
                r.bitop(
                    "XOR",
                    XOR_KEY,
                    "%s_atlas_gt" %
                    query_sample,
                    "%s_atlas_gt" %
                    sample)
                r.bitop(
                    "AND",
                    XOR_AND_KEY,
                    XOR_KEY,
                    "%s_atlas_filtered" %
                    sample,
                    "%s_atlas_filtered" %
                    query_sample)
                diff_count = r.bitcount(XOR_AND_KEY)
                sample_to_distance_metrics[sample] = {}
                sample_to_distance_metrics[sample]["distance"] = diff_count
        return self._sort_dist(sample_to_distance_metrics)

    def _sort_dist(self, sample_to_distance_metrics):
        out = {}
        sorted_sample_to_distance_metrics_keys = sorted(
            sample_to_distance_metrics.keys(),
            key=lambda x: (
                sample_to_distance_metrics[x]['distance']),
            reverse=False)
        for i, k in enumerate(sorted_sample_to_distance_metrics_keys):
            out[i] = {k: sample_to_distance_metrics[k]}
        return out

    def _get_genotypes(self, call_set_id, variants=None):
        if variants:
            q = VariantCall.objects(
                call_set=call_set_id,
                variant__in=variants).only(
                'genotype',
                'info.conf',
                'variant').order_by('variant').as_pymongo()
        else:
            q = VariantCall.objects(
                call_set=call_set_id).only(
                'genotype',
                'info.conf',
                'variant').order_by('variant').as_pymongo()
        return [(sum(vc['genotype']), int(vc['info']['conf'] > 1)) for vc in q]

    def exhaustive_overlap(self, query_sample, use_cache=True):
        query_sample_call_set = self._get_variant_call_set(query_sample)
        call_set_to_distinct_variants = self._get_call_set_to_distinct_variants(
            use_cache)
        best_sample_symmetric_difference_count = 10000
        best_sample = None
        best_intersect = 0
        sample_to_distance_metrics = {}
        sample_variants_set = set([str(v.id) for v in VariantCall.objects(
            call_set=query_sample_call_set).distinct("variant")])
        logger.info(
            "calculating distinct metrics againsts all %i samples" %
            len(call_set_to_distinct_variants))
        for call_set_id, variant_id_list in call_set_to_distinct_variants.items(
        ):
            # Check similarity
            sample = VariantCallSet.objects.get(id=call_set_id).sample_id
            csvs = set(variant_id_list)
            intersection_count = len(csvs & sample_variants_set)
            symmetric_difference_count = len(csvs ^ sample_variants_set)
            in_query_not_in_searched_count = len(csvs - sample_variants_set)
            not_in_query_in_searched_count = len(sample_variants_set - csvs)
            if call_set_id != str(query_sample_call_set.id):
                sample_to_distance_metrics[sample] = {}
                sample_to_distance_metrics[sample][
                    "symmetric_difference_count"] = symmetric_difference_count
                sample_to_distance_metrics[sample][
                    "in_query_not_in_searched_count"] = in_query_not_in_searched_count
                sample_to_distance_metrics[sample][
                    "not_in_query_in_searched_count"] = not_in_query_in_searched_count
                sample_to_distance_metrics[sample][
                    "intersection_count"] = intersection_count
                sample_to_distance_metrics[sample]["ratio"] = float(
                    intersection_count) / float(symmetric_difference_count)
                if symmetric_difference_count < best_sample_symmetric_difference_count:
                    best_sample_symmetric_difference_count = symmetric_difference_count
                    best_sample = sample
                    best_intersect = intersection_count
        if best_intersect > 0:
            logger.info(
                "Finished searching %i samples - closest sample to %s is %s with %i overlapping variants and %i variants between them" %
                (len(call_set_to_distinct_variants),
                 query_sample,
                 best_sample,
                 best_intersect,
                 best_sample_symmetric_difference_count))
            return self._within_N_matches(sample_to_distance_metrics, N=1000)
        else:
            logger.info(
                "Finished searching %i samples - could not place %s as no samples had overlapping variants" %
                (len(call_set_to_distinct_variants), query_sample))
            return self._within_N_matches(sample_to_distance_metrics, N=0)


# class Tree(dict):
#     """Tree is defined by a dict of nodes"""
#     def __init__(self):
#         super(Tree, self).__init__()


def lazyprop(fn):
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazyprop(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazyprop


class Node(object):

    """docstring for Node"""

    def __init__(self, children=[]):
        super(Node, self).__init__()
        self.parent = None
        self.children = children  # List of nodes
        for child in self.children:
            child.add_parent(self)
        self._phylo_snps = None

    def add_parent(self, parent):
        self.parent = parent

    def other_child(self, node):
        for child in self.children:
            if child != node:
                return child

    @property
    def samples(self):
        samples = []
        for child in self.children:
            samples.extend(child.samples)
        return samples  # List of sample below node in tree

    def __str__(self):
        return "Node with children %s " % ",".join(self.samples)

    def __repr__(self):
        return "Node with children %s " % ",".join(self.samples)

    @property
    def num_samples(self):
        return len(self.samples)

    @property
    def is_leaf(self):
        return False

    @property
    def is_node(self):
        return True

    @property
    def in_group_call_sets(self):
        return VariantCallSet.objects(sample_id__in=self.samples)

    def count_number_of_ingroup_call_sets(self):
        return float(self.in_group_call_sets.count())

    @property
    def outgroup_call_set(self):
        if self.parent:
            return VariantCallSet.objects(
                sample_id__in=self.parent.other_child(self).samples)
        else:
            return []

    def count_number_of_outgroup_call_sets(self):
        if self.outgroup_call_set:
            return float(self.outgroup_call_set.count())
        else:
            return 0

    def query_variant_count(self, call_sets):
        variant_calls = VariantCall._get_collection().aggregate([
            {"$match": {
                "call_set": {"$in": [cs.id for cs in call_sets]}
            }
            },
            {"$group": {
                "_id": {"variant": "$variant"},
                "count": {"$sum": 1}
            }
            },
            {"$match": {
                "count": {"$gt": 0}
            }
            }
        ])
        counts = {}
        for res in variant_calls:
            counts[str(res.get("_id", {}).get("variant"))
                   ] = res.get("count", 0)
        return counts

    def calculate_phylo_snps(self):
        logger.debug("calculating phylo_snps for %s" % self)
        out_dict = {}
        number_of_ingroup_samples = self.count_number_of_ingroup_call_sets()
        logger.debug("Ingroup call sets %i" % number_of_ingroup_samples)
        number_of_outgroup_samples = self.count_number_of_outgroup_call_sets()
        logger.debug("Outgroup call sets %i" % number_of_outgroup_samples)

        logging.debug("Querying for in_group_variant_calls_counts")
        in_group_variant_calls_counts = self.query_variant_count(
            self.in_group_call_sets)
        logging.debug("Querying for out_group_variant_calls_counts")
        out_group_variant_calls_counts = self.query_variant_count(
            self.outgroup_call_set)

        for variant, count_ingroup in in_group_variant_calls_counts.items():
            ingroup_freq = float(count_ingroup) / number_of_ingroup_samples
            if number_of_outgroup_samples != 0:
                count_outgroup = out_group_variant_calls_counts.get(variant, 0)
                outgroup_freq = float(
                    count_outgroup) / number_of_outgroup_samples
            else:
                count_outgroup = 0
                outgroup_freq = 0
            # logging.debug(
            #     "%s has ingroup count %i freq %f.  outgroup count %i freq %f. Diff %f" %
            #     (variant,
            #      count_ingroup,
            #      ingroup_freq,
            #      count_outgroup,
            #      outgroup_freq,
            #      ingroup_freq -
            #      outgroup_freq))
            out_dict[variant] = ingroup_freq - outgroup_freq
        self._phylo_snps = out_dict
        return self._phylo_snps

    @lazyprop
    def phylo_snps(self):
        return self.calculate_phylo_snps()

    def search(self, variant_calls):
        assert self.children[0].parent is not None
        assert self.children[1].parent is not None
        logger.info(
            "step %s %s %s " %
            (self, self.children[0], self.children[1]))

        overlap = []
        # Get the overlapping SNPS
        variant_set = set([str(vc.variant.id) for vc in variant_calls])

        l0 = list(set(self.children[0].phylo_snps.keys()) & variant_set)
        l1 = list(set(self.children[1].phylo_snps.keys()) & variant_set)
        logger.info("left %i right %i " % (len(l0), len(l1)))
        count0 = 0
        count1 = 0
        for k in l0:
            count0 += self.children[0].phylo_snps[k]
        for k in l1:
            count1 += self.children[1].phylo_snps[k]
        overlap = (count0, count1)
        logger.info(
            "%s %s %s" %
            (self.children[0],
             self.children[1],
             overlap))
        if overlap[0] > overlap[1]:
            return self.children[0].search(variant_calls)
        elif overlap[1] > overlap[0]:
            return self.children[1].search(variant_calls)
        else:
            return self.samples


class Leaf(Node):

    def __init__(self, sample):

        super(Leaf, self).__init__()
        self.sample = sample

    @property
    def samples(self):
        return [self.sample]

    @property
    def is_leaf(self):
        return True

    @property
    def is_node(self):
        return False

    def search(self, variants):
        return self.sample

    def __repr__(self):
        return "Leaf : %s " % self.sample
