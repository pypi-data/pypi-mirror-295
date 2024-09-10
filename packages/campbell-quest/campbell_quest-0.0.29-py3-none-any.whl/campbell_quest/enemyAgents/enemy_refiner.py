from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

def get_required_enemies(quest, model):
    system_prompt = (
    "You are a dedicated AI Assistant working at a game studio.\n"
    "Your role is to assist the Narrative Designer by evaluating a Quest concept that has been provided.\n"
    "This concept outlines a series of objectives related to the player's journey.\n\n"
    "Your task is to carefully analyze each objective and identify any enemies the player needs to fight with to complete that objective.\n"
    "Focus only on the enemies; do not include objectives involving friendly interactions.\n"
    "Use the following format for the output:\n"
    "Enemy Name:\nObjective Reference:\n")
    
    user_prompt = (f"Consider the quest given and determine whether the player needs to fight with an enemy.\n"
    "Adhere to the system instructions.\n"
    "\n###\n"
    "Quest:\n"
    "{quest}\n")
    
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)

    user_template = HumanMessagePromptTemplate.from_template(user_prompt)
    
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])
    
    llm = ChatOllama(model=model, temperature=0)
    
    agent = chat_prompt | llm | StrOutputParser()
    
    res = agent.invoke(input = { 
        "quest": quest
        })
    
    return res