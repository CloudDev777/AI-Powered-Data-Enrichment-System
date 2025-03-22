# 🚀 AI-Powered Data Enrichment System  
_Automate lead generation with LLM-enhanced web scraping and CRM-ready outputs_

![Banner](https://caprae-leadgen-tool-ywtu9ekczpkeakcazg8d8u.streamlit.app/banner.png)

---

![Stars](https://img.shields.io/github/stars/rishi02102017/caprae-leadgen-tool?style=social)
![Forks](https://img.shields.io/github/forks/rishi02102017/caprae-leadgen-tool?style=social)
![Issues](https://img.shields.io/github/issues/rishi02102017/caprae-leadgen-tool)

[![Streamlit App](https://img.shields.io/badge/Live%20Demo-Streamlit-green?style=flat-square&logo=streamlit)](https://caprae-leadgen-tool-ywtu9ekczpkeakcazg8d8u.streamlit.app)
[![Open in Colab](https://img.shields.io/badge/Run%20in%20Colab-grey?style=flat-square&logo=google-colab)](https://colab.research.google.com/drive/1X83VZ9NIeDUuY5SjtQP8sZhYpLFkrAWs?usp=sharing)
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)](#license)

---

## 🧠 Overview

**AI-Powered Data Enrichment System** is an end-to-end automation tool that transforms raw tabular data (CSV) into enriched, structured information for lead generation, marketing, and CRM systems.

It uses:

- 🔍 **SerpAPI** for real-time web search  
- 🧠 **Groq LLaMA3** (via LangChain) for structured context extraction  
- 📤 **Pandas** for smart CSV transformation & export  

---

## ✨ Features

- ✅ Upload and parse any CSV
- 🧩 Real-time query generation from selected columns
- 🌐 Dynamic web scraping with SerpAPI
- 🧠 LLM-based information enrichment with Groq’s LLaMA3
- 📁 Export enriched leads in CRM-ready format
- 💻 Interactive UI with Streamlit (or Flask if using `/templates/`)
- 🌙 Optional dark/light mode support

---

## 🖼️ Project Structure

├── app.py # Entry point ├── .env # Environment variables (API keys) ├── requirements.txt # Python dependencies

├── modules/ │ ├── init.py │ ├── data_processor.py # Handles CSV upload, enrichment, export │ ├── llm_processor.py # Handles LLM-based extraction (Groq + LangChain) │ └── search_engine.py # Performs web search using SerpAPI

├── static/ │ └── css/ │ └── style.css # UI styling

├── templates/ │ ├── index.html # Main interface │ ├── configure.html # Query builder │ └── results.html # Output view

├── uploads/ │ ├── cities.csv # Sample CSV │ ├── companies.csv # Sample CSV │ └── enriched_data.csv # Output after enrichment

└── README.md


---

## ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/rishi02102017/caprae-leadgen-tool.git
cd caprae-leadgen-tool

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API keys in a .env file
touch .env


.env file format:

env
Copy
Edit
SERPAPI_API_KEY=your_serpapi_key
GROQ_API_KEY=your_groq_api_key


🚀 Run the App
bash
Copy
Edit
streamlit run app.py


📊 Powered By
Tech Stack	Role
🐍 Python	Backend scripting
🌐 SerpAPI	Web search engine
🧠 LangChain + Groq	Contextual data extraction
📦 Pandas	DataFrame handling & CSV ops
🎨 Streamlit/Flask	Frontend UI
📁 Dotenv	Secure API handling