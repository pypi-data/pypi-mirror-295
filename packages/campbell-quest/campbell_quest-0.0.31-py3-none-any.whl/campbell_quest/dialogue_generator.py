from .dialogueAgents import dialogue_brainstormer, dialogue_refiner, dialogue_formatter
import json

def get_dialogues(quest, required_dialogues_schema, template, locations, characters, model = "llama3.1"):
    """
    Generate dialogue trees for a given quest using various dialogue agents.

    @param quest: The quest context for which dialogues are being generated.
    @param required_dialogues_schema: The schema defining the structure of required dialogues.
    @param template: Template used for dialogue generation.
    @param locations: List of locations relevant to the quest.
    @param characters: List of characters involved in the quest.
    @param model: The model version used for dialogue generation, default is "llama3.1".
    
    @return: A list of dialogue trees generated for the quest.
    """
    
    # Get the required dialogues based on the quest and characters using the specified model.
    required_dialogues = dialogue_refiner.get_required_dialogues(quest, characters, model)
    
    # Format the required dialogues according to the given schema and model.
    formatted_required_dialogues = dialogue_formatter.get_formatted_required_dialogues(
        quest, required_dialogues, required_dialogues_schema, model
    )
    
    # Parse the formatted dialogues into JSON.
    required_dialogues_json = json.loads(formatted_required_dialogues)
    
    npcs = []  # List to store unique NPC names encountered in the objectives.
    dialogue_cues = {}  # Dictionary to store dialogue cues for each NPC.
    
    # Extract objectives from the parsed JSON and organize dialogue cues by NPC.
    objectives = required_dialogues_json.get("objectives", [])
    for objective in objectives:
        npc_name = objective.get("npc_name")
        if npc_name not in npcs:
            npcs.append(npc_name)
        dialogue_cues.setdefault(npc_name, []).append(objective.get("description"))
    
    dialogue_trees = []  # List to store the generated dialogue trees.
    
    # Generate dialogue trees for each NPC based on the dialogue cues and other parameters.
    for npc in npcs:
        dialogue_tree = dialogue_brainstormer.generate_dialogue(
            quest, npc, dialogue_cues[npc], template, locations, characters, model
        )
        
        # Refine and format the generated dialogue tree.
        dialogue_tree = dialogue_refiner.check_dialogue_tree(dialogue_tree, template, model)
        dialogue_tree = dialogue_formatter.get_formatted_dialogue_tree(dialogue_tree, model)
        
        # Add the formatted dialogue tree to the list.
        dialogue_trees.append(dialogue_tree)
    
    return dialogue_trees  # Return the list of dialogue trees.