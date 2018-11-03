from jsonschema import validate
import json

with open('border.schema.json') as fp:
    schema = json.load(fp)

with open('data.json') as fp:
    data = json.load(fp)

validate(data, schema)
