from .questAgents import quest_brainstormer, quest_refiner, quest_formatter

def generate_initial_quest(quest_prompt, objective_info, location_info, character_info, model = "llama3.1"):
    """
    Generate an initial quest based on the provided information and model.

    @param quest_prompt: A string containing the initial quest prompt.
    @param objective_info: A dictionary or object containing the quest's objective information.
    @param location_info: A dictionary or object containing the quest's location information.
    @param character_info: A dictionary or object containing the quest's character information.
    @param model: A string specifying the model to use for quest generation. Default is "llama3.1".
    
    @return: A string representing the initial generated quest.
    """
    initial_generated_quest = quest_brainstormer.generate_quest(objective_info, quest_prompt, location_info, character_info, model)
    return initial_generated_quest

def generate_quest_with_objectives(initial_generated_quest, location_info, character_info, model = "llama3.1"):
    """
    Enhance the initial quest by defining specific objectives.

    @param initial_generated_quest: A string representing the initial generated quest.
    @param location_info: A dictionary or object containing the quest's location information.
    @param character_info: A dictionary or object containing the quest's character information.
    @param model: A string specifying the model to use for refining the quest. Default is "llama3.1".
    
    @return: A string representing the quest with defined objectives.
    """
    quest_with_objectives = quest_refiner.define_quest_objectives(initial_generated_quest, location_info, character_info, model)
    return quest_with_objectives

def generate_quest_reward(initial_generated_quest, rewards, model = "llama3.1"):
    """
    Define rewards for the quest based on the initial quest details.

    @param initial_generated_quest: A string representing the initial generated quest.
    @param rewards: A list or object containing possible rewards for the quest.
    @param model: A string specifying the model to use for defining the quest rewards. Default is "llama3.1".
    
    @return: A string representing the quest with defined rewards.
    """
    quest_reward = quest_refiner.define_quest_reward(initial_generated_quest, rewards, model)
    return quest_reward

def get_formatted_quest(quest, schema, model = "llama3.1"):
    """
    Format the quest according to a specified schema.

    @param quest: A string representing the quest to be formatted.
    @param schema: A dictionary or object defining the schema for formatting the quest.
    @param model: A string specifying the model to use for formatting. Default is "llama3.1".
    
    @return: A formatted quest as a string.
    """
    return quest_formatter.format_quest(quest, schema, model)

def get_formatted_quest_with_rewards(quest, reward, schema, model = "llama3.1"):
    """
    Format the quest along with its rewards according to a specified schema.

    @param quest: A string representing the quest to be formatted.
    @param reward: A string or object representing the rewards associated with the quest.
    @param schema: A dictionary or object defining the schema for formatting the quest and rewards.
    @param model: A string specifying the model to use for formatting. Default is "llama3.1".
    
    @return: A formatted quest with rewards as a string.
    """
    return quest_formatter.format_quest_with_rewards(quest, reward, schema, model)