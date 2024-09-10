from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

def define_quest_objectives(quest, locations, characters, model):    
    system_prompt = (
    "You are a Writer at a Game studio.\n"
    "You have been tasked with editing given Side-Quests for a Role-Playing Game.\n"
    "The quest, the character and the location information is given to you.\n"
    "Adhere to the information provided.\n"
    "\n###\n"
    "Quest:\n"
    "{quest}\n"
    "\n###\n"
    "Locations:\n"
    "{locations}\n"
    "\n###\n"
    "Characters:\n"
    "{characters}\n"
    )
    
    user_prompt = (
    "As a Writer at a Game Studio, your task is to revise the quest provided in the system instructions.\n"
    "Your goal is to rewrite the quest to include a detailed list of clear and concise objectives.\n"
    "Each objective should outline a single, specific action that the player needs to complete.\n"
    "Ensure that these objectives are logical and coherent within the context of the quest.\n"
    "Use ONLY the given quest to create the objectives.\n"
    "Do not generate any additional information beyond what is provided.\n"
    "\nDescribe the quest in the format given:\n"
    "Name:\nDescription:\nGoal:\nObjectives:\n"
    )
    
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)

    user_template = HumanMessagePromptTemplate.from_template(user_prompt)
    
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])
    
    llm = ChatOllama(model=model, temperature=0)
    
    agent = chat_prompt | llm | StrOutputParser()
    
    res = agent.invoke(input = {
        "quest": quest,
        "locations": locations,
        "characters": characters
        })
    
    return res

def define_quest_reward(quest, rewards, model):    
    system_prompt = (
    "You are a Quest Designer at a Game studio.\n"
    "You have been tasked with choosing the appropriate reward for a given Side-Quest.\n"
    "Consider the quest provided and pick a reward from the list given.\n"
    "ONLY pick an item from the list.\n"
    "You MUST pick some reward.\n"
    "\n###\n"
    "Quest:"
    "{quest}\n"
    "\n###\n"
    "Rewards:"
    "{rewards}\n"
    )
    
    user_prompt = ("Using the provided Quest and Rewards, pick an appropriate reward according to the system instructions.\n")
    
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)
    
    user_template = HumanMessagePromptTemplate.from_template(user_prompt)
    
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])
    
    llm = ChatOllama(model=model, temperature=0)
    
    agent = chat_prompt | llm | StrOutputParser()
    
    res = agent.invoke(input = {
        "quest": quest,
        "rewards": rewards
        })
    
    return res