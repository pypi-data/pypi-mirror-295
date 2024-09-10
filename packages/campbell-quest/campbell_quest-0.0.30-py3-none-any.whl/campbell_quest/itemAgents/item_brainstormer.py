from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

def generate_action_item(quest, item_context, template, model):
    system_prompt = (
    "You are a dedicated AI Assistant working at a game studio.\n"
    "You have been tasked with crafting engaging and immersive item descriptions for an RPG game.\n"
    "Using the provided quest and item context, your goal is to create descriptions that not only fit seamlessly into the world but also enhance the player's experience.\n"
    "\n###\n"
    "Format the item in a clear manner similar to the provided template:\n"
    "{template}\n")
    
    user_prompt = (
    "Use the quest and item context to create descriptions according to the system instructions.\n"
    "\n###\n"
    "Quest:\n"
    "{quest}\n"
    "\n###\n"
    "Item Context:\n"
    "{item_context}\n"
    )
    
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)

    user_template = HumanMessagePromptTemplate.from_template(user_prompt)
    
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])
    
    llm = ChatOllama(model=model, temperature=1.2)
    
    agent = chat_prompt | llm | StrOutputParser()
    
    res = agent.invoke(input = { 
        "quest": quest,
        "item_context": item_context,
        "template": template
        })
    
    return res

def generate_equipment(quest, item_context, template, model):
    system_prompt = (
    "You are a dedicated AI Assistant working at a game studio.\n"
    "You have been tasked with crafting engaging and immersive item descriptions for an RPG game.\n"
    "Using the provided quest and item context, your goal is to create descriptions that not only fit seamlessly into the world but also enhance the player's experience.\n"
    "\n###\n"
    "Based on the item's characteristics, assign an appropriate value to the \"allowedEquipLocation\" field from the following options:\n"
    "Helmet, Necklace, Body, Trousers, Boots, Weapon, Shield, Gloves.\n"
    "Ensure the location reflects the nature and usage of the item within the game context.\n"
    "\n###\n"
    "Format the item in a clear manner similar to the provided template:\n"
    "{template}\n"
    )
    
    user_prompt = (
    "Use the quest and item context to create descriptions according to the system instructions.\n"
    "\n###\n"
    "Quest:\n"
    "{quest}\n"
    "\n###\n"
    "Item Context:\n"
    "{item_context}\n"
    )
    
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)

    user_template = HumanMessagePromptTemplate.from_template(user_prompt)
    
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])
    
    llm = ChatOllama(model=model, temperature=1.2)
    
    agent = chat_prompt | llm | StrOutputParser()
    
    res = agent.invoke(input = { 
        "quest": quest,
        "item_context": item_context,
        "template": template
        })
    
    return res