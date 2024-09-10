from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

def get_formatted_required_enemies(required_enemies, schema, model):
    system_prompt = (
    "You are a helpful AI Assistant at a game studio.\n"
    "Your task is to encode the enemies given into a JSON format based on the provided schema.\n"
    "Review the required enemies and generate a JSON output that strictly adheres to the schema.\n"
    "Ensure the output is a valid JSON without including any additional text.\n"
    "The output should ONLY include the valid JSON.\n"
    "\n###\n"
    "Schema:"
    "{schema}\n"
    )
    
    user_prompt = (
    "Please encode the Required Enemies into JSON format according to the system instructions.\n"
    "\n###\n"
    "Required Enemies:\n"
    "{required_enemies}\n"
    )
    
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)
    
    user_template = HumanMessagePromptTemplate.from_template(user_prompt)
    
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])
    
    llm = ChatOllama(model=model, temperature=0, format="json")
    
    agent = chat_prompt | llm | StrOutputParser()
    
    res = agent.invoke(input = {
        "required_enemies": required_enemies,
        "schema": schema
        })
    
    return res

def get_formatted_enemy(enemy, model):
    system_prompt = (
    "You are a helpful AI Assistant at a game studio.\n"
    "You are given an enemy description in JSON format.\n"
    "Your task is to remove all non-JSON text, leaving only the JSON structure intact.\n"
    "Ensure the output is a valid JSON without including any additional text.\n"
    "The output should ONLY include the valid JSON.\n"
    "Avoid enclosing the response in triple backticks (```).\n"
    )
    
    user_prompt = (
    "Please encode the given Enemy into JSON format according to the system instructions.\n"
    "\n###\n"
    "Enemy:\n"
    "{enemy}\n"
    )
    
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)
    
    user_template = HumanMessagePromptTemplate.from_template(user_prompt)
    
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])
    
    llm = ChatOllama(model=model, temperature=0, format="json")
    
    agent = chat_prompt | llm | StrOutputParser()
    
    res = agent.invoke(input = {
        "enemy": enemy
        })
    
    return res