# 🏥 HealNexus – AI-Powered RAG Chatbot for Healthcare

HealNexus is an intelligent healthcare assistant that leverages **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware responses from medical documents.
It combines **LLMs + Vector Databases + Backend APIs** to deliver reliable healthcare insights.

---

## 🚀 Features

* 🔍 **Semantic Search over Medical Data**
* 🤖 **AI Chatbot with Context Awareness**
* 📄 **Document Ingestion & Chunking**
* 🧠 **Vector Embeddings + Similarity Search**
* 🔐 **Secure Backend with Spring Boot**
* ⚡ **Fast API-based Query Processing**
* 📊 **Scalable Architecture (Production-ready mindset)**

---

## 🏗️ Architecture

```
User Query
   ↓
Backend (Spring Boot / FastAPI)
   ↓
Retriever (Vector DB)
   ↓
Relevant Chunks
   ↓
LLM (Gemini / OpenAI)
   ↓
Final Response
```

---

## 🧰 Tech Stack

### 🔹 Backend

* Java 21
* Spring Boot 3
* Spring Security (JWT)
* REST APIs

### 🔹 AI / RAG Layer

* LangChain
* LangGraph (workflow orchestration)
* Embeddings (OpenAI / Gemini / HuggingFace)
* Vector Database (FAISS / Pinecone / Chroma)

### 🔹 Database

* MySQL (Application Data)
* Vector DB (Semantic Search)

### 🔹 Cloud (Optional / Planned)

* GCP (preferred)
* AWS (basic familiarity)

---

## 📂 Project Structure

```
healnexus-rag-chatbot/
│
├── backend/              # Spring Boot APIs
├── rag/
│   ├── ingestion/        # Document processing
│   ├── retriever/        # Vector search logic
│   ├── embeddings/       # Embedding models
│   └── pipeline/         # RAG workflow
│
├── config/               # Configurations
├── docs/                 # Sample medical docs
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/healnexus-rag-chatbot.git
cd healnexus-rag-chatbot
```

---

### 2️⃣ Backend Setup (Spring Boot)

Update `application.properties`:

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/healnexus
spring.datasource.username=YOUR_USERNAME
spring.datasource.password=YOUR_PASSWORD

spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
```

Run the backend:

```bash
mvn spring-boot:run
```

---

### 3️⃣ RAG Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Ingest Documents

```bash
python -m app.rag.ingestion
```

---

### 5️⃣ Run Chatbot

```bash
python -m app.main
```

---

## 🧪 Example Use Cases

* 🩺 Ask questions from medical reports
* 📑 Retrieve insights from clinical documents
* 💊 Get contextual healthcare explanations
* 🧠 Assist doctors/patients with quick knowledge access

---

## 🔐 Security

* JWT-based authentication
* Role-based access (PATIENT / DOCTOR / ADMIN)
* Secure API endpoints

---

## 📈 Future Enhancements

* ✅ Doctor availability & scheduling
* ✅ Real-time chat UI (React)
* ✅ Multi-document reasoning
* ✅ Audit logging & monitoring
* ✅ Deployment on GCP (Cloud Run / GKE)

---

## 👨‍💻 Author

**Mahammad Alfaz**

* 🔗 GitHub: https://github.com/MahammadAlfaz
* 💼 LinkedIn: https://www.linkedin.com/in/mahammad-alfaz-b27b3225a
* 📧 Email: [alfazkota.786@gmail.com](mailto:alfazkota.786@gmail.com)

---

## ⭐ Contribute

Contributions are welcome!
Feel free to fork, raise issues, or submit PRs.

---

## 📜 License

This project is licensed under the MIT License.

---

## 💡 Inspiration

Built as part of a journey to create **production-grade AI healthcare systems** using modern backend + AI architectures.
