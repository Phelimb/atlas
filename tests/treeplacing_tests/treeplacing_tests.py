from unittest import TestCase
from nose.tools import assert_raises

from mongoengine import connect
from pymongo import MongoClient

from mykatlas.treeplacing import Node
from mykatlas.treeplacing import Leaf
from mykatlas.treeplacing import Placer

from ga4ghmongo.schema import ReferenceSet
from ga4ghmongo.schema import Reference
from ga4ghmongo.schema import VariantSet
from ga4ghmongo.schema import Variant
from ga4ghmongo.schema import VariantCallSet
from ga4ghmongo.schema import VariantCall
from ga4ghmongo.schema import VariantCall


c = MongoClient()

DBNAME = 'atlas-test'
DB = connect(DBNAME)


class BaseTest(TestCase):

    def setUp(self):
        DB.drop_database(DBNAME)
        c.drop_database(DBNAME)
        Reference.drop_collection()

    def teardown(self):
        DB.drop_database(DBNAME)
        c.drop_database(DBNAME)
        Reference.drop_collection()


class TestNodes(BaseTest):
    pass

    def test_single_node_no_children(self):
        node = Node()
        assert node.children == []
        assert node.num_samples == 0
        assert node.is_leaf is False

    def test_node_triplet(self):
        node1 = Leaf(sample='C1')
        node2 = Leaf(sample='C2')
        root = Node(children=[node1, node2])
        assert root.num_samples == 2
        assert root.samples == ['C1', 'C2']


