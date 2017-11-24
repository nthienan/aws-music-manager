import uuid

from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import AllProjection, LocalSecondaryIndex
from pynamodb.models import Model


class OwnerIndex(LocalSecondaryIndex):
    class Meta:
        projection = AllProjection()

    id = UnicodeAttribute(hash_key=True)
    owner = UnicodeAttribute(range_key=True)


class Song(Model):
    class Meta:
        table_name = 'mm-song'

    id = UnicodeAttribute(hash_key=True)
    owner = UnicodeAttribute()
    name = UnicodeAttribute(range_key=True)
    genre = UnicodeAttribute()
    file = UnicodeAttribute()
    owner_index = OwnerIndex()

    @classmethod
    def uuid(cls):
        return 's-%s' % str(uuid.uuid4()).replace('-', '')[:8]


class User(Model):
    class Meta:
        table_name = 'mm-user'

    name = UnicodeAttribute(range_key=True)
    email = UnicodeAttribute(hash_key=True)
    password = UnicodeAttribute()
