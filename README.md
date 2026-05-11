# 🚀 AI-Native E-commerce Engine & Agentic QA Framework

An advanced e-commerce data pipeline integrated with Local AI models for sentiment analysis, semantic search, and an automated QA auditing agent.

## ✨ Key Features
- **Big Data Simulation:** 200,000+ orders generated and managed via **Dockerized PostgreSQL**.
- **Local Sentiment AI:** Analyzed 1,000+ customer reviews using a fine-tuned **Transformers** model.
- **Semantic Search:** Vector-based product search using **FAISS** and **Sentence Transformers**.
- **Agentic QA:** An automated auditing agent powered by **Ollama (Llama 3)** that validates search results.

## 🛠️ Tech Stack
- **Database:** PostgreSQL, Docker
- **AI/ML:** HuggingFace Transformers, FAISS, Sentence-Transformers
- **Agentic Framework:** LangChain, Ollama (Llama 3)
- **Language:** Python 3.14

## 📊 Sample QA Audit Report (Ollama)
> **Query:** "Summer casual outfits"  
> **Verdict:** `[FAIL]`  
> **Reason:** System returned formal attire instead of casual wear. 
> *The AI Agent identified this contextual gap, proving the robustness of the QA framework.*

## 🚀 How to Run
1. Clone the repo.
2. Set up a virtual environment: `python -m venv venv`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run `docker-compose up -d` to start the DB.
5. Generate the vector database: `python create_vector_db.py`.
6. Run the QA Auditor: `python ai_qa_agent.py`.
