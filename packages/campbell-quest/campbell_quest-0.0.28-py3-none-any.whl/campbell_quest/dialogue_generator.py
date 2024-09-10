from .dialogueAgents import dialogue_brainstormer, dialogue_refiner, dialogue_formatter
import json

def get_dialogues(quest, required_dialogues_schema, template, locations, characters, model = "llama3.1"):
    required_dialogues = dialogue_refiner.get_required_dialogues(quest, characters, model)
    
    formatted_required_dialogues = dialogue_formatter.get_formatted_required_dialogues(quest, required_dialogues, required_dialogues_schema, model)
    
    required_dialogues_json = json.loads(formatted_required_dialogues)
    
    npcs = []
    dialogue_cues = {}
    objectives = required_dialogues_json.get("objectives", [])
    for objective in objectives:
        npc_name = objective.get("npc_name")
        if npc_name not in npcs:
            npcs.append(npc_name)
        
        dialogue_cues.setdefault(npc_name, []).append(objective.get("description"))
    
    dialogue_trees = []
    for npc in npcs:
        dialogue_tree = dialogue_brainstormer.generate_dialogue(quest, npc, dialogue_cues[npc], template, locations, characters, model)
        dialogue_tree = dialogue_refiner.check_dialogue_tree(dialogue_tree, template, model)
        dialogue_tree = dialogue_formatter.get_formatted_dialogue_tree(dialogue_tree, model)
        dialogue_trees.append(dialogue_tree)
        
    return dialogue_trees