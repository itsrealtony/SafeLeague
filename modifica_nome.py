import json


def fix_app_name(file_path):
    # Leggi il file JSON
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Sostituisci tutti i riferimenti da "transfermarkt" a "SafeLeague"
    for item in data:
        if 'model' in item:
            item['model'] = item['model'].replace('SafeLeague.', 'league.')

    # Salva il file corretto
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print("Nomi dei modelli corretti da 'transfermarkt' a 'SafeLeague'")


# Esegui la correzione
fix_app_name('dati_calcio.json')