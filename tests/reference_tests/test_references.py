from ga4ghmongo.schema.models.references import Reference
from ga4ghmongo.schema.models.references import ReferenceSet
from mongoengine import connect
DB = connect('atlas-test')


class BaseTest():

    def setUp(self):
        DB.drop_database('atlas-test')

    def teardown(self):
        DB.drop_database('atlas-test')


class TestReferenceSet(BaseTest):

    def test_create_reference_set(self):
        reference = ReferenceSet().create_and_save(name="ref_set")
        assert reference.name == "ref_set"
        r = ReferenceSet.objects.get(name="ref_set")
        assert r == reference


class TestReference(BaseTest):

    def setUp(self):
        self.reference_set = ReferenceSet.create_and_save(name="ref_set")

    def test_create_reference(self):
        reference = Reference().create_and_save(
            name="ref2",
            md5checksum="sre32",
            reference_sets=[
                self.reference_set])
        assert reference.name == "ref2"
        r = Reference.objects.get(name="ref2")
        assert r == reference
        assert r.reference_sets[0].name == "ref_set"
