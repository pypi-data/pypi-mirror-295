from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

def get_required_items(quest, model):
    system_prompt = (f"You are a dedicated AI Assistant working at a game studio.\n"
    "Your role is to assist the Narrative Designer by evaluating a Quest concept that has been provided.\n"
    "This concept outlines a series of objectives related to the player's journey.\n\n"
    "Your task is to carefully analyze each objective and identify any items the player needs to interact with to complete that objective.\n"
    "Focus only on the items required for interaction; do not include objectives involving NPC interactions, as they do not constitute item interactions.\n"
    "Once you identify the necessary items, classify each one by selecting a type from the following list:\n"
    "1. Action Item: Items that can be used one time, providing temporary benefits, effects, or simply filling a spot in the inventory.\n"
    "These may be consumed upon use or have limited duration. They might offer direct advantages, trigger events, or serve as collectibles.\n"
    "2. Equipment: Items that can be worn or wielded to enhance the player's abilities or alter their appearance.\n"
    "These items can be equipped in various slots (e.g., head, chest, weapon).\n"
    "3. Stat-Boosting Equipment: Equipment that offers permanent stat bonuses or other lasting benefits while equipped.\n\n"
    "Once you have classified the items, your next task is to determine the most appropriate objective type for each item based on the player's interaction with it. Choose from the following two options:\n"
    "1. Pickup Item: The item must be collected or acquired by the player, typically to be added to their inventory or used later in the quest.\n"
    "2. Destroy Item: The item must be eliminated, broken, or otherwise removed from existence by the player as part of the quest objective.\n"   
    "\n###\n"
    "Ensure that the output contains ONLY ITEMS, omitting any characters (whether enemies, allies, or otherwise).\n"
    "Use the following format for the output:\n"
    "Item Name:\nItem Type:\nObjective Reference:\nObjective Type:\n")
    
    user_prompt = (f"Consider the quest given and determine whether the player needs to interact with an item.\n"
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