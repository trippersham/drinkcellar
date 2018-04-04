from google.cloud import datastore
from text_utils import convert_to_camel_case
import uuid

datastore_client = datastore.Client()

kinds = [
    'BottleData',
    'Review',
    'FoodPairing',
    'Bottle',
    'Place',
    'Brand',
    'Grape'
]

def create_entity(kind, data, unique_name=None, parent_key=None):
    if kind not in kinds:
        raise ValueError('Kind ' + kind + ' is not supported')

    name = unique_name if unique_name else str(uuid.uuid4())
    key = datastore_client.key(kind, name, parent=parent_key)
    entity = datastore.Entity(key=key)

    for k,v in data.items():
        if isinstance(v, dict):
            create_entity(convert_to_camel_case(k), v, parent_key=key)
        elif isinstance(v, list):
            for l in v:
                print(l)
                create_entity(convert_to_camel_case(k)[:-1], l, parent_key=key)
        else:
            entity[k] = v

    datastore_client.put(entity)
    return entity
