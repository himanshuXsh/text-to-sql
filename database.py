import sqlite3
import pandas as pd

def save_file_to_sqlite(uploaded_file, table_name="user_table"):
    """
    Save uploaded dataset to SQLite database.
    Supports CSV, TSV, Excel xlsx/xls, and ODS.
    """
    uploaded_file.seek(0)
    filename = uploaded_file.name.lower()

    if filename.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif filename.endswith(".tsv"):
        df = pd.read_csv(uploaded_file, sep="\t")
    elif filename.endswith((".xlsx", ".xls")):
        df = pd.read_excel(uploaded_file)
    elif filename.endswith(".ods"):
        df = pd.read_excel(uploaded_file, engine="odf")
    else:
        df = pd.read_csv(uploaded_file)  # fallback

    if df.empty or df.shape[1] == 0:
        raise ValueError("Uploaded file has no columns or is empty!")

    conn = sqlite3.connect("user_data.db")
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    return f"Saved {df.shape[0]} rows and {df.shape[1]} columns to table '{table_name}'."
