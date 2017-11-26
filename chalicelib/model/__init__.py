import uuid

from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute
from pynamodb.indexes import AllProjection, LocalSecondaryIndex
from pynamodb.models import Model


class Song(Model):
    class Meta:
        table_name = 'mm-song'

    id = UnicodeAttribute(hash_key=True)
    owner = UnicodeAttribute()
    name = UnicodeAttribute()
    genre = UnicodeAttribute(null=True)
    file = UnicodeAttribute(null=True)
    shared = BooleanAttribute(default=False)

    @classmethod
    def uuid(cls):
        return 's-%s' % str(uuid.uuid4()).replace('-', '')[:8]


class User(Model):
    class Meta:
        table_name = 'mm-user'

    email = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    password = UnicodeAttribute()


class Token(Model):
    class Meta:
        table_name = 'mm-token'

    token = UnicodeAttribute(hash_key=True)
    valid = BooleanAttribute(default=False)
    create_at = UTCDateTimeAttribute()
