from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

def get_required_dialogues(quest, characters, model):
    system_prompt = (
    "As a Writer at a Game Studio, you have received a Quest concept from the Narrative Designer.\n"
    "This concept includes a list of required objectives.\n"
    "Your task is to review each objective and determine if it involves the player needing to interact with an NPC.\n"
    "\n###\n"
    "Only output the objectives which require player interaction.\n"
    "Describe the output in the format given:\n"
    "NPC Name:\nObjective\n")
    
    user_prompt = (
    "Consider the quest and characters given and determine whether the player needs to talk to an NPC.\n"
    "Adhere to the system instructions.\n"
    "\n###\n"
    "Quest:\n"
    "{quest}\n"
    "\n###\n"
    "Characters:\n"
    "{characters}\n")
    
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)

    user_template = HumanMessagePromptTemplate.from_template(user_prompt)
    
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])
    
    llm = ChatOllama(model=model, temperature=0)
    
    agent = chat_prompt | llm | StrOutputParser()
    
    res = agent.invoke(input = { 
        "quest": quest,
        "characters": characters
        })
    
    return res

def check_dialogue_tree(dialogue, example, model):
    system_prompt = (
    "You are a helpful AI Assistant at a game studio.\n"
    "Your task is to ensure that the dialogue tree between a player and an NPC is cohesive and logically consistent. "
    "Each branch of the dialogue must flow naturally and make sense within the overall story. "
    "The conditions and outcomes should align with the context of the story and character interactions.\n"
    "Your objective is to review the dialogue tree and check that the flow of the conversation maintains narrative integrity. "
    "Ensure that the dialogue branches have logical transitions and lead to coherent outcomes.\n\n"
    "Additionally, ensure that the `condition` and `result` properties use only the following functions:\n"
    "### Available Condition Functions:\n"
    "1. has_quest(param: quest_name)\n"
    "2. has_item(param: item_name)\n"
    "3. completed_objective(param: objective_reference)\n"
    "4. completed_quest(param: quest_name)\n\n"
    "### Available Result Functions:\n"
    "1. receive_quest(param: quest_name)\n"
    "2. complete_objective(param: objective_reference)\n"
    "3. complete_quest(param: quest_name)\n"
    "4. attack_player()\n"
    "5. add_item(param: item_name)\n"
    "6. remove_item(param: item_name)\n\n"
    "Remove any `condition` or `result` properties not listed above. "
    "Insert missing quest functions where they logically belong within the dialogue tree.\n\n"
    "### Example Dialogue Tree:\n"
    "{example}\n")
    
    user_prompt = (
    "Check the dialogue tree given below according to system instructions.\n"
    "\n###\n"
    "Dialogue:\n"
    "{dialogue}\n")
    
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)

    user_template = HumanMessagePromptTemplate.from_template(user_prompt)
    
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])
    
    llm = ChatOllama(model=model, temperature=0)
    
    agent = chat_prompt | llm | StrOutputParser()
    
    res = agent.invoke(input = { 
        "dialogue": dialogue,
        "example": example
        })
    
    return res