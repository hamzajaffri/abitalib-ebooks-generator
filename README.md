# ABITALIB E-Books Generator™

ABITALIB E-Books Generator is a modular, production-ready local AI writing stack that generates multi-chapter books using **local GGUF models** (llama.cpp), then exports final artifacts as **PDF** and **EPUB**.

It is designed for MVP SaaS prototyping without paid APIs and can run locally or in Google Colab.

## Features

- Local-only text generation with GGUF models (`llama-cpp-python`)
- Hardware detection (CPU, RAM, GPU/VRAM)
- Structured book generation input:
  - title
  - author
  - genre
  - language
  - chapter count
- Smart chapter memory with rolling summaries for continuity
- Automatic table of contents creation
- PDF and EPUB export
- ISBN-13 sample barcode generation
- Publishing license document generation
- Gradio web UI
- Works with local filesystem or mounted Google Drive in Colab

## Project Structure

```text
abitalib-ebooks-generator/
├── README.md
├── requirements.txt
├── run_colab.ipynb
├── config.py
├── hardware.py
├── model_loader.py
├── memory_system.py
├── book_engine.py
├── toc.py
├── metadata.py
├── isbn.py
├── license.py
├── pdf_engine.py
├── epub_engine.py
└── ui.py
```

## Installation

### 1) Clone

```bash
git clone https://github.com/<your-username>/abitalib-ebooks-generator.git
cd abitalib-ebooks-generator
```

### 2) Create environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

## Upload / Provide a Local GGUF Model

You can either:

1. Copy your GGUF file into `./models/` (recommended), e.g.:
   - `models/mistral-7b-instruct.Q4_K_M.gguf`
2. Or keep it anywhere and paste full path in the UI **GGUF Model Path** box.

Then click **Load Model** in the Model tab.

## Run Locally

```bash
python ui.py
```

Open the URL shown by Gradio (default `http://127.0.0.1:7860`).

### Local usage flow

1. Open **System** tab to inspect hardware detection.
2. Open **Model** tab and load a GGUF model path.
3. Open **Generate Book** tab and set title, author, genre, language, chapter count.
4. Click **Generate Book + PDF + EPUB**.
5. Collect output files from your selected output directory.

## Run in Google Colab

Use the included notebook: `run_colab.ipynb`.

It includes:

- repository clone
- dependency install
- optional Google Drive mount
- model upload instructions
- UI launch command

### Colab quick steps

1. Open `run_colab.ipynb` in Colab.
2. Run setup cells.
3. Upload your GGUF model (either to runtime filesystem or Drive).
4. Run `python ui.py` cell.
5. Use the generated public Gradio link.

## Usage Examples

### Example: launch app

```bash
python ui.py
```

### Example: set custom output directory in UI

Set `Output Directory` to:

```text
/content/drive/MyDrive/abitalib_outputs
```

(Useful in Google Colab when Drive is mounted.)

## Notes

- If no model is loaded, the engine still generates fallback draft chapters.
- For best quality and speed, use quantized instruction-tuned GGUF models.
- Ensure sufficient RAM/VRAM for your selected model size.

## License

Use and modify for your own projects. Validate legal/publishing requirements before commercial distribution.
