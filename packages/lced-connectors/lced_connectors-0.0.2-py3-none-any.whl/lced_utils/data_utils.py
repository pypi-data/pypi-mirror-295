import json


def parse_val(val, val_type):
    new_val = val
    if isinstance(val, bytes) or isinstance(val, bytearray):
        new_val = val.decode("utf-8")
    if isinstance(val, list):
        val_list = []
        for item in val:
            val_item = parse_val(item, None)
            val_list.append(val_item)
        if val_type == list:
            return val_list
        else:
            new_val = val_list
    if type(new_val) != val_type:
        if val_type == int:
            return int(new_val)
        elif val_type == str and isinstance(new_val, list):
            return new_val[0]
        elif val_type == dict:
            return json.loads(new_val)
        else:
            return new_val
    return new_val
