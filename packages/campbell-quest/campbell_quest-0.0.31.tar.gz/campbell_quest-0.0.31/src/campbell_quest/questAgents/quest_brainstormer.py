from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

def generate_quest(objective_info, quest_prompt, locations, characters, model):
    """
    Generate a side quest for a Role-Playing Game based on provided objectives, locations, and characters.

    This function utilizes language model prompts to generate a quest description.
    It combines system and user prompts to instruct the model on how to generate the quest.

    @param objective_info: Information about the quest objectives, outlining the type of quest.
    @param quest_prompt: A prompt that provides the initial context or theme for the quest.
    @param locations: A list of locations available for use in the quest.
    @param characters: A list of characters that can be included in the quest.
    @param model: The language model to be used for generating the quest.

    @return: The generated quest as a string, following the specified format.
    """

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

    # Create a system message template from the provided system prompt
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)
    
    # Create a human message template from the provided user prompt
    user_template = HumanMessagePromptTemplate.from_template(user_prompt)
    
    # Combine system and user message templates into a chat prompt
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])
    
    # Initialize the language model with the specified model and temperature settings
    llm = ChatOllama(model=model, temperature=1.2)
    
    # Create an agent pipeline with the chat prompt, language model, and output parser
    agent = chat_prompt | llm | StrOutputParser()
    
    # Invoke the agent with the input data to generate the quest
    res = agent.invoke(input={
        "objective_info": objective_info,
        "quest_prompt": quest_prompt,
        "locations": locations,
        "characters": characters
    })
    
    return res