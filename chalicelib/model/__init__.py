from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model


class Song(Model):
    class Meta:
        table_name = 'mm-song'

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute(range_key=True)
    genre = UnicodeAttribute()
