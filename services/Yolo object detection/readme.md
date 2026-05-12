# Client di Rilevamento Oggetti (`consume-yolo.py`)

Questo script Python è uno strumento professionale per interagire con un'API REST di Object Detection (YOLO). Invia un'immagine all'API, riceve le coordinate degli oggetti rilevati, le stampa in console e genera un'immagine annotata con i rettangoli di selezione (bounding boxes).

## 🚀 Funzionalità

- **Architettura Object-Oriented:** Struttura pulita e manutenibile.
- **Output in Console:** Visualizzazione immediata di classi e confidenza per ogni oggetto rilevato.
- **Logging Professionale:** Tracciamento delle operazioni tramite il modulo `logging`.
- **Parsing Intelligente:** Supporto per molteplici formati di risposta JSON (liste, dizionari nested).
- **Annotazione Avanzata:** Disegno di box e testi con background contrastante.
- **Export Dati:** Opzione per salvare i risultati delle rilevazioni in un file JSON.
- **Parametrizzazione .env:** Configurazione flessibile tramite variabili d'ambiente.

## 📋 Prerequisiti

Assicurati di avere Python installato. Installa tutte le dipendenze necessarie tramite il file `requirements.txt`:

```bash
pip install -r requirements.txt
```

## ⚙️ Configurazione

Crea un file `.env` partendo dall'esempio fornito sotto.

### .env.example
```env
# URL dell'API di Object Detection
DETECTION_API_URL=https://cv.sitai.duckdns.org/v2/object-detection/yolo

# Percorso predefinito per l'immagine di output
DETECTION_OUTPUT_PATH=output_image.jpg

# Abilita il logging dettagliato (True/False)
DETECTION_VERBOSE=False
```

## 🛠️ Utilizzo

Il comando base richiede il percorso dell'immagine:

```bash
python consume-yolo.py nome_immagine.jpg
```

### Esempi Avanzati

**Esportare i risultati in JSON:**
```bash
python consume-yolo.py test.jpg --json risultati.json
```

**Endpoint personalizzato e Debug mode:**
```bash
python consume-yolo.py test.jpg --api http://127.0.0.1:5001/v2/object-detection/yolo --verbose
```

## ⚙️ Opzioni della riga di comando

| Parametro | Descrizione | Valore Predefinito |
| :--- | :--- | :--- |
| `image_path` | **Obbligatorio:** Percorso del file immagine. | N/D |
| `--api` | L'URL completo dell'API REST. | Dal file .env |
| `--output` | Nome del file di output annotato. | Dal file .env |
| `--json` | Percorso del file JSON per salvare i dati rilevati. | N/D |
| `--verbose` | Abilita i log di debug dettagliati. | Dal file .env |

---

## 📄 Sorgente Completo (`consume-yolo.py`)

```python
import os
import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

import requests
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

class ObjectDetectionClient:
    """Client per interagire con API di Object Detection."""

    def __init__(self, api_url: str):
        self.api_url = api_url
        self.session = requests.Session()

    def _standardize_detections(self, raw_data: Any) -> List[Dict[str, Any]]:
        if isinstance(raw_data, str):
            try: raw_data = json.loads(raw_data)
            except json.JSONDecodeError: return []

        detections_list = []
        if isinstance(raw_data, list):
            detections_list = raw_data
        elif isinstance(raw_data, dict):
            for key in ['detections', 'results', 'objects', 'predictions']:
                if key in raw_data and isinstance(raw_data[key], list):
                    detections_list = raw_data[key]
                    break
        
        standardized = []
        for det in detections_list:
            if not isinstance(det, dict): continue
            try:
                bbox = {
                    'xmin': float(det.get('xmin', 0)),
                    'ymin': float(det.get('ymin', 0)),
                    'xmax': float(det.get('xmax', 0)),
                    'ymax': float(det.get('ymax', 0))
                }
                standardized.append({
                    'class_name': det.get('name', det.get('class_name', 'unknown')),
                    'confidence': float(det.get('confidence', 0)),
                    'bbox': bbox
                })
            except (ValueError, TypeError): continue
        return standardized

    def detect(self, image_path: Path) -> List[Dict[str, Any]]:
        logger.info(f"Invio immagine all'API: {image_path.name}")
        try:
            with open(image_path, 'rb') as img_file:
                files = {'image': (image_path.name, img_file, 'image/jpeg')}
                response = self.session.post(self.api_url, files=files)
                response.raise_for_status()
                raw_data = response.json()
                detections = self._standardize_detections(raw_data)
                logger.info(f"API ha restituito {len(detections)} oggetti rilevati.")
                return detections
        except Exception as e:
            logger.error(f"Errore durante il rilevamento: {e}")
            raise

class ImageAnnotator:
    @staticmethod
    def _get_font(size: int = 20):
        font_paths = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "arial.ttf"]
        for path in font_paths:
            try: return ImageFont.truetype(path, size)
            except: continue
        return ImageFont.load_default()

    @classmethod
    def draw_detections(cls, input_path: Path, detections: List[Dict[str, Any]], output_path: Path):
        try:
            with Image.open(input_path) as img:
                draw = ImageDraw.Draw(img)
                font = cls._get_font(20)
                for det in detections:
                    bbox = det['bbox']
                    label = f"{det['class_name']} {det['confidence']:.2f}"
                    box = [bbox['xmin'], bbox['ymin'], bbox['xmax'], bbox['ymax']]
                    draw.rectangle(box, outline='red', width=3)
                    txt_bbox = draw.textbbox((bbox['xmin'], bbox['ymin']), label, font=font)
                    padded_txt_bbox = [txt_bbox[0], txt_bbox[1] - 4, txt_bbox[2] + 4, txt_bbox[3]]
                    draw.rectangle(padded_txt_bbox, fill='red')
                    draw.text((bbox['xmin'] + 2, bbox['ymin'] - 2), label, fill='white', font=font)
                img.save(output_path)
                logger.info(f"Immagine salvata in: {output_path}")
        except Exception as e:
            logger.error(f"Errore annotazione: {e}")
            raise

def main():
    env_api = os.getenv('DETECTION_API_URL', 'http://localhost:7000/api/v1/object-detection')
    env_output = os.getenv('DETECTION_OUTPUT_PATH', 'output_image.jpg')
    env_verbose = os.getenv('DETECTION_VERBOSE', 'False').lower() in ('true', '1', 't')

    parser = argparse.ArgumentParser(description='Client YOLO REST API')
    parser.add_argument('image_path', type=str, help='Immagine input')
    parser.add_argument('--api', default=env_api, help='URL API')
    parser.add_argument('--output', default=env_output, help='Immagine output')
    parser.add_argument('--json', help='Percorso file JSON per i risultati')
    parser.add_argument('--verbose', action='store_true', default=env_verbose, help='Debug logging')

    args = parser.parse_args()
    if args.verbose: logger.setLevel(logging.DEBUG)

    input_path = Path(args.image_path)
    output_path = Path(args.output)
    json_path = Path(args.json) if args.json else None

    if not input_path.exists():
        logger.error(f"File non trovato: {input_path}")
        sys.exit(1)

    try:
        client = ObjectDetectionClient(args.api)
        detections = client.detect(input_path)
        
        if detections:
            print("\n" + "="*30)
            print(f" OGGETTI RILEVATI IN {input_path.name}")
            print("="*30)
            for i, det in enumerate(detections, 1):
                bbox = det['bbox']
                print(f"{i}. {det['class_name']} ({det['confidence']:.2%})")
                print(f"   Coords: xmin={bbox['xmin']:.0f}, ymin={bbox['ymin']:.0f}, xmax={bbox['xmax']:.0f}, ymax={bbox['ymax']:.0f}")
            print("="*30 + "\n")

        if json_path and detections:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(detections, f, indent=4)
            logger.info(f"Dati esportati in: {json_path}")

        if detections:
            ImageAnnotator.draw_detections(input_path, detections, output_path)
        else:
            logger.warning("Nessun oggetto trovato.")
    except Exception: sys.exit(1)

if __name__ == '__main__':
    main()
```
