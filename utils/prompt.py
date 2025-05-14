def amend_prompt_with_tool(prompt, result):

    amended_prompt = f"""
    you are a helpful assistant with access to a variety of tools at your disposable.
    The user as provided the query: '{prompt}.'
    
    
    
    You have determine that a tool is suitable to answer the user's query.
    You used the tool with the user's query and the result from the tool is: '{result}'

    Using the user's query and the result obtained from the tool, provide an proper answer back to the user to answer his query

    """
    return amended_prompt
    