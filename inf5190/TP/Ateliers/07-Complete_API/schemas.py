# noinspection PyInterpreter
insert_personne_schema = {
    "$schema": "http://json-schema.org/draft-03/schema#",
    "title": "Personne",
    "type": "object",
    "required": ["nom", "prenom", "age", "date_naissance", "grades"],
    "properties": {
        "nom" :{
            "type": "string"
        },
        "prenom": {
            "type": "string"
        },
        "age": {
            "type": "number"
        },
       "date_naissance": {
            "type": "string",
            "format": "date",
            "pattern": "^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$"
        },
        "grades": {
            "type":"array",
            "items":{
                "type": "string"
            }
        }
    },
    "additionalProperties": False
}

update_personne_schema = {
    "title": "Personne",
    "type": "object",
    "properties": {
        "nom": {
            "type": "string"
        },
        "prenom": {
            "type": "string"
        },
        "age": {
            "type": "number"
        },
        "date_naissance": {
            "type": "string",
            "format": "date",
            "pattern": "^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$"
        },
        "grades": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "additionalProperties": False
}