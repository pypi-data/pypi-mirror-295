from .itemAgents import item_brainstormer, item_refiner, item_formatter
import json

def get_items(quest, required_items_schema, item_templates, model="llama3.1"):
    """
    Generate a list of items based on a quest and item templates.

    @param quest: The quest data used to generate items.
    @param required_items_schema: The schema used to format the required items.
    @param item_templates: A dictionary of item templates categorized by item type.
    @param model: The model version used for generating and refining items. Defaults to "llama3.1".
    
    @return: A list of formatted items generated for the quest.
    """
    required_items = item_refiner.get_required_items(quest, model)
    formatted_required_items = item_formatter.get_formatted_required_items(required_items, required_items_schema, model)
    required_items_json = json.loads(formatted_required_items)
    item_cues = required_items_json.get("items", [])
    items = []

    for item_cue in item_cues:
        item_type = item_cue.get("item_type")
        item_template = item_templates.get(item_type)
        item = None

        if item_type == "Action Item":
            item = item_brainstormer.generate_action_item(quest, item_cue, item_template, model)
        else:
            item = item_brainstormer.generate_equipment(quest, item_cue, item_template, model)

        item = item_formatter.get_formatted_item(item, model)
        items.append(item)

    return items