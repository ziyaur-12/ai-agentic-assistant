# AI Agentic Assistant

Starter project structure for a modular AI assistant with agents, RAG, tools, memory, schemas, and a Streamlit frontend.

## Structure

- `app/`: backend assistant package
- `frontend/streamlit_app.py`: UI entrypoint
- `tests/`: automated tests
- `data/uploaded_docs/`: uploaded source documents
- `vectordb/`: local vector store data

## Run

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run the app with `python app/main.py`.
4. Launch the UI with `streamlit run frontend/streamlit_app.py`.
