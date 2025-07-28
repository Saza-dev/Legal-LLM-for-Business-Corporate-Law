# 🧑‍⚖️ Legal Assistant for Sri Lankan Business & Corporate Law

A Streamlit-based AI Legal Assistant that helps answer questions, draft documents, check legal compliance, and summarize contracts or policies based on Sri Lankan Business and Corporate Law.

---

## 🚀 Features

### 🧠 Assistant
Ask free-form legal questions and get answers backed by case law and legal documents.

### 📝 Drafter
Automatically draft legal/business documents using intelligent prompts and domain-specific knowledge.

### ✅ Compliance Checker
Upload a PDF document and receive feedback on missing clauses or legal non-compliance.

### 📄 Summarizer
Upload large legal documents (e.g., contracts, policies) and get a clean, structured summary.

---

## 🧱 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **LLM**: [GROQ + LLaMA3-70B](https://groq.com/)
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Vector DB**: [ChromaDB](https://www.trychroma.com/)
- **RAG Pipeline**: [LangChain](https://www.langchain.com/)
- **PDF Processing**: PyPDFLoader (LangChain)
- **Document Drafting**: python-docx

---

## 📂 Project Structure

```
legal-assistant/
├── app.py                  # Main Streamlit launcher
├── chains/                 # Chains for Assistant, Drafter, Checker, Summarizer
├── components/             # Session management
├── config/                 # LLM, Embeddings, Retriever setup
├── utils/                  # Prompts, PDF utilities
├── chroma_legal_db/        # Persisted vectorstore (auto-created)
├── requirements.txt
└── .env                    # Contains environment variables
```

---

## ⚙️ Setup Instructions

1. **Clone the repo**
```bash
git clone https://github.com/your-username/legal-assistant.git
cd legal-assistant
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the root with:
```
GROQ_API_KEY=your_groq_api_key_here
HUGGINGFACEHUB_API_TOKEN=your_hugging_face_api_key_here
```

5. **Run the app**
```bash
streamlit run app.py
```

---

## 📘 Notes

- This assistant is trained specifically on **Sri Lankan business & corporate law** data.
- If you want to extend its capabilities, you can load additional PDFs into ChromaDB manually.

---

## 📜 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Pull requests and feedback are welcome! Open an issue to discuss improvements or bugs.
