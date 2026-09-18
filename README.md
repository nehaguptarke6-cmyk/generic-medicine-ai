# 💊 Generic Medicine AI

A beginner-friendly **RAG (Retrieval-Augmented Generation)** application built with Python and Streamlit.

Generic Medicine AI allows users to ask questions about medicines available in its knowledge base. The application retrieves relevant medicine information using semantic search and uses a local Qwen language model to generate a simple response.

> **Disclaimer:** This application is for general educational information only. It does not diagnose medical conditions, prescribe medicines, or replace advice from a qualified healthcare professional.

---

## 🎯 Project Objective

The main objective of this project is to build a simple AI-powered medicine information assistant while learning:

* RAG
* Vector databases
* Semantic search
* Hugging Face models
* LangChain
* Streamlit
* Git and GitHub

---

## ✨ Features

* 💬 Chat-based Streamlit interface
* 🔎 Semantic search using FAISS
* 📚 Retrieval-Augmented Generation
* 🤗 Hugging Face embeddings
* 🤖 Local Qwen language model
* 📄 CSV-based medicine knowledge base
* 🛡️ Basic dosage-question safety handling
* 🚫 Avoids generating dosage instructions
* 📖 View retrieved information
* 🗑️ Clear chat option
* ❌ Avoids displaying missing values such as `NaN`

---

## 🏗️ Architecture

```text
User Question
      ↓
Streamlit App
      ↓
Medicine CSV Dataset
      ↓
Document Creation
      ↓
Text Splitting
      ↓
Hugging Face Embeddings
      ↓
FAISS Vector Store
      ↓
Relevant Documents
      ↓
RAG Prompt
      ↓
Qwen LLM
      ↓
Final Response
```

---

## 🛠️ Tech Stack

| Technology            | Purpose                    |
| --------------------- | -------------------------- |
| Python                | Application development    |
| Streamlit             | User interface             |
| Pandas                | Dataset handling           |
| LangChain             | RAG workflow               |
| FAISS                 | Vector similarity search   |
| Hugging Face          | Embeddings and model tools |
| Sentence Transformers | Text embeddings            |
| Qwen                  | Local language model       |
| openFDA               | Medicine label data        |

---

## 📁 Project Structure

```text
generic-medicine-ai/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── medicines.csv
│   └── real_medicines.csv
│
└── src/
    ├── __init__.py
    ├── data_loader.py
    ├── fetch_medicines.py
    ├── llm.py
    ├── prompts.py
    ├── rag.py
    ├── safety.py
    └── search.py
```

---

## 🔄 How the Application Works

### 1. Load Data

Medicine information is loaded from the CSV dataset using Pandas.

### 2. Create Documents

Medicine records are converted into LangChain documents.

### 3. Split Documents

The documents are divided into smaller chunks for retrieval.

### 4. Create Embeddings

The application uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

to create text embeddings.

### 5. FAISS Search

FAISS performs semantic similarity search to find relevant medicine information.

### 6. Generate Response

The retrieved information is provided as context to:

```text
Qwen/Qwen2.5-0.5B-Instruct
```

The model generates a response based on the retrieved context.

### 7. Safety Handling

The application contains a separate safety check for dosage-related questions and does not generate dosage instructions.

---

## 💬 Example Questions

```text
What is acetaminophen?
```

```text
What is ibuprofen?
```

```text
What information is available about amoxicillin?
```

For information that is not present in the knowledge base, the application is designed to avoid inventing information.

---

## 🚀 How to Run Locally

### Step 1: Clone the repository

```bash
git clone https://github.com/nehaguptarke6-cmyk/generic-medicine-ai.git
```

### Step 2: Open the project

```bash
cd generic-medicine-ai
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

### Step 4: Activate the environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the application

```bash
streamlit run app.py
```

The Streamlit application will open in the browser.

---

## 📊 Data

The project contains a medicine knowledge base in CSV format.

The `real_medicines.csv` dataset was created using medicine labeling information from **openFDA**.

The application uses the information available in its local knowledge base for retrieval and response generation.

---

## 🛡️ Safety and Limitations

This is a **learning project**, not a medical decision-making tool.

The application:

* Does not diagnose medical conditions.
* Does not prescribe medicines.
* Does not provide dosage instructions.
* Does not replace professional medical advice.
* May have incomplete information because the knowledge base is limited.
* May produce imperfect AI-generated responses.

Information should be verified using appropriate official sources or a qualified healthcare professional when needed.

---

## 🚧 Future Improvements

Possible future improvements include:

* Expand the medicine dataset.
* Improve medicine-name matching.
* Add source references to retrieved information.
* Improve response validation.
* Add more structured medicine information.
* Improve the Streamlit interface.

---

## 👩‍💻 Author

**Neha Bansal**

### Learning Focus

This project was created as a hands-on learning project to understand:

**Python → LangChain → RAG → FAISS → Hugging Face → LLMs → Streamlit → GitHub**
