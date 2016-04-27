import json
import uuid
import time

__author__ = 'alivinco'


class PayloadType:
    # Fisrt version of IOT JSON message format
    JSON_IOT_MSG_V0 = 0
    # Current version of IOT JSON message format
    JSON_IOT_MSG_V1 = 1
    # Opaque JSON message , which can't be mapped to IOT Msg object
    JSON_OPAQUE = 2
    # Binary encoded IOT message format
    BINARY_IOT_MSG_V1 = 3
    # Payload is a single value
    BINARY_VALUE = 4
    # Opaque binary payload
    BINARY_OPAQUE = 5

    str_to_type_map = {"jim0": JSON_IOT_MSG_V0,
                       "jim1": JSON_IOT_MSG_V1,
                       "jopq": JSON_OPAQUE,
                       "bim1": BINARY_IOT_MSG_V1,
                       "bval": BINARY_VALUE,
                       "bopq": BINARY_OPAQUE}

    @classmethod
    def get_type(cls, type_):
        inv_map = {v: k for k, v in cls.str_to_type_map.items()}
        return inv_map[type_]


class MsgType:
    CMD = 1
    EVT = 2
    GET = 3


def get_uuid():
    return str(uuid.uuid4())


def get_timestamp():
    return int(time.time()) * 1000


class IotMsg:
    def __init__(self, origin, msg_type=MsgType.CMD, msg_class=None, msg_subclass=None, timestamp=get_timestamp(), uuid_=get_uuid(),corid=None):
        self.origin = origin
        self.msg_type = msg_type
        self.msg_class = msg_class
        self.msg_subclass = msg_subclass
        self.default = None
        self.properties = None
        self.topic = None
        self.timestamp = timestamp
        self.uuid = uuid_
        self.corid = corid

    def get_type(self):
        return self.msg_type

    def is_event(self):
        return True if self.msg_type == MsgType.EVT else False

    def is_command(self):
        return True if self.msg_type == MsgType.CMD else False

    def get_uuid(self):
        return self.uuid

    def get_corid(self):
        return self.corid

    def set_default(self, value, unit=None, type_=None):
        """

        :param value:
        :param unit:
        :param type_:
        """
        v = {"value":value}
        if unit:
            v["unit"] = unit
        if type_ :
            v["type"] = type_

        self.default = v

    def get_default(self):
        return self.default

    def get_default_value(self):
         return self.default["value"]

    def set_properties(self, props):
        self.properties = props

    def get_properties(self):
        return self.properties

    def get_msg_class(self):
        return self.msg_class

    def get_msg_subclass(self):
        return self.msg_subclass

    def __str__(self):
        return "msg_type = %s , msg_class = %s , msg_subclass = %s \n default : %s  \n properties : %s \n uuid : %s \n corid : %s \n"%(
                self.msg_type, self.msg_class, self.msg_subclass , self.default , self.properties , self.uuid ,self.corid
        )


if __name__ == '__main__':
    m = IotMsg.new_iot_msg("blackflow", "command", "binary", "switch")
    m.set_default(True)
    m.set_properties({"p1":165})
    print json.dumps(m.get_dict())
    json_str = '{"origin": {"@id": "blackflow", "@type": "app"}, "event": {"default": {"value": true}, "subtype": "switch", "@type": "binary", "properties": {"p1": 165}}, "creation_time": 1459696245000, "uuid": "e48fbe58-3aaf-442d-b769-7a24aed8b716", "spid": "SP1"}'
    m2 = IotMsg.new_iot_msg_from_dict("blackflow", json.loads(json_str))
    print m2.get_default()["value"]
    print m2.get_properties()
    print m2.get_msg_class()
    print m2.get_msg_subclass()
