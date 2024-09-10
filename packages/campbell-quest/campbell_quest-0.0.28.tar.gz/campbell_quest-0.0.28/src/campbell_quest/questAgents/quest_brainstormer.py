from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

def generate_quest(objective_info, quest_prompt, locations, characters, model):
    system_prompt = (
    "You are a Quest Designer at a Game studio.\n"
    "You have been tasked with creating compelling Side-Quests for a Role-Playing Game.\n"
    "The game is set in a Fantasy setting.\n"
    "Consider the locations and characters given and generate a quest.\n"
    "\n###\n"
    "The quest should be of a type outlined in the 'quest_objectives' below:\n"
    "{objective_info}\n"
    "\n###\n"
    "Locations:\n"
    "{locations}\n"
    "\n###\n"
    "Characters:\n"
    "{characters}\n"
    )
    
    user_prompt = (
    "As a Quest Designer at a Game Studio, your task is to generate an appropriate quest based on the given quest prompt and system instructions.\n"
    "Ensure you do not introduce new characters or locations, and avoid adding any extra requirements or restrictions.\n"
    "Use only the provided characters and locations that fit logically within the context of the quest.\n"
    "Avoid adding any new information to the existing locations.\n"
    "\n###\n"
    "Quest Prompt:\n"
    "{quest_prompt}\n"
    "\n###\n"
    "Describe the quest in the format given:\n"
    "Name:\nType:\nGoal:\nDescription:\n"
    "\n###\n"
    "Remember to adhere to the system instructions.\n"
    )
    
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)

    user_template = HumanMessagePromptTemplate.from_template(user_prompt)
    
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])
    
    llm = ChatOllama(model=model, temperature=1.2)
    
    agent = chat_prompt | llm | StrOutputParser()
    
    res = agent.invoke(input = {
        "objective_info":objective_info, 
        "quest_prompt": quest_prompt,
        "locations": locations,
        "characters": characters
        })
    
    return res