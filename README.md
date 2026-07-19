# Smart Research Assistant

# Live Demonstration

| Resource | Link |
|---------|------|
| Live Application | https://celebalproject-mnudbuco5ysnjvp6mqc9xt.streamlit.app/ |


---


## 1. Introduction
**Smart Research Assistant is an Advanced Retrieval-Augmented Generation (RAG) system designed for intelligent document understanding, semantic knowledge retrieval, and grounded response generation. The system combines semantic search, multi-query retrieval, persistent vector storage, confidence scoring, conversational memory, and an evaluation framework to provide accurate and explainable responses from large document collections while preventing hallucinations through grounded refusals.**

## 2. Why Smart Research Assistant?
Traditional document chatbots often suffer from hallucinations, lack of transparency, and poor handling of complex, multi-turn queries. Smart Research Assistant addresses these gaps by prioritizing reliability, explainability, and modular software engineering. It is built not just to answer questions, but to provide verifiable, contextually grounded insights with measurable confidence levels.

## 3. Key Features
- Advanced Retrieval-Augmented Generation (RAG).
- Semantic Document Understanding.
- Persistent ChromaDB Knowledge Base.
- Multi-Query Retrieval.
- Multi-Turn Conversations.
- Confidence Scoring Mechanism.
- Dynamic Evaluation Framework.
- Grounded Refusal Generation.
- Graceful Failure Handling.
- Session Analytics.
- Semantic Search.
- Modular Architecture.
- Lightweight Deployment.
- Streamlit-Based Interactive Interface.

## 4. System Architecture Diagram
<img width="335" height="841" alt="image" src="https://github.com/user-attachments/assets/a2a82ca6-d141-4b45-8bdc-1cb9e4fc09ef" />

## 5. RAG PIPELINE SEQUENCE DIAGRAM
<img width="1371" height="885" alt="image" src="https://github.com/user-attachments/assets/230a7c0f-47bc-494f-aaad-1c474f93ece8" />

## 6.Project Structure

```text
Smart-Research-Assistant/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
├── core/
│   ├── loader.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── prompts.py
│   ├── llm.py
│   ├── ingestion.py
│   ├── memory.py
│   └── pipeline.py
├── evaluation/
│   ├── confidence.py
│   ├── ragas_metrics.py
│   └── response_metrics.py
├── uploads/
└── database/
```

## 7. Installation Guide
Follow these sequential steps to set up and run the advanced RAG pipeline locally on your machine.

### 1. Clone the Repository
```bash
git clone https://github.com
cd CelebalProject
```

### 2. Create a Virtual Environment
```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment
* **On macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```
* **On Windows:**
  ```bash
  venv\Scripts\activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file in the project root directory and add your private Groq API key:
```text
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
```

### 6. Run the Application
Launch the Streamlit web dashboard interface:
```bash
streamlit run app.py
```

## 8. Technologies Used

*   **Frontend**: Streamlit
*   **Orchestration**: LangChain, LangChain Community, LangChain Core
*   **Vector Database**: ChromaDB
*   **Embeddings**: Sentence Transformers (`all-MiniLM-L6-v2`)
*   **LLM Provider**: Groq (`llama-3.3-70b-versatile`)
*   **Evaluation**: Custom LLM-as-a-Judge Metrics (Faithfulness, Answer Relevance, Context Precision)
*   **Document Processing**: PyPDF, Python-Docx
*   **Environment**: Python 3.11, PyTorch (CPU-optimized)

## 9.Design Decisions

The project was intentionally designed around a modular architecture to maximize maintainability, scalability, and component-level extensibility.

Major engineering decisions include:

- Persistent vector storage using ChromaDB.
- Semantic retrieval using Sentence Transformers embeddings.
- Modular separation of ingestion, retrieval, generation, and evaluation layers.
- Grounded refusal handling to minimize hallucinations.
- Confidence scoring based on retrieval quality, source quality, response quality, and evaluation metrics.
- Conversation history support for multi-turn interactions.
- Lightweight Streamlit deployment suitable for cloud hosting.
- LLM-as-a-Judge based response evaluation for measuring faithfulness, answer relevance, and contextual precision.


## 10.Future Improvements

*   **Hybrid Search**: Integrate BM25 sparse retrieval alongside dense vector embeddings to optimize specific keyword matching.
*   **Expanded Data Ingestion**: Support scanned image PDFs via optical character recognition (OCR) parsing engines and audio file transcripts.
*   **Asynchronous Pipelines**: Transition the data extraction workflows to an async background worker loop to ingest large enterprise document repositories without slowing down the user interface.
*   **Role-Based Access Control (RBAC)**: Implement secure multi-user tenant authentication and file permission levels for compliant enterprise deployments.

## 11.App Screenshots

---

## 1. Smart Research Assistant - Home Interface

The landing page of the application displaying the active knowledge base, document statistics, project stack, and the question answering interface.

<img width="1710" height="952" alt="Screenshot 2026-07-19 at 8 24 04 PM" src="https://github.com/user-attachments/assets/22fc0c00-1885-4997-9faa-68ddc7fefb3d" />

---
## 2. Response Generation using RAG Pipeline

The Research Assistant generates grounded responses by combining semantic retrieval with LLM-based reasoning. Responses are generated strictly from the retrieved contextual information.

<p align="center">
<img width="1705" height="933" alt="Screenshot 2026-07-19 at 8 24 53 PM" src="https://github.com/user-attachments/assets/9c44a146-abe1-4af8-a80c-1943d521d89a" />
</p>

---

## 3. Evaluation Dashboard

The Evaluation Dashboard provides comprehensive response quality assessment using multiple metrics including confidence scoring, retrieval quality, source quality, response quality, and RAGAS-inspired evaluation metrics.

### Metrics Included

- Confidence Score
- Confidence Level
- Retrieval Quality
- Response Quality
- Source Quality
- Faithfulness Score
- Answer Relevance Score
- Context Precision Score

<p align="center">
<img width="1171" height="739" alt="Screenshot 2026-07-19 at 8 25 03 PM" src="https://github.com/user-attachments/assets/41c2fb60-509b-4461-93a6-d0d972284d53" />
</p>

---