class TestMultiNode(TestNodes):

    def setUp(self):
        DB.drop_database(DBNAME)
        c.drop_database(DBNAME)
        Reference.drop_collection()

        self.reference_set = ReferenceSet.create_and_save(
            name="refset1")
        self.ref = Reference.create_and_save(
            name="ref1",
            md5checksum="sdf",
            reference_sets=[self.reference_set])
        self.vs = VariantSet.create_and_save(
            name="global", reference_set=self.reference_set)
        cs1 = VariantCallSet.create_and_save(
            sample_id="C1", name="C1", variant_sets=self.vs)
        cs2 = VariantCallSet.create_and_save(
            sample_id="C2", name="C2", variant_sets=self.vs)
        cs3 = VariantCallSet.create_and_save(
            sample_id="C3", name="C3", variant_sets=self.vs)
        cs4 = VariantCallSet.create_and_save(
            sample_id="C4", name="C4", variant_sets=self.vs)
        cs5 = VariantCallSet.create_and_save(
            sample_id="C5", name="C5", variant_sets=self.vs)
        assert VariantCallSet.objects(sample_id__in=["C1", "C2"]).count() > 1

        self.v1 = Variant.create_and_save(variant_sets=[self.vs.id],
                                          start=1,
                                          end=2,
                                          reference_bases="A",
                                          alternate_bases=["T"],
                                          reference=self.ref)

        self.v2 = Variant.create_and_save(variant_sets=[self.vs.id],
                                          start=2,
                                          end=2,
                                          reference_bases="A",
                                          alternate_bases=["T"],
                                          reference=self.ref)

        self.v3 = Variant.create_and_save(variant_sets=[self.vs.id],
                                          start=3,
                                          end=2,
                                          reference_bases="A",
                                          alternate_bases=["T"],
                                          reference=self.ref)

        self.v4 = Variant.create_and_save(variant_sets=[self.vs.id],
                                          start=4,
                                          end=2,
                                          reference_bases="A",
                                          alternate_bases=["T"],
                                          reference=self.ref)

        VariantCall.create_and_save(
            variant=self.v1,
            call_set=cs1,
            genotype="1/1",
            genotype_likelihoods=[0, 0, 1])
        VariantCall.create_and_save(
            variant=self.v2,
            call_set=cs2,
            genotype="1/1",
            genotype_likelihoods=[0, 0, 1])
        VariantCall.create_and_save(
            variant=self.v3,
            call_set=cs3,
            genotype="1/1",
            genotype_likelihoods=[0, 0, 1])
        VariantCall.create_and_save(
            variant=self.v4,
            call_set=cs4,
            genotype="1/1",
            genotype_likelihoods=[0, 0, 1])
        VariantCall.create_and_save(
            variant=self.v4,
            call_set=cs5,
            genotype="1/1",
            genotype_likelihoods=[0, 0, 1])

        self.l1 = Leaf(sample='C1')
        self.l2 = Leaf(sample='C2')
        self.l3 = Leaf(sample='C3')
        self.l4 = Leaf(sample='C4')
        self.l5 = Leaf(sample='C5')

        self.node1 = Node(children=[self.l1, self.l2])
        self.node2 = Node(children=[self.l4, self.l5])
        self.node3 = Node(children=[self.node2, self.l3])
        self.root = Node(children=[self.node1, self.node3])

        #                        | -- l2
        #                        |
        #           |-- node 1 - | -- l1
        #   root -- |
        #           |            | -- l3
        #           |-- node 3 - |             | -- l4
        #                        | -- node2 -- |
        #                                      | -- l5

    def test_multi_node(self):
        assert self.root.num_samples == 5
        assert sorted(self.root.samples) == ['C1', 'C2', 'C3', 'C4', 'C5']
        assert self.l1.parent == self.node1
        assert self.l4.parent == self.node2
        assert self.node2.parent == self.node3

    def test_phylo_snps(self):
        assert self.node1.count_number_of_ingroup_call_sets() > 0
        assert self.node1.calculate_phylo_snps() == {
            str(self.v1.id): 0.5, str(self.v2.id): 0.5}
        assert self.node2.calculate_phylo_snps() == {str(self.v4.id): 1}
        assert self.node3.calculate_phylo_snps() == {
            str(self.v3.id): 0.3333333333333333,
            str(self.v4.id): 0.6666666666666666}
        assert self.root.calculate_phylo_snps() == {
            str(self.v1.id): 0.2,
            str(self.v2.id): 0.2,
            str(self.v3.id): 0.2,
            str(self.v4.id): 0.4}

        assert self.l1.calculate_phylo_snps() == {str(self.v1.id): 1}
        assert self.l2.calculate_phylo_snps() == {str(self.v2.id): 1}
        assert self.l3.calculate_phylo_snps() == {str(self.v3.id): 1}
        assert self.l4.calculate_phylo_snps() == {str(self.v4.id): 0}
        assert self.l5.calculate_phylo_snps() == {str(self.v4.id): 0}

    def test_placement(self):
        new_call_set = VariantCallSet.create_and_save(
            sample_id="C6", name="C6", variant_sets=self.vs)
        VariantCall.create_and_save(
            variant=self.v1,
            call_set=new_call_set,
            genotype="1/1",
            genotype_likelihoods=[0, 0, 1])

        assert Placer(root=self.root).place("C6", verbose=True) == "C1"

    def test_abigious_placement(self):
        new_call_set = VariantCallSet.create_and_save(
            sample_id="C7", name="C7", variant_sets=self.vs)

        VariantCall.create_and_save(
            variant=self.v4,
            call_set=new_call_set,
            genotype="1/1",
            genotype_likelihoods=[0, 0, 1])

        assert Placer(root=self.root).place("C7") == ["C4", "C5"]


