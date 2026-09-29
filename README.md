# 🧠 LifeSync AI: Holistic Mental & Financial Assistant for Students

**LifeSync AI** is an intelligent, AI-powered assistant application designed to help vocational and high school students navigate and manage the two most critical pillars of student life: **Financial Health (Pocket Care)** and **Mental Well-being (Mind Care)**.

This innovation project seamlessly integrates a highly responsive web interface with high-speed Large Language Models (LLMs) powered by the cutting-edge **Groq API Cloud** infrastructure.

## 🌟 Problem Statement & Background
Research shows that the majority of students experience high levels of stress stemming from two primary sources: **academic pressure** and **financial anxiety (running out of monthly allowance)**. Unfortunately, students often abandon rigid, mainstream tracking apps because they feel mechanical and tedious.

**LifeSync AI bridges this gap.** By combining an empathetic conversational companion with an intuitive expense ledger, this platform helps students maintain a healthy balance between their mind and their wallet—all within a secure, locally-encrypted system.

## 🚀 Key Features

### 💰 1. Financial Assistant (Pocket Care)
* **Allowance Tracking:** Dynamically input your initial monthly allowance or income.
* **Instant Expense Ledger:** Log daily expenses smoothly with automatic, real-time balance deductions.
* **AI Financial Planner:** Consult an interactive AI advisor that analyzes your actual spending history to generate tailored, realistic budgeting strategies.

### 🌱 2. Psychological Consultant (Mind Care - Interactive Chat)
* **Polished Web Chat Interface:** An immersive chat room layout where users can comfortably share their thoughts.
* **Emotional Counselor:** The AI acts as a compassionate student counselor that validates emotions, analyzes stress indicators, provides warm motivation, and delivers 3 practical, actionable anxiety-relief steps.

### 📊 3. Central Download Hub (Export System)
* **Local Spreadsheet Auto-Save:** Every single financial transaction and counseling chat log is automatically saved into local files.
* **Official Document Export:** Users can download comprehensive financial summaries in **Excel (.xlsx)** format or export their mental health journals into official **Microsoft Word (.docx)** files.

## 🛠️ Technical Architecture & Stack
* **Programming Language:** Python 3.9+
* **Frontend Framework:** Streamlit
* **AI & Inference Engine:** Groq Cloud SDK (`gpt-oss-20b`)
* **Data Processing & File Export:** Pandas, OpenPyXL, Python-Docx
* **Secure Environment Management:** Python-Dotenv

## 💻 Local Installation Guide

Follow these sequential steps to set up and run LifeSync AI on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com
cd lifesync_ai
```

### 2. Install Dependencies
Make sure you have your virtual environment activated, then install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Configure the Environment Variables (`.env`)
Create a new file named `.env` in the root directory of your project. Insert your active Groq API Key as follows:
```text
GROQ_API_KEY=your_secret_groq_api_key_here
```

### 4. Launch the Application
Execute the following command in your terminal to fire up the Streamlit server:
```bash
streamlit run app.py
```

## 🔒 Security, Privacy, & Best Practices
1. **Local-First Storage:** All financial ledgers and personal mental health journals are strictly saved inside local Excel databases on your own device, ensuring no external public cloud servers can scrape your data.
2. **Secure Key Management:** The backend leverages `python-dotenv` to fetch credentials from a hidden `.env` file. This file is explicitly registered inside `.gitignore` to prevent confidential credentials from being leaked to public repositories.

---
<p align="center">
  <i>Developed with passion as a Portfolio Innovation for Applied AI Hackathons 🚀</i>
</p>
