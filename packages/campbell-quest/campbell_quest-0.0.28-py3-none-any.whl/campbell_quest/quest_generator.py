from .questAgents import quest_brainstormer, quest_refiner, quest_formatter

def generate_initial_quest(quest_prompt, objective_info, location_info, character_info, model = "llama3.1"):
    initial_generated_quest = quest_brainstormer.generate_quest(objective_info, quest_prompt, location_info, character_info, model)
    return initial_generated_quest

def generate_quest_with_objectives(initial_generated_quest, location_info, character_info, model = "llama3.1"):
    quest_with_objectives = quest_refiner.define_quest_objectives(initial_generated_quest, location_info, character_info, model)
    return quest_with_objectives

def generate_quest_reward(initial_generated_quest, rewards, model = "llama3.1"):    
    quest_reward = quest_refiner.define_quest_reward(initial_generated_quest, rewards, model)
    return quest_reward

def get_formatted_quest(quest, schema, model = "llama3.1"):
    return quest_formatter.format_quest(quest, schema, model)

def get_formatted_quest_with_rewards(quest, reward, schema, model = "llama3.1"):
    return quest_formatter.format_quest_with_rewards(quest, reward, schema, model)