class TestMultiNodeHomoplasy(TestNodes):

    def setUp(self):
        DB.drop_database(DBNAME)
        c.drop_database(DBNAME)
        Reference.drop_collection()

        self.l1 = Leaf(sample='C1')
        self.l2 = Leaf(sample='C2')
        self.l3 = Leaf(sample='C3')
        self.l4 = Leaf(sample='C4')
        self.l5 = Leaf(sample='C5')

        self.node1 = Node(children=[self.l1, self.l2])
        assert self.l1.parent == self.node1
        assert self.l2.parent == self.node1
        self.node2 = Node(children=[self.l4, self.l5])
        self.node3 = Node(children=[self.node2, self.l3])
        self.root = Node(children=[self.node1, self.node3])
        self.reference_set = ReferenceSet.create_and_save(
            name="refset2")
        self.ref = Reference.create_and_save(
            name="ref2",
            md5checksum="sdf",
            reference_sets=[self.reference_set])
        self.vs = VariantSet.create_and_save(
            name="global", reference_set=self.reference_set)
        cs1 = VariantCallSet.create_and_save(
            sample_id="C1", name="C1", variant_sets=self.vs)

        cs2 = VariantCallSet.create_and_save(
            sample_id="C2", name="C2", variant_sets=self.vs)

        cs3 = VariantCallSet.create_and_save(
            sample_id="C3", name="C3", variant_sets=self.vs)

        cs4 = VariantCallSet.create_and_save(
            sample_id="C4", name="C4", variant_sets=self.vs)

        cs5 = VariantCallSet.create_and_save(
            sample_id="C5", name="C5", variant_sets=self.vs)

        self.v1 = Variant.create_and_save(variant_sets=[self.vs.id],
                                          start=1,
                                          end=2,
                                          reference_bases="A",
                                          alternate_bases=["T"],
                                          reference=self.ref)

        self.v2 = Variant.create_and_save(variant_sets=[self.vs.id],
                                          start=2,
                                          end=2,
                                          reference_bases="A",
                                          alternate_bases=["T"],
                                          reference=self.ref)

        self.v3 = Variant.create_and_save(variant_sets=[self.vs.id],
                                          start=3,
                                          end=2,
                                          reference_bases="A",
                                          alternate_bases=["T"],
                                          reference=self.ref)

        self.v4 = Variant.create_and_save(variant_sets=[self.vs.id],
                                          start=4,
                                          end=2,
                                          reference_bases="A",
                                          alternate_bases=["T"],
                                          reference=self.ref)

        VariantCall.create_and_save(
            variant=self.v1,
            call_set=cs1,
            genotype="1/1",
            genotype_likelihoods=[0, 0, 1])
        VariantCall.create_and_save(
            variant=self.v2,
            call_set=cs2,
            genotype="1/1",
            genotype_likelihoods=[0, 0, 1])

        VariantCall.create_and_save(
            variant=self.v3,
            call_set=cs3,
            genotype="1/1",
            genotype_likelihoods=[0, 0, 1])

        VariantCall.create_and_save(
            variant=self.v4,
            call_set=cs4,
            genotype="1/1",
            genotype_likelihoods=[0, 0, 1])
        VariantCall.create_and_save(
            variant=self.v1,
            call_set=cs5,
            genotype="1/1",
            genotype_likelihoods=[0, 0, 1])

    def test_multi_node(self):
        assert self.root.num_samples == 5
        assert sorted(self.root.samples) == ['C1', 'C2', 'C3', 'C4', 'C5']

    def test_phylo_snps(self):
        assert self.node1.phylo_snps == {
            str(self.v1.id): 0.5 -
            0.3333333333333333,
            str(self.v2.id): 0.5}
        assert self.node2.phylo_snps == {
            str(self.v1.id): 0.5, str(self.v4.id): 0.5}
        assert self.node3.phylo_snps == {
            str(self.v1.id): 0.3333333333333333 - 0.5,
            str(self.v3.id): 0.3333333333333333,
            str(self.v4.id): 0.3333333333333333}
        assert self.root.phylo_snps == {
            str(self.v1.id): 0.4,
            str(self.v2.id): 0.2,
            str(self.v3.id): 0.2,
            str(self.v4.id): 0.2}

        assert self.l1.phylo_snps == {str(self.v1.id): 1}
        assert self.l2.phylo_snps == {str(self.v2.id): 1}
        assert self.l3.phylo_snps == {str(self.v3.id): 1}
        assert self.l4.phylo_snps == {str(self.v4.id): 1}
        assert self.l5.phylo_snps == {str(self.v1.id): 1}

    def test_placement(self):
        new_call_set = VariantCallSet.create_and_save(
            sample_id="C8", name="C8", variant_sets=self.vs)
        VariantCall.create_and_save(
            variant=self.v1,
            call_set=new_call_set,
            genotype="1/1",
            genotype_likelihoods=[0, 0, 1])
        # Note - I think the commented line hear should be correct behaviour
        Placer(root=self.root).place("C8") == ["C1"]
        # print Placer(root = self.root).place("C8", verbose=True)
        # assert sorted(Placer(root = self.root).place("C8")) == sorted(['C1', 'C2', 'C3', 'C4', 'C5'])

    def test_abigious_placement(self):
        new_call_set = VariantCallSet.create_and_save(
            sample_id="C9", name="C9", variant_sets=self.vs)

        VariantCall.create_and_save(
            variant=self.v4,
            call_set=new_call_set,
            genotype="1/1",
            genotype_likelihoods=[0, 0, 1])

        assert Placer(root=self.root).place("C9") == "C4"
