insert_demande_schema = {
    "title": "Demande",
    "type": "object",
    "required": ["nom_etablissement", "adresse",
                 "ville", "date_visite", "nom", "prenom",
                 "description_probleme"],
    "properties": {
        "nom_etablissement": {
            "type": "string",
            "minLength": 1
        },
        "adresse": {
            "type": "string",
            "minLength": 1
        },
        "ville": {
            "type": "string",
            "minLength": 1
        },
        "date_visite": {
            "type": "string",
            "format": "date",
            "pattern": r"^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$"
        },
        "nom": {
            "type": "string",
            "minLength": 1
        },
        "prenom": {
            "type": "string",
            "minLength": 1
        },
        "description_probleme": {
            "type": "string",
            "minLength": 1
        }
    },
    "additionalProperties": False
}

insert_user_schema = {
    "title": "Utilisateur",
    "type": "object",
    "required": ["nom_complet", "email", "etablissements", "password"],
    "properties": {
        "nom_complet": {
            "type": "string",
            "minLength": 1
        },
        "email": {
            "type": "string",
            "format": "email",
            "pattern": "^\\S+@\\S+\\.\\S+$"
        },
        "etablissements": {
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 1
            }
        },
        "password": {
            "type": "string",
            "minLength": 6
        }
    }
}

update_etab_user_schema = {
    "title": "Etablissement Utilisateur",
    "type": "object",
    "required": ["etablissements"],
    "properties": {
        "etablissements": {
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 1
            }
        }
    }
}
