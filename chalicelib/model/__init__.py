from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute
from pynamodb.indexes import LocalSecondaryIndex, AllProjection
from pynamodb.models import Model


class SongUserView(LocalSecondaryIndex):
    class Meta:
        projection = AllProjection()

    id = UnicodeAttribute(hash_key=True)
    user = UnicodeAttribute(range_key=True)


class Song(Model):
    class Meta:
        table_name = 'mm-song'

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute(range_key=True)
    genre = UnicodeAttribute()
    file = UnicodeAttribute()
    user = UnicodeAttribute()
    owner_view = SongUserView()
