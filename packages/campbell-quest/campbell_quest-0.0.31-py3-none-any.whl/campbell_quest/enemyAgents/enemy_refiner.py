from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

def get_required_enemies(quest, model):
    """
    Analyzes a quest to identify required enemies for each objective.

    @param quest: A string representing the quest concept that outlines the series of objectives related to the player's journey.
    @param model: The model to use for generating the chat-based analysis.

    @return: A structured string output detailing enemy names and their corresponding objective references.
    """
    
    # Define the system prompt providing instructions to the AI assistant.
    system_prompt = (
        "You are a dedicated AI Assistant working at a game studio.\n"
        "Your role is to assist the Narrative Designer by evaluating a Quest concept that has been provided.\n"
        "This concept outlines a series of objectives related to the player's journey.\n\n"
        "Your task is to carefully analyze each objective and identify any enemies the player needs to fight with to complete that objective.\n"
        "Focus only on the enemies; do not include objectives involving friendly interactions.\n"
        "Use the following format for the output:\n"
        "Enemy Name:\n"
        "Objective Reference:\n"
    )
    
    # Define the user prompt instructing the AI to analyze the quest.
    user_prompt = (
        f"Consider the quest given and determine whether the player needs to fight with an enemy.\n"
        "Adhere to the system instructions.\n"
        "\n###\n"
        "Quest:\n"
        "{quest}\n"
    )
    
    # Create system and user message templates from the defined prompts.
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)
    user_template = HumanMessagePromptTemplate.from_template(user_prompt)
    
    # Combine the system and user templates into a chat prompt.
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])
    
    # Initialize a chat model with the specified model and a fixed temperature.
    llm = ChatOllama(model=model, temperature=0)
    
    # Create an agent that processes the chat prompt through the language model and parses the output.
    agent = chat_prompt | llm | StrOutputParser()
    
    # Invoke the agent with the provided quest input and return the result.
    res = agent.invoke(input={"quest": quest})
    return res