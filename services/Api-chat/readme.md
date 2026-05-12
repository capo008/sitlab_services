
# Chat CLI (Ollama)

A simple Python CLI toolkit to interact with chat models via OpenAI-compatible APIs.

## Prerequisites

- **Python 3.8+**
- **Ollama** installed and running.

## Setup

1. **Clone the repository** (or navigate to the project folder).
2. **Create a virtual environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

## Configuration

You can configure default values using a `.env` file. Copy the example file and edit it:

```powershell
copy .env.example .env
```

Available variables:
- `OLLAMA_MODEL`: Default model name (default: `VladimirGav/gemma4-26b-16GB-VRAM`).
- `OLLAMA_HOST`: Ollama OpenAI-compatible endpoint (e.g., `https://ollama.sitlab.duckdns.org/v1`).

## Usage

### Ollama (`chat_test.py`)

Run the script by providing a prompt:

```powershell
python chat_test.py "Scrivi un breve riassunto della teoria della relativita in 5 punti"
```

### Arguments

| Argument | Description | Default |
| :--- | :--- | :--- |
| `prompt` | **(Required)** User prompt. | N/A |
| `--system` | Optional system instruction. | None |
| `--model` | Ollama model name to use. | `OLLAMA_MODEL` (or `gemma4-26b-iq4`) |
| `--host` | OpenAI-compatible server address. | `OLLAMA_HOST` (or `http://localhost:11434/v1`) |
| `--temperature` | Sampling temperature. | `1.0` |
| `--list-models` | List available models from the server. | N/A |

### Examples

```powershell
# Esempio base
python chat_test.py "Spiega la differenza tra list e tuple in Python"

# Con istruzione di sistema
python chat_test.py "Genera 3 idee per un progetto side" --system "Rispondi in italiano, sintetico e pratico"

# Con modello specifico
python chat_test.py "Traduci in inglese: ci vediamo domani" --model qwen2.5:7b

# Elenco modelli disponibili
python chat_test.py --list-models
```

## Source Code (`chat_test.py`)

```python
# Questo script testa un modello di chat Ollama utilizzando l'API compatibile con OpenAI.
import argparse
import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description="Test Ollama Chat model using OpenAI-compatible API"
    )
    parser.add_argument("prompt", nargs="?", default=None, help="Prompt for the model")
    parser.add_argument(
        "--system",
        default=None,
        help="Optional system prompt to steer the assistant",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("OLLAMA_MODEL", "gemma4-26b-iq4"),
        help="Model name (default: OLLAMA_MODEL env or gemma4-26b-iq4)",
    )
    parser.add_argument(
        "--host",
        default=os.getenv("OLLAMA_HOST", "http://localhost:11434/v1"),
        help=(
            "Ollama OpenAI host address "
            "(default: OLLAMA_HOST env or http://localhost:11434/v1)"
        ),
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=1.0,
        help="Sampling temperature (default: 1.0)",
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available models from the Ollama server and exit",
    )

    args = parser.parse_args()

    try:
        client = OpenAI(
            base_url=args.host,
            api_key="ollama",  # Required but ignored by Ollama
        )

        if args.list_models:
            print(f"Fetching models from {args.host}...")
            models = client.models.list()
            print("\nAvailable models:")
            for model in models.data:
                print(f"- {model.id}")
            sys.exit(0)

        if not args.prompt:
            parser.error("the following arguments are required: prompt (unless --list-models is used)")

        messages = []
        if args.system:
            messages.append({"role": "system", "content": args.system})
        messages.append({"role": "user", "content": args.prompt})

        print(f"Connecting to Ollama (OpenAI API) at {args.host}...")
        print(f"Using model: {args.model}")
        print(f"Prompt: {args.prompt}")
        if args.system:
            print(f"System prompt: {args.system}")
        print("-" * 30)

        response = client.chat.completions.create(
            model=args.model,
            messages=messages,
            temperature=args.temperature,
            stream=False,
        )

        content = response.choices[0].message.content
        if content is None:
            print("No content returned by model.")
            sys.exit(1)

        print("\nResponse:")
        print(content)

    except Exception as error:
        print(f"An error occurred: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

## Troubleshooting

- **Model not found**: Ensure you have pulled the model using `ollama pull <model_name>`.
- **Connection error**: Verify that the Ollama service is running and the `--host` address is correct.
- **Empty response**: Try reducing prompt complexity or switching model.
```

---

### 2. File `.env.example`

Crea un file chiamato `.env.example` nella root del progetto con questo contenuto:

```env
# Default model name (e.g., gemma4-26b-iq4, qwen2.5:7b, etc.)
OLLAMA_MODEL=gemma4-26b-iq4

# Ollama OpenAI-compatible endpoint
OLLAMA_HOST=http://localhost:11434/v1
```
