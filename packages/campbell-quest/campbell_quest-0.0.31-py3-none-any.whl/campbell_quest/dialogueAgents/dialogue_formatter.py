from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

def get_formatted_required_dialogues(quest, required_dialogues, schema, model):
    """
    Formats required dialogues for a game quest into a JSON structure based on a provided schema.

    @param quest: The quest details that need to be encoded.
    @param required_dialogues: The dialogues that are required for the quest.
    @param schema: The JSON schema to adhere to when formatting the dialogues.
    @param model: The model to be used for generating the JSON output.

    @return: A JSON formatted string that represents the encoded dialogues.
    """
    system_prompt = (
        "You are a helpful AI Assistant at a game studio.\n"
        "Your task is to encode the objectives of a quest into a JSON format based on the provided schema.\n"
        "Review the required dialogues and generate a JSON output that strictly adheres to the schema.\n"
        "Ensure the output is a valid JSON without including any additional text.\n"
        "The output should ONLY include the valid JSON.\n"
        "\n###\n"
        "Schema:"
        "{schema}\n"
    )
    user_prompt = (
        "Please use the given Quest to encode the Required Dialogues into JSON format according to the system instructions.\n"
        "\n###\n"
        "Quest:\n"
        "{quest}\n"
        "\n###\n"
        "Required Dialogues:\n"
        "{required_dialogues}\n"
    )
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)
    user_template = HumanMessagePromptTemplate.from_template(user_prompt)
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])
    llm = ChatOllama(model=model, temperature=0, format="json")
    agent = chat_prompt | llm | StrOutputParser()
    res = agent.invoke(input={
        "quest": quest,
        "required_dialogues": required_dialogues,
        "schema": schema
    })
    return res

def get_formatted_dialogue_tree(dialogue_tree, model):
    """
    Formats a dialogue tree into a JSON structure, ensuring only valid JSON is returned.

    @param dialogue_tree: The dialogue tree to be formatted.
    @param model: The model to be used for processing the dialogue tree.

    @return: A JSON formatted string representing the dialogue tree.
    """
    system_prompt = (
        "You are a helpful AI Assistant at a game studio.\n"
        "You are given a dialogue tree in JSON format.\n"
        "Your task is to remove all non-JSON text, leaving only the JSON structure intact.\n"
        "Ensure the output is a valid JSON without including any additional text.\n"
        "The output should ONLY include the valid JSON.\n"
        "Avoid enclosing the response in triple backticks (```).\n"
    )
    user_prompt = (
        "Please encode the given Dialogue Tree into JSON format according to the system instructions.\n"
        "\n###\n"
        "Dialogue Tree:\n"
        "{dialogue_tree}\n"
    )
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)
    user_template = HumanMessagePromptTemplate.from_template(user_prompt)
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])
    llm = ChatOllama(model=model, temperature=0, format="json")
    agent = chat_prompt | llm | StrOutputParser()
    res = agent.invoke(input={
        "dialogue_tree": dialogue_tree
    })
    return res