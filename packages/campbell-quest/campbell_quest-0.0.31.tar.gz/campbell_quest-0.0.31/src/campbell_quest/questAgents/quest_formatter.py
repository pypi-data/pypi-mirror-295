from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

def format_quest(quest, schema, model):
    """
    Formats a given quest into a JSON format according to a specified schema using a language model.

    @param quest: The quest description that needs to be formatted into JSON.
    @param schema: The schema that the JSON output must adhere to.
    @param model: The language model to be used for formatting the quest.
    
    @return: A JSON formatted string of the quest.
    """
    system_prompt = (
        "You are a helpful AI Assistant at a game studio.\n"
        "Your task is to encode a given quest into a JSON format according to the provided schema.\n"
        "Review the quest and generate a JSON output that strictly adheres to the schema.\n"
        "\n###\n"
        "Schema:\n"
        "{schema}\n"
    )
    user_prompt = (
        "Please encode the given Quest into a JSON format according to the system instructions.\n"
        "\n###\n"
        "Quest:\n"
        "{quest}\n"
    )
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)
    user_template = HumanMessagePromptTemplate.from_template(user_prompt)
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])
    llm = ChatOllama(model=model, temperature=0, format="json")
    agent = chat_prompt | llm | StrOutputParser()
    res = agent.invoke(input={
        "quest": quest,
        "schema": schema
    })
    return res

def format_quest_with_rewards(quest, reward, schema, model):
    """
    Adds a "rewards" field to a JSON object of a quest according to a specified schema using a language model.

    @param quest: The JSON object of the quest that needs a rewards field added.
    @param reward: The reward information to be added to the quest JSON object.
    @param schema: The schema that the updated JSON output must adhere to.
    @param model: The language model to be used for adding the rewards field.
    
    @return: A JSON formatted string of the quest with the added rewards field.
    """
    system_prompt = (
        "You are a helpful AI Assistant at a game studio.\n"
        "Your task is to add a \"rewards\" field to a JSON object according to the provided schema.\n"
        "Ensure that the output retains all existing fields in the JSON object and only adds the \"rewards\" field.\n"
        "DO NOT modify or remove any other fields.\n"
        "\n###\n"
        "Schema:"
        "{schema}\n"
    )
    user_prompt = (
        "Please add a \"rewards\" field to the given Quest JSON object according to the system instructions.\n"
        "\n###\n"
        "Quest JSON:"
        "{quest}\n"
        "\n###\n"
        "Reward:"
        "{reward}\n"
    )
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)
    user_template = HumanMessagePromptTemplate.from_template(user_prompt)
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])
    llm = ChatOllama(model=model, temperature=0, format="json")
    agent = chat_prompt | llm | StrOutputParser()
    res = agent.invoke(input={
        "quest": quest,
        "reward": reward,
        "schema": schema
    })
    return res