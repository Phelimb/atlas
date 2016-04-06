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

#     def test_single_node_no_children(self):
#         node = Node()
#         assert node.children == []
#         assert node.num_samples == 0
#         assert node.is_leaf is False

#     def test_node_triplet(self):
#         node1 = Leaf(sample='C1')
#         node2 = Leaf(sample='C2')
#         root = Node(children=[node1, node2])
#         assert root.num_samples == 2
#         assert root.samples == ['C1', 'C2']


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
        vs1 = VariantSet.create_and_save(
            name="C1", reference_set=self.reference_set)
        cs1 = VariantCallSet.create_and_save(
            sample_id="C1", name="C1", variant_sets=vs1)
        vs2 = VariantSet.create_and_save(
            name="C2", reference_set=self.reference_set)
        cs2 = VariantCallSet.create_and_save(
            sample_id="C2", name="C2", variant_sets=vs2)
        vs3 = VariantSet.create_and_save(
            name="C3", reference_set=self.reference_set)
        cs3 = VariantCallSet.create_and_save(
            sample_id="C3", name="C3", variant_sets=vs3)
        vs4 = VariantSet.create_and_save(
            name="C4", reference_set=self.reference_set)
        cs4 = VariantCallSet.create_and_save(
            sample_id="C4", name="C4", variant_sets=vs4)
        vs5 = VariantSet.create_and_save(
            name="C5", reference_set=self.reference_set)
        cs5 = VariantCallSet.create_and_save(
            sample_id="C5", name="C5", variant_sets=vs5)
        assert VariantCallSet.objects(sample_id__in=["C1", "C2"]).count() > 1

        self.v1 = Variant.create_and_save(variant_sets=[vs1.id],
                                          start=1,
                                          end=2,
                                          reference_bases="A",
                                          alternate_bases=["T"],
                                          reference=self.ref)

        self.v2 = Variant.create_and_save(variant_sets=[vs2.id],
                                          start=2,
                                          end=2,
                                          reference_bases="A",
                                          alternate_bases=["T"],
                                          reference=self.ref)

        self.v3 = Variant.create_and_save(variant_sets=[vs3.id],
                                          start=3,
                                          end=2,
                                          reference_bases="A",
                                          alternate_bases=["T"],
                                          reference=self.ref)

        self.v4 = Variant.create_and_save(variant_sets=[vs4.id],
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

    def test_multi_node(self):
        assert self.root.num_samples == 5
        assert sorted(self.root.samples) == ['C1', 'C2', 'C3', 'C4', 'C5']

    def test_phylo_snps(self):
        print (self.node1.phylo_snps)
        assert self.node1.count_number_of_ingroup_call_sets() > 0
        assert self.node1.phylo_snps == {self.v1: 0.5, self.v2: 0.5}
        assert self.node2.phylo_snps == {self.v4: 1}
        assert self.node3.phylo_snps == {
            self.v3: 0.3333333333333333,
            self.v4: 0.6666666666666666}
        assert self.root.phylo_snps == {
            self.v1: 0.2,
            self.v2: 0.2,
            self.v3: 0.2,
            self.v4: 0.4}

        assert self.l1.phylo_snps == {self.v1: 1}
        assert self.l2.phylo_snps == {self.v2: 1}
        assert self.l3.phylo_snps == {self.v3: 1}
        print (self.l4.phylo_snps)
        assert self.l4.phylo_snps == {self.v4: 0}
        assert self.l5.phylo_snps == {self.v5: 0}

#     def test_placement(self):
#         new_call_set = VariantCallSet.create(sample_id="123", name="C6")
#         VariantCall.create(
#             name="A1T",
#             call_set=new_call_set.id,
#             reference_median_depth=0,
#             reference_percent_coverage=100,
#             alternate_median_depth=0,
#             alternate_percent_coverage=30,
#             gt="1/1")
#         assert Placer(root=self.root).place("C6") == "C1"

#     def test_abigious_placement(self):
#         new_call_set = VariantCallSet.create(sample_id="123", name="C7")
#         VariantCall.create(
#             name="A4T",
#             call_set=new_call_set.id,
#             reference_median_depth=0,
#             reference_percent_coverage=100,
#             alternate_median_depth=0,
#             alternate_percent_coverage=30,
#             gt="1/1")
#         assert Placer(root=self.root).place("C7") == ["C4", "C5"]


# class TestMultiNodeHomoplasy(TestNodes):

#     def setUp(self):
#         DB.drop_database(DBNAME)
#         c.drop_database(DBNAME)
#         Reference.drop_collection()

#         self.l1 = Leaf(sample='C1')
#         self.l2 = Leaf(sample='C2')
#         self.l3 = Leaf(sample='C3')
#         self.l4 = Leaf(sample='C4')
#         self.l5 = Leaf(sample='C5')

#         self.node1 = Node(children=[self.l1, self.l2])
#         assert self.l1.parent == self.node1
#         assert self.l2.parent == self.node1
#         self.node2 = Node(children=[self.l4, self.l5])
#         self.node3 = Node(children=[self.node2, self.l3])
#         self.root = Node(children=[self.node1, self.node3])
#         self.ref = Reference.create(
#             name="ref1",
#             length=10000,
#             source_accessions="SRA_ABC123")
#         vs1 = VariantSet.create(name="C1")
#         cs1 = VariantCallSet.create(sample_id="123", name="C1")
#         vs2 = VariantSet.create(name="C2")
#         cs2 = VariantCallSet.create(sample_id="123", name="C2")
#         vs3 = VariantSet.create(name="C3")
#         cs3 = VariantCallSet.create(sample_id="123", name="C3")
#         vs4 = VariantSet.create(name="C4")
#         cs4 = VariantCallSet.create(sample_id="123", name="C4")
#         vs5 = VariantSet.create(name="C5")
#         cs5 = VariantCallSet.create(sample_id="123", name="C5")

#         self.v1 = Variant.create(variant_set=vs1.id,
#                                  start=1,
#                                  end=2,
#                                  reference_bases="A",
#                                  alternate_bases=["T"],
#                                  reference=self.ref.id)

#         self.v2 = Variant.create(variant_set=vs2.id,
#                                  start=2,
#                                  end=2,
#                                  reference_bases="A",
#                                  alternate_bases=["T"],
#                                  reference=self.ref.id)

#         self.v3 = Variant.create(variant_set=vs3.id,
#                                  start=3,
#                                  end=2,
#                                  reference_bases="A",
#                                  alternate_bases=["T"],
#                                  reference=self.ref.id)

#         self.v4 = Variant.create(variant_set=vs4.id,
#                                  start=4,
#                                  end=2,
#                                  reference_bases="A",
#                                  alternate_bases=["T"],
#                                  reference=self.ref.id)

#         self.v5 = Variant.create(variant_set=vs5.id,
#                                  start=1,
#                                  end=2,
#                                  reference_bases="A",
#                                  alternate_bases=["T"],
#                                  reference=self.ref.id)

#         VariantCall.create(
#             variant=self.v1.id,
#             call_set=cs1.id,
#             genotype="0/1",
#             genotype_likelihood=0.91)
#         VariantCall.create(
#             variant=self.v2.id,
#             call_set=cs1.id,
#             genotype="0/1",
#             genotype_likelihood=0.91)
#         VariantCall.create(
#             variant=self.v3.id,
#             call_set=cs1.id,
#             genotype="0/1",
#             genotype_likelihood=0.91)
#         VariantCall.create(
#             variant=self.v4.id,
#             call_set=cs1.id,
#             genotype="0/1",
#             genotype_likelihood=0.91)
#         VariantCall.create(
#             variant=self.v5.id,
#             call_set=cs1.id,
#             genotype="0/1",
#             genotype_likelihood=0.91)

#     def test_multi_node(self):
#         assert self.root.num_samples == 5
#         assert sorted(self.root.samples) == ['C1', 'C2', 'C3', 'C4', 'C5']

#     def test_phylo_snps(self):
#         assert self.node1.phylo_snps == {
#             self.v1.name: 0.5 -
#             0.3333333333333333,
#             self.v2.name: 0.5}
#         assert self.node2.phylo_snps == {self.v1.name: 0.5, self.v4.name: 0.5}
#         assert self.node3.phylo_snps == {
#             self.v1.name: 0.3333333333333333 - 0.5,
#             self.v3.name: 0.3333333333333333,
#             self.v4.name: 0.3333333333333333}
#         assert self.root.phylo_snps == {
#             self.v1.name: 0.4,
#             self.v2.name: 0.2,
#             self.v3.name: 0.2,
#             self.v4.name: 0.2}

#         assert self.l1.phylo_snps == {self.v1.name: 1}
#         assert self.l2.phylo_snps == {self.v2.name: 1}
#         assert self.l3.phylo_snps == {self.v3.name: 1}
#         assert self.l4.phylo_snps == {self.v4.name: 1}
#         assert self.l5.phylo_snps == {self.v1.name: 1}

#     def test_placement(self):
#         new_call_set = VariantCallSet.create(sample_id="123", name="C8")
#         VariantCall.create(
#             name="A1T",
#             call_set=new_call_set.id,
#             reference_median_depth=0,
#             reference_percent_coverage=100,
#             alternate_median_depth=0,
#             alternate_percent_coverage=30,
#             gt="1/1")
#         # Note - I think the commented line hear should be correct behaviour
#         Placer(root=self.root).place("C8") == ["C1"]
#         # print Placer(root = self.root).place("C8", verbose=True)
#         # assert sorted(Placer(root = self.root).place("C8")) == sorted(['C1', 'C2', 'C3', 'C4', 'C5'])

#     def test_abigious_placement(self):
#         new_call_set = VariantCallSet.create(sample_id="123", name="C9")
#         VariantCall.create(
#             name="A4T",
#             call_set=new_call_set.id,
#             reference_median_depth=0,
#             reference_percent_coverage=100,
#             alternate_median_depth=0,
#             alternate_percent_coverage=30,
#             gt="1/1")
#         assert Placer(root=self.root).place("C9") == "C4"
