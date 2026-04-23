# Multi-Agent Data Cleaning, KPI Intelligence & Universal Data Analyzer

This is a production-style AI application built with **Streamlit**, **Python**, and **Groq API**. It features a multi-agent architecture to handle data loading, cleaning, schema understanding, KPI detection, anomaly detection, AI insights, and natural language SQL.

## 🚀 Features

- **Universal Data Support**: CSV, Excel, JSON (nested/flattened), SQL scripts, SQLite, PostgreSQL, and Server Logs.
- **Multi-Agent Architecture**: 
  - **Supervisor Agent**: Routes tasks.
  - **Cleaning Agent**: Automatically cleans messy data.
  - **KPI Agent**: Detects business KPIs automatically.
  - **SQL Agent**: Natural language to SQL.
  - **Anomaly Agent**: Statistical and ML-based outlier detection.
  - **Insight & Recommendation Agents**: High-level business strategy.
- **Premium UI**: Dark-themed dashboard with interactive Plotly charts.
- **Export Center**: Export cleaned data to CSV/Excel.

## 🛠 Tech Stack

- **Frontend**: Streamlit
- **AI/LLM**: Groq API (Llama 3, Mixtral)
- **Data Processing**: Pandas, NumPy, Scikit-learn
- **Visualization**: Plotly
- **Database**: SQLite (Internal), PostgreSQL (Connector)

## 📋 Setup Instructions

1. **Clone the repository**:
   ```bash
   cd universal_data_analyzer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   - Create a `.env` file from `.env.example`.
   - Add your **Groq API Key**:
     ```
     GROQ_API_KEY=gsk_your_key_here
     ```

4. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## 📂 Project Structure

- `app.py`: Main entry point.
- `agents/`: Contains specialized AI agents.
- `utils/`: Core utilities for files, DBs, and charts.
- `uploads/`: Temporary storage for uploaded files.
- `exports/`: Destination for processed files.
- `database/`: App-internal SQLite data.

## 🧪 Example Files Included

You can find test files (CSV, JSON, Logs) in the `uploads/` directory after running some initial tests.

## 🛡 License

MIT License
