from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

def get_formatted_required_items(required_items, schema, model):
    """
    Formats a list of required items into a JSON string according to a specified schema.

    This function takes a list of required items and a schema, then uses a language model
    to format these items into a JSON string that adheres strictly to the given schema.

    @param required_items: The items that need to be formatted into JSON.
    @param schema: The schema that the JSON output should adhere to.
    @param model: The language model to be used for formatting.
    @return: A JSON-formatted string of the required items.
    """
    system_prompt = (
        "You are a helpful AI Assistant at a game studio.\n"
        "Your task is to encode the items given into a JSON format based on the provided schema.\n"
        "Review the required items and generate a JSON output that strictly adheres to the schema.\n"
        "Ensure the output is a valid JSON without including any additional text.\n"
        "The output should ONLY include the valid JSON.\n"
        "\n###\n"
        "Schema:"
        "{schema}\n"
    )
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
    res = agent.invoke(input={
        "required_items": required_items,
        "schema": schema
    })
    return res

def get_formatted_item(item, model):
    """
    Formats a single item description into a JSON string.

    This function takes a single item description in JSON format and processes it to
    ensure that only the JSON structure is returned, stripping away any non-JSON text.

    @param item: The item description that needs to be formatted.
    @param model: The language model to be used for formatting.
    @return: A JSON-formatted string of the item.
    """
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
    res = agent.invoke(input={
        "item": item
    })
    return res
