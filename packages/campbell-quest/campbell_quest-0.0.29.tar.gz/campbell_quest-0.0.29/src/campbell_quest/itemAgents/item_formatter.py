from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

def get_formatted_required_items(required_items, schema, model):
    system_prompt = (
    "You are a helpful AI Assistant at a game studio.\n"
    "Your task is to encode the items given into a JSON format based on the provided schema.\n"
    "Review the required items and generate a JSON output that strictly adheres to the schema.\n"
    "Ensure the output is a valid JSON without including any additional text.\n"
    "The output should ONLY include the valid JSON.\n"    
    "\n###\n"    
    "Schema:"
    "{schema}\n")
    
    user_prompt = (
    "Please encode the Required Items into JSON format according to the system instructions.\n"
    "\n###\n"   
    "Required Items:\n"
    "{required_items}\n"
    )
    
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)
    
    user_template = HumanMessagePromptTemplate.from_template(user_prompt)
    
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])
    
    llm = ChatOllama(model=model, temperature=0, format="json")
    
    agent = chat_prompt | llm | StrOutputParser()
    
    res = agent.invoke(input = {
        "required_items": required_items,
        "schema": schema
        })
    
    return res

def get_formatted_item(item, model):
    system_prompt = (
    "You are a helpful AI Assistant at a game studio.\n"
    "You are given an item description in JSON format.\n"
    "Your task is to remove all non-JSON text, leaving only the JSON structure intact.\n"
    "Ensure the output is a valid JSON without including any additional text.\n"
    "The output should ONLY include the valid JSON.\n"
    "Avoid enclosing the response in triple backticks (```).\n"
    )
    
    user_prompt = (
    "Please encode the given Item into JSON format according to the system instructions.\n"
    "\n###\n"
    "Item:\n"
    "{item}\n"
    )
    
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)
    
    user_template = HumanMessagePromptTemplate.from_template(user_prompt)
    
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])
    
    llm = ChatOllama(model=model, temperature=0, format="json")
    
    agent = chat_prompt | llm | StrOutputParser()
    
    res = agent.invoke(input = {
        "item": item
        })
    
    return res