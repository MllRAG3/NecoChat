import json


class JsonConverter:
    def __init__(self, obj):
        self.obj = obj
        self.type = str(type(obj))

    @property
    def json(self) -> str:
        ALLOWED_TYPES = {
            "<class 'ChatPermissions'>": self.convert_chat_permissions,
            "<class 'NoneType'>": self.none
        }
        if self.type not in ALLOWED_TYPES.keys(): raise TypeError
        return ALLOWED_TYPES[self.type]()

    @staticmethod
    def none() -> str:
        return "{}"

    def convert_chat_permissions(self) -> str:
        data = self.obj.__dict__
        del data["_client"]
        return json.dumps(data)
