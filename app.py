import streamlit as st
import pandas as pd
import os
import json
from dotenv import load_dotenv

# Import Utils
from utils.file_loader import FileLoader
from utils.db_connector import DBConnector
from utils.charts import ChartGenerator
from utils.exporters import Exporter
from utils.validators import Validator
from utils.sql_parser import SQLParser

# Import Agents
from agents.supervisor import SupervisorAgent
from agents.cleaning_agent import CleaningAgent
from agents.kpi_agent import KPIAgent
from agents.sql_agent import SQLAgent
from agents.anomaly_agent import AnomalyAgent
from agents.insight_agent import InsightAgent
from agents.recommendation_agent import RecommendationAgent
from agents.schema_agent import SchemaAgent
from agents.log_agent import LogAgent
from agents.json_agent import JSONAgent

# Page Config
st.set_page_config(page_title="Universal Data Analyzer", layout="wide", page_icon="📊")

# Custom CSS for Dark Theme and Premium Feel
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #3e4451;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session State
if 'df' not in st.session_state:
    st.session_state.df = None
if 'cleaned_df' not in st.session_state:
    st.session_state.cleaned_df = None
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar
with st.sidebar:
    st.title("🤖 AI Data Platform")
    st.subheader("Configuration")
    model_choice = st.selectbox("Groq Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"])
    source_type = st.radio("Connect Mode", ["Universal Upload", "MySQL Connection"])
    
    st.divider()
    if st.button("Clear Session"):
        st.session_state.df = None
        st.session_state.cleaned_df = None
        st.rerun()

    # Developer Section
    st.sidebar.markdown("---")
    col1, col2 = st.sidebar.columns([1, 3])
    with col1:
        st.image("https://media.licdn.com/dms/image/v2/D5603AQH62lVf6HzTaQ/profile-displayphoto-scale_400_400/B56ZrQmDwuI0Ag-/0/1764436231313?e=1778716800&v=beta&t=n2gISQgF76zt8NVZiU4VHDEPulsn34e3NKu3iX12_C8", width=50)
    with col2:
        st.markdown("**Developed by**  \nBittu Sharma")

# Main Header
st.title("Multi-Agent Data Cleaning & KPI Intelligence")
st.markdown("---")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📂 Upload/Connect", "🔍 Data Preview", "🧹 Cleaning Report", 
    "📈 Metrics", "📊 Dashboard", "💡 AI Insights", "🎯 Recommendations"
])

