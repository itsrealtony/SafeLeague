import chardet
import json

def detect_and_fix_encoding(file_path):
    # Rileva l'encoding attuale
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        detected_encoding = result['encoding']
        confidence = result['confidence']

    print(f"Encoding rilevato: {detected_encoding} (confidenza: {confidence:.2f})")

    # Leggi con l'encoding rilevato e salva in UTF-8
    try:
        with open(file_path, 'r', encoding=detected_encoding) as file:
            data = json.load(file)

        # Salva il file in UTF-8 (corretto)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

        print(f"File convertito con successo da {detected_encoding} a UTF-8")

    except Exception as e:
        print(f"Errore durante la conversione: {e}")
        # Prova con encoding comuni per dati italiani
        for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    data = json.load(file)

                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=2, ensure_ascii=False)

                print(f"File convertito con successo da {encoding} a UTF-8")
                break
            except:
                continue

# Esegui la correzione
detect_and_fix_encoding('dati_calcio.json')