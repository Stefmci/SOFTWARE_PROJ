from datetime import datetime, date
from tinydb.storages import JSONStorage
from tinydb_serialization import Serializer, SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer

class DateSerializer(Serializer):
    OBJ_CLASS = date

    def encode(self, obj):
        return obj.isoformat()

    def decode(self, s):
        try:
            return date.fromisoformat(s)
        except AttributeError:
            return datetime.strptime(s, "%Y-%m-%d").date()

serializer = SerializationMiddleware(JSONStorage)
serializer.register_serializer(DateTimeSerializer(), 'TinyDateTime')
serializer.register_serializer(DateSerializer(), 'TinyDate')
