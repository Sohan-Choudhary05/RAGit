# RAGit – Open-Source RAG on GitHub Repos

RAGit is an end-to-end Generative AI project that enables users to query any GitHub repository using Retrieval-Augmented Generation (RAG). It can answer questions about code, generate summaries.

## 🛠️ Technology Stack

This project uses:
* **LangChain** for orchestration
* **FAISS** for vector storage
* **Ollama Mistral** as the LLM
* **Flask** as the backend API

## 🚀 Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/ragit.git
   cd ragit
   ```

2. **Create virtual environment & install dependencies**
   ```bash
   conda create -n ragit_env python=3.11
   conda activate ragit_env
   pip install -r requirements.txt
   ```

3. **Run the Flask server**
   ```bash
   python run.py
   ```

   The server will start at:
   ```
   http://127.0.0.1:5000
   ```

## 📬 API Usage with Postman

### 1. Import Repo & Build Knowledge Base

**POST** `http://127.0.0.1:5000/api/process_repo`

**Body (JSON):**
```json
{
  "repo_url": "https://github.com/openai/gym"
}
```

**✅ Response:**
```json
{
  "message": "Repo processed and embedded successfully"
}
```

### 2. Ask Questions about the Repo

**POST** `http://127.0.0.1:5000/ask`

**Body (JSON):**
```json
{
  "question": "What does the main.py file do?"
}
```

**✅ Response:**
```json
{
  "answer": "The main.py file initializes the environment..."
}
```
## 🚀 Features

- **Repository Indexing**: Automatically clone and index any public GitHub repository
- **Intelligent Querying**: Ask questions about code structure, functionality, and implementation
- **README Generation**: Auto-generate comprehensive README files for repositories
- **Vector Search**: Fast and accurate code retrieval using FAISS/Chroma vector databases
- **RESTful API**: Easy integration with web applications and services

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
