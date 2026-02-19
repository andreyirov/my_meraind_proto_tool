# AI Diagram Generator Web Service

This is a web service that allows users to generate and edit Mermaid.js diagrams (Sequence and Flowchart) using an LLM.

## Prerequisites

- Python 3.8+
- An OpenAI-compatible API key (e.g., DeepSeek, OpenAI) in the `.env` file at the project root.

## Setup

1. Navigate to the backend directory:
   ```bash
   cd web_service/backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure your `.env` file in the root directory has the following variables:
   ```
   API_KEY=your_api_key
   BASE_URL=your_base_url
   MODEL=deepseek-chat
   ```

## Running the Service

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## Features

- **Diagram Types**: Sequence Diagram, Flowchart (Block).
- **Interactive Editing**: Describe changes in natural language to update the diagram.
- **History**: Undo and Redo functionality.
- **Save**: Download the diagram code as a `.mmd` file.
