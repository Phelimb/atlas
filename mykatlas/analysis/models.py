from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import IntField
from mongoengine import ReferenceField
from mongoengine import ListField
from mongoengine import FloatField
from mongoengine import DictField
from mongoengine import GenericReferenceField
from mongoengine import BooleanField
from mongoengine import queryset_manager
import datetime
from ga4ghmongo.schema.models.base import CreateAndSaveMixin


class AnalysisResult(Document, CreateAndSaveMixin):

    meta = {'allow_inheritance': True}

    files = ListField(StringField())
    created_at = DateTimeField(default=datetime.datetime.now)
    version = DictField(required=True)

    @classmethod
    def create(cls):
        raise NotImplementedError("Implemented in subclass")
