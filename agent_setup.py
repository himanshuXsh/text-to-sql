import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.agents import create_sql_agent

# Make sure your Google API key is set

def create_agent_for_db():
    """
    This function creates a LangChain SQL Agent connected to the SQLite database.
    """
    
    # Connect to the local SQLite database file your app creates
    db = SQLDatabase.from_uri("sqlite:///user_data.db")

    # Initialize the language model using Google Gemini
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    # Create the SQL agent using the create_sql_agent function
    agent = create_sql_agent(
        llm=model,
        db=db,
        agent_type="openai-tools",
        verbose=True
    )

    return agent
