import streamlit as st
import pandas as pd

from database import save_file_to_sqlite
from agent_setup import create_agent_for_db
from utils import run_agent_query

# Page configuration
st.set_page_config(
    page_title="AI Text-to-SQL Chat",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI SQL Chat — Ask Questions About Your Data")

# File uploader that accepts csv, Excel, tsv, ods
uploaded_file = st.file_uploader(
    "Upload a dataset (CSV, Excel, TSV, ODS)",
    type=["csv", "xlsx", "xls", "tsv", "ods"]
)

# If a file is uploaded
if uploaded_file:
    # Attempt to preview file
    try:
        if uploaded_file.name.lower().endswith(("csv", "tsv")):
            preview_df = pd.read_csv(uploaded_file)
        else:
            preview_df = pd.read_excel(uploaded_file)
        st.write("### 📊 Dataset Preview")
        st.dataframe(preview_df.head(10))
    except Exception as e:
        st.error(f"Could not preview the dataset: {e}")

    # Save to SQLite database
    try:
        save_msg = save_file_to_sqlite(uploaded_file)
        st.success(save_msg)
    except Exception as e:
        st.error(f"Failed to save the dataset: {e}")
        st.stop()

    # Initialize agent once
    if "agent" not in st.session_state:
        try:
            st.session_state.agent = create_agent_for_db()
        except Exception as e:
            st.error(f"Agent creation failed: {e}")
            st.stop()

    st.write("---")

    # Ask user for a question
    user_query = st.text_input("Ask a question about your data")

    if user_query:
        if st.button("Run Query"):
            with st.spinner("Thinking..."):
                try:8
                
                    answer = run_agent_query(st.session_state.agent, user_query)
                
                # Option B (If your utility expects a dict):
                # answer = run_agent_query(st.session_state.agent, {"input": user_query})

                    st.write("### 🧠 Answer")
                    st.write(answer)


                except Exception as e:
                    st.error(f"Query failed: {e}")

# If no file uploaded yet
else:
    st.info("Upload a dataset file to begin.")
