from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

def generate_enemy(quest, enemy_context, template, model):
    system_prompt = (f"You are a dedicated AI Assistant working at a game studio.\n"
    "You have been tasked with crafting engaging enemy names for an RPG game.\n"
    "Using the provided quest and enemy context, your goal is to create a unique enemy name.\n"
    "\n###\n"
    "Format the enemy in a clear manner similar to the provided template:\n"
    "{template}\n"
    )
    
    user_prompt = (
    "Consider the quest and enemy context given and create unique enemy names.\n"
    "Adhere to the system instructions.\n"
    "\n###\n"
    "Quest:\n"
    "{quest}\n"
    "\n###\n"
    "Enemy Context:\n"
    "{enemy_context}\n"
    )
    
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)

    user_template = HumanMessagePromptTemplate.from_template(user_prompt)
    
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])
    
    llm = ChatOllama(model=model, temperature=0.2)
    
    agent = chat_prompt | llm | StrOutputParser()
    
    res = agent.invoke(input = { 
        "quest": quest,
        "enemy_context": enemy_context,
        "template": template
        })
    
    return res