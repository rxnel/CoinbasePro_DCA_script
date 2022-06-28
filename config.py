import json

config = {
    "cbpro_api_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "cbpro_secret": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "cbpro_passphrase": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
}

with open("config1.json", "w") as f:
    json.dump(config, f)