# --- Tab 1: Upload / Connect ---
with tab1:
    st.header("Connect your Data Source")
    
    if source_type == "Universal Upload":
        uploaded_file = st.file_uploader("Upload any file (CSV, Excel, JSON, SQL, DB, Log)", 
                                         type=["csv", "xlsx", "xls", "json", "sql", "db", "sqlite", "log", "txt"])
        if uploaded_file:
            save_path = os.path.join("uploads", uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            
            try:
                if ext == '.csv':
                    st.session_state.df = FileLoader.load_csv(save_path)
                    st.success("CSV loaded!")
                elif ext in ['.xlsx', '.xls']:
                    st.session_state.df = FileLoader.load_excel(save_path)
                    st.success("Excel loaded!")
                elif ext == '.json':
                    st.session_state.df = FileLoader.load_json(save_path)
                    st.success("JSON flattened and loaded!")
                elif ext == '.sql':
                    sql_content = uploaded_file.read().decode("utf-8")
                    parser = SQLParser(sql_content)
                    conn, tables = parser.parse_and_rebuild()
                    selected_table = st.selectbox("Select table from SQL file", tables)
                    if selected_table:
                        st.session_state.df = SQLParser.get_df_from_table(conn, selected_table)
                elif ext in ['.db', '.sqlite']:
                    db_conn = DBConnector("sqlite", {"path": save_path})
                    tables = db_conn.get_table_names()
                    selected_table = st.selectbox("Select table from DB", tables)
                    if selected_table:
                        st.session_state.df = db_conn.execute_query(f"SELECT * FROM {selected_table}")
                elif ext in ['.log', '.txt']:
                    st.session_state.df = FileLoader.load_log(save_path)
                    st.success("Log file parsed!")
            except Exception as e:
                st.error(f"Error loading file: {e}")

    elif source_type == "MySQL Connection":
        with st.form("mysql_form"):
            host = st.text_input("Host", value="localhost")
            port = st.text_input("Port", value="3306")
            user = st.text_input("User", value="root")
            pwd = st.text_input("Password", type="password")
            db_name = st.text_input("Database Name")
            if st.form_submit_button("Connect"):
                try:
                    db_conn = DBConnector("mysql", {"host": host, "port": port, "user": user, "password": pwd, "database": db_name})
                    tables = db_conn.get_table_names()
                    st.session_state.mysql_conn = db_conn
                    st.success("Connected to MySQL!")
                    selected_table = st.selectbox("Select Table", tables)
                    if selected_table:
                        st.session_state.df = db_conn.execute_query(f"SELECT * FROM {selected_table}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")

# --- Tab 2: Data Preview ---
with tab2:
    if st.session_state.df is not None:
        st.subheader("Raw Data Preview")
        st.dataframe(st.session_state.df.head(100), use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"Total Rows: {len(st.session_state.df)}")
        with col2:
            st.info(f"Total Columns: {len(st.session_state.df.columns)}")
        
        # Schema Agent Analysis
        if st.button("Run Schema Analysis"):
            schema_agent = SchemaAgent()
            analysis = schema_agent.understand_schema(st.session_state.df)
            st.markdown(f"### AI Schema Interpretation\n{analysis}")
    else:
        st.warning("Please upload data first.")

# --- Tab 3: Cleaning Report ---
with tab3:
    if st.session_state.df is not None:
        st.header("Data Cleaning Agent")
        if st.button("Auto-Clean Data"):
            cleaner = CleaningAgent()
            cleaned_df, report = cleaner.clean_data(st.session_state.df)
            st.session_state.cleaned_df = cleaned_df
            
            st.subheader("Cleaning Log")
            for item in report:
                st.write(f"- {item}")
            
            st.subheader("Cleaned Data Preview")
            st.dataframe(cleaned_df.head(50), use_container_width=True)
            
            # Export Option
            csv_data = Exporter.to_csv(cleaned_df)
            st.download_button("Download Cleaned CSV", csv_data, "cleaned_data.csv", "text/csv")
        
        if st.session_state.cleaned_df is not None:
            st.divider()
            st.subheader("Anomaly Detection")
            if st.button("Run Anomaly Detection"):
                anomaly_agent = AnomalyAgent()
                anomalies, summary = anomaly_agent.detect_anomalies(st.session_state.cleaned_df)
                st.write(summary)
                if not anomalies.empty:
                    st.dataframe(anomalies, use_container_width=True)
    else:
        st.warning("Please upload data first.")

# --- Tab 4: Metrics ---
with tab4:
    work_df = st.session_state.cleaned_df if st.session_state.cleaned_df is not None else st.session_state.df
    if work_df is not None:
        st.header("📈 Business Metrics")
        if st.button("Detect & Calculate KPIs"):
            kpi_agent = KPIAgent()
            kpis = kpi_agent.detect_kpis(work_df)
            kpi_values = kpi_agent.calculate_kpi_values(work_df, kpis)
            
            # Display KPI Cards
            cols = st.columns(len(kpi_values))
            for i, (name, val) in enumerate(kpi_values.items()):
                with cols[i]:
                    st.metric(label=name, value=f"{val:,.2f}")
            
            # Auto-Charts
            st.subheader("Visualizations")
            chart_gen = ChartGenerator()
            numeric_cols = work_df.select_dtypes(include=['number']).columns
            if len(numeric_cols) >= 2:
                fig = chart_gen.plot_bar(work_df, work_df.columns[0], numeric_cols[0], f"{numeric_cols[0]} by {work_df.columns[0]}")
                st.plotly_chart(fig, use_container_width=True)
                
                fig2 = chart_gen.plot_heatmap(work_df, "Correlation Heatmap")
                st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Please upload data first.")



# --- Tab 5: Dashboard ---
with tab5:
    work_df = st.session_state.cleaned_df if st.session_state.cleaned_df is not None else st.session_state.df
    if work_df is not None:
        st.header("📊 Interactive Data Dashboard")
        
        # Summary Charts
        st.subheader("Visual Trends")
        chart_gen = ChartGenerator()
        num_cols = work_df.select_dtypes(include=['number']).columns.tolist()
        
        if len(num_cols) > 0:
            c1, c2 = st.columns(2)
            with c1:
                y_axis = st.selectbox("Select Y-axis for Bar Chart", num_cols, key="dash_bar_y")
                st.plotly_chart(chart_gen.plot_bar(work_df, work_df.columns[0], y_axis, f"{y_axis} Distribution"), use_container_width=True)
            with c2:
                hist_col = st.selectbox("Select Column for Histogram", num_cols, key="dash_hist")
                st.plotly_chart(chart_gen.plot_histogram(work_df, hist_col, f"{hist_col} Frequency"), use_container_width=True)
        
        st.divider()
        st.subheader("💬 AI Natural Language Query")
        user_query = st.text_input("Ask a question (e.g., 'total revenue by region')")
        if user_query:
            temp_db = DBConnector("sqlite", {"path": "database/temp_query.db"})
            work_df.to_sql("data_table", temp_db.engine, if_exists="replace", index=False)
            sql_agent = SQLAgent()
            schema_str = f"Table: data_table, Columns: {work_df.columns.tolist()}"
            generated_sql = sql_agent.generate_sql(user_query, schema_str)
            st.code(generated_sql, language="sql")
            try:
                result_df = temp_db.execute_query(generated_sql)
                st.dataframe(result_df, use_container_width=True)
            except Exception as e:
                st.error(f"Query Error: {e}")
    else:
        st.warning("Please upload data first.")

# --- Tab 6: AI Insights ---
with tab6:
    work_df = st.session_state.cleaned_df if st.session_state.cleaned_df is not None else st.session_state.df
    if work_df is not None:
        st.header("Deep AI Insights")
        if st.button("Generate Insights"):
            insight_agent = InsightAgent()
            data_summary = f"Columns: {work_df.columns.tolist()}\nDescribe:\n{work_df.describe().to_string()}"
            insights = insight_agent.generate_insights(data_summary)
            st.markdown(insights)
    else:
        st.warning("Please upload data first.")

# --- Tab 7: Recommendations ---
with tab7:
    work_df = st.session_state.cleaned_df if st.session_state.cleaned_df is not None else st.session_state.df
    if work_df is not None:
        st.header("Strategic Recommendations")
        if st.button("Get Recommendations"):
            insight_agent = InsightAgent()
            data_summary = f"Columns: {work_df.columns.tolist()}\nDescribe:\n{work_df.describe().to_string()}"
            insights = insight_agent.generate_insights(data_summary)
            rec_agent = RecommendationAgent()
            recommendations = rec_agent.generate_recommendations(insights)
            st.markdown(recommendations)
    else:
        st.warning("Please upload data first.")

# Footer
st.divider()
st.markdown("Developed with ❤️ by **Bittu Sharma**")
