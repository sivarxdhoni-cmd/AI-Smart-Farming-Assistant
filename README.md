# AI-Driven Smart Farming Assistant – RAG Vector Database

This project implements the **Weeks 3–4 Agricultural Knowledge Base & RAG Integration** foundation from the supplied project document.

## What this implementation does

1. Reads agricultural knowledge documents (`.txt`, `.md`, `.pdf`, `.docx`).
2. Splits documents into overlapping chunks using LangChain's recursive text splitter.
3. Loads a multilingual Sentence Transformers embedding model.
4. Generates vector embeddings for each agricultural text chunk.
5. Stores embeddings and source metadata in a persistent ChromaDB collection.
6. Embeds a farmer's query and retrieves semantically similar passages.
7. Prints source document and relevance score for every retrieved passage.

## Technology selection based on the project document

- **Vector database:** ChromaDB (one of the project's explicitly proposed options: ChromaDB / Pinecone).
- **RAG orchestration and chunking:** LangChain.
- **Embedding model:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.
- **Vector size:** 384 dimensions.
- **Vector metric:** cosine similarity.
- **Persistence:** local `chroma_db/` directory.
- **Document inputs:** ICAR material, Kisan Call Centre FAQs, government agriculture scheme material, crop guidance and verified agricultural manuals.

The selected embedding model is multilingual and is a practical prototype baseline for English and Indic-language semantic retrieval. Validate retrieval quality separately for Hindi and Kannada using a representative evaluation set before production. The project's Sarvam AI STT/TTS and translation services are separate components; they are not required to complete this vector database task.

## Setup in VS Code (Windows)

Install Python 3.10+ (Python 3.11 recommended). Open this folder in VS Code, then Terminal → New Terminal:

```powershell
py -3.11 -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\\Scripts\\Activate.ps1
```

## Add agriculture documents

Put verified source documents in:

`data/agriculture_knowledge/`

Supported formats: TXT, Markdown, text-based PDF, DOCX. Scanned PDFs require OCR before ingestion.

Two demo documents are included to test the pipeline. They are illustrative starter content, **not official ICAR recommendations or a substitute for local agricultural expert advice**. For project evaluation, add curated documents from ICAR, Kisan Call Centre FAQs and official government scheme portals, preserving source titles and versions.

## Run the required task

### 1. Create embeddings and store in ChromaDB

```powershell
python main.py ingest
```

### 2. Test semantic search

```powershell
python main.py test
```

### 3. Ask your own question

```powershell
python main.py search
```

Try a Hindi or Kannada query after ingestion to make an initial multilingual retrieval check. Model quality must be measured with a proper set of questions and expected source passages; one successful query is only a smoke test.

## Expected output

First run downloads the model, then prints a successful ingestion summary including number of source documents, chunks, vectors in ChromaDB and the persistent database path. The test command should return relevant agriculture passages with source names and relevance scores and print `TEST PASSED`.

Exact scores and chunk counts can vary by library/model version and document length.

## Folder structure

```text
Smart_Farming_RAG_VectorDB/
├── data/
│   └── agriculture_knowledge/
│       ├── crop_health_and_pest_monitoring.md
│       └── soil_and_water_management.md
├── chroma_db/                 # created automatically
├── .env.example
├── .gitignore
├── requirements.txt
├── config.py
├── embeddings.py
├── document_loader.py
├── chunking.py
├── vector_store.py
├── ingest.py
├── search.py
├── main.py
└── README.md
```

## Scope and limitations

This completes the vector database and retrieval setup, not the full conversational RAG system. The next stage connects retrieved passages to the LLM, enforces answer grounding and source citations, routes queries to crop advisory / pest control / schemes / mandi-price agents, and integrates live AGMARKNET, weather and scheme APIs. Real-time prices and weather must come from their APIs, not stale vector documents.

For farmer-facing deployment, add language detection/translation, Sarvam AI speech services, query evaluation, low-confidence escalation to agricultural extension workers, privacy controls and API security. Do not present generated pesticide dosages, chemical recommendations or scheme eligibility as authoritative without verified sources and appropriate expert/official confirmation.
