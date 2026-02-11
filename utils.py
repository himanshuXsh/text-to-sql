def run_agent_query(agent, query_text):
    """
    Run the SQL agent with the given query and return the result.
    """
    result = agent.invoke(query_text)
    return result['output']
