from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

def generate_enemy(quest, enemy_context, template, model):
    """
    Generates a unique enemy name for an RPG game based on the given quest and enemy context.

    This function utilizes a language model to craft engaging enemy names by adhering to a specified template.
    It constructs system and user prompts, processes them through a chat model, and returns a generated enemy name.

    @param quest: A string representing the quest details provided as context for generating the enemy name.
    @param enemy_context: A string containing additional context about the enemy, aiding in creating a relevant name.
    @param template: A string that defines the format or structure in which the enemy name should be generated.
    @param model: The language model to be used for generating the enemy name, encapsulated within the ChatOllama class.

    @return: A string representing the generated enemy name formatted according to the provided template.
    """
    system_prompt = (
        f"You are a dedicated AI Assistant working at a game studio.\n"
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

    # Instantiate system and user message templates based on predefined prompts
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)
    user_template = HumanMessagePromptTemplate.from_template(user_prompt)

    # Create a chat prompt using the system and user templates
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])

    # Initialize the language model with the specified parameters
    llm = ChatOllama(model=model, temperature=0.2)

    # Create an agent by piping the chat prompt through the language model and output parser
    agent = chat_prompt | llm | StrOutputParser()

    # Invoke the agent with the provided inputs and return the generated enemy name
    res = agent.invoke(input={
        "quest": quest,
        "enemy_context": enemy_context,
        "template": template
    })

    return res