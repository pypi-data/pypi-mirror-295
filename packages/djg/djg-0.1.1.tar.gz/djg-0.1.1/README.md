# DJG
DJG is a simple library and cli tool generating JSON objects based on a given schema.

*DJG is in very early development.*

Currently supported features:
 - number
 - string
 - array
 - enum & const for each type


## Installation
Install via pip
```bash
$ pip install djg
```

## Usage
#### As Python module
```python
from djg import gen_from_schema
import json

schema = {
    "type": "object",
    "properties": {
        "ProductIdentifier": {
            "type": "object",
            "properties": {
                "Name": {"type": "string", "pattern": "[a-zA-Z]{5,10}"},
                "Uid": {"type": "number", "minimum": 1000, "maximum": 100000},
            },
        },
        "ProductQuantity": {
            "type": "number",
            "minimum": 0,
            "maximum": 100,
        },
    },
}

json_object = gen_from_schema(schema)
```

#### CLI
```bash
djg --help

usage: djg.py [-h] -s SCHEMA_FILE [-o FILE]

djg - create random JSON objects based on a given schema.

options:
  -h, --help            show this help message and exit
  -s SCHEMA_FILE, --schema SCHEMA_FILE
                        JSON Schema loaction
  -o FILE, --output FILE
                        JSON output location - default is stdout
```
