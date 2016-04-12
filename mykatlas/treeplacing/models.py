from __future__ import print_function
import sys
import os
import logging
from os import path
from ga4ghmongo.schema import Variant
from ga4ghmongo.schema import VariantSet
from ga4ghmongo.schema import VariantCall
from ga4ghmongo.schema import VariantCallSet
from mykatlas.utils import lazyprop
sys.path.append(path.abspath("../"))

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Placer(object):

    """Placer"""

    def __init__(self, root):
        super(Placer, self).__init__()
        self.root = root

    def place(self, sample, verbose=False):
        logger.debug("Placing sample %s on the tree" % sample)
        variant_calls = VariantCall.objects(
            call_set=VariantCallSet.objects.get(
                sample_id=sample))
        logger.debug("Using %i variant calls" % len(variant_calls))        
        return self.root.search(variant_calls=variant_calls)

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

    def query_variant_count(self, call_sets, variants):
        variant_calls = VariantCall._get_collection().aggregate([
                {"$match" : {
                    "call_set" : {"$in" : [cs.id for cs in call_sets]},
                    "variant" : {"$in" : [v.id for v in variants]}
                    }
                },
                {"$group" : { 
                    "_id" : {"variant" : "$variant"},
                    "count" : {"$sum" : 1}
                    }
                },
                {"$match" : {
                    "count" : {"$gt" : 0}
                    }
                }
            ])
        counts = {}
        for res in variant_calls:
            counts[str(res.get("_id", {}).get("variant"))] = res.get("count", 0)
        return counts

    def calculate_phylo_snps(self):
        logger.debug("calculating phylo_snps for %s" % self)    
        out_dict = {}
        number_of_ingroup_samples = self.count_number_of_ingroup_call_sets()
        logger.debug("Ingroup call sets %i" % number_of_ingroup_samples)    
        number_of_outgroup_samples = self.count_number_of_outgroup_call_sets()
        logger.debug("Outgroup call sets %i" % number_of_outgroup_samples)    

        variants = VariantCall.objects(
            call_set__in=self.in_group_call_sets).distinct('variant')
        logging.debug("%i variant_calls" % len(variants))

        logging.debug("Querying for in_group_variant_calls_counts")        
        in_group_variant_calls_counts = self.query_variant_count(self.in_group_call_sets, variants)
        logging.debug("Querying for out_group_variant_calls_counts")                
        out_group_variant_calls_counts = self.query_variant_count(self.outgroup_call_set, variants)

        for variant in variants:
            variant = str(variant.id)
            count_ingroup = in_group_variant_calls_counts.get(variant, 0)
            ingroup_freq = float(count_ingroup) / number_of_ingroup_samples
            if number_of_outgroup_samples != 0:
                count_outgroup = out_group_variant_calls_counts.get(variant, 0)
                outgroup_freq = float(
                    count_outgroup) / number_of_outgroup_samples
            else:
                count_outgroup = 0
                outgroup_freq = 0
            logging.debug("%s has ingroup count %i freq %f.  outgroup count %i freq %f. Diff %f" % (variant, count_ingroup, ingroup_freq, count_outgroup, outgroup_freq, ingroup_freq - outgroup_freq))                
            out_dict[variant] = ingroup_freq - outgroup_freq
        self._phylo_snps = out_dict
        return self._phylo_snps

    @lazyprop
    def phylo_snps(self):
        return self.calculate_phylo_snps()

    def search(self, variant_calls):
        assert self.children[0].parent is not None
        assert self.children[1].parent is not None
        logging.info("step %s %s %s " % (self, self.children[0], self.children[1]))

        overlap = []
        # Get the overlapping SNPS
        variant_set = set([str(vc.variant.id) for vc in variant_calls])
        logging.info("step %s %s %s" % (self, self.children[0], self.children[1]))

        l0 = list(set(self.children[0].phylo_snps.keys()) & variant_set)
        l1 = list(set(self.children[1].phylo_snps.keys()) & variant_set)
        logging.info("left %i right %i " % (len(l0), len(l1)))
        count0 = 0
        count1 = 0
        for k in l0:
            count0 += self.children[0].phylo_snps[k]
        for k in l1:
            count1 += self.children[1].phylo_snps[k]
        overlap = (count0, count1)
        logging.info("%s %s %s" % (self.children[0], self.children[1], overlap))
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
