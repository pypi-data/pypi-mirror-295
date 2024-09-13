from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

def generate_dialogue(quest, npc, dialogue_context, template, locations, characters, model):
    """
    Generate RPG dialogue for a given quest, NPC, and context using a language model.

    @param quest: The quest information to be used in the dialogue.
    @param npc: The name of the NPC (Non-Player Character) initiating the dialogue.
    @param dialogue_context: The context or background for the dialogue.
    @param template: The dialogue template to maintain consistency in style.
    @param locations: The locations relevant to the quest and dialogue.
    @param characters: The characters involved in the quest and dialogue.
    @param model: The language model to use for generating the dialogue.

    @return: The generated dialogue as a string.
    """

    # Define the system prompt with instructions for generating RPG dialogue
    system_prompt = (
        "You are a skilled RPG dialogue writer working on an engaging story for a fantasy role-playing game. "
        "Your task is to create captivating, context-appropriate dialogue between the player and NPCs that drives the story forward. "
        "The dialogue should reflect the ongoing quest's narrative, using the provided locations and characters. "
        "\n### Quest Information ###\n"
        "{quest}\n"
        "\n### Locations ###\n"
        "{locations}\n"
        "\n### Characters ###\n"
        "{characters}\n"
        "Make sure the dialogue is natural, aligns with the tone of the quest, and adheres to the following conditions and results:\n"
        "\n### Functions for Conditions ###\n"
        "1. has_quest(param: quest_name)\n"
        "2. has_item(param: item_name)\n"
        "3. completed_objective(param: quest_name, objective_reference)\n"
        "4. completed_quest(param: quest_name)\n"
        "\n### Functions for Results ###\n"
        "1. receive_quest(param: quest_name)\n"
        "2. complete_objective(param: objective_reference)\n"
        "3. complete_quest(param: quest_name)\n"
        "4. attack_player()\n"
        "5. add_item(param: item_name)\n"
        "6. remove_item(param: item_name)\n"
    )

    # Define the user prompt for generating dialogue with NPC initiating the conversation
    user_prompt = (
        "Generate dialogue based on the quest, NPC, and context. The NPC should initiate the conversation. "
        "Use concise, natural lines without descriptions or actions. Keep dialogue consistent with the given template.\n"
        "\n### NPC ###\n"
        "Name: {npc}\n"
        "\n### Context ###\n"
        "{dialogue_context}\n"
        "\n### Template ###\n"
        "{template}\n"
    )

    # Create system and user message templates from the defined prompts
    system_template = SystemMessagePromptTemplate.from_template(system_prompt)
    user_template = HumanMessagePromptTemplate.from_template(user_prompt)

    # Combine system and user templates into a chat prompt
    chat_prompt = ChatPromptTemplate.from_messages([system_template, user_template])

    # Initialize language model with specified parameters
    llm = ChatOllama(model=model, temperature=1.2)

    # Create an agent to process the chat prompt and language model output
    agent = chat_prompt | llm | StrOutputParser()

    # Invoke the agent with the input parameters and return the generated dialogue
    res = agent.invoke(input={
        "quest": quest,
        "locations": locations,
        "characters": characters,
        "npc": npc,
        "dialogue_context": dialogue_context,
        "template": template
    })

    return res