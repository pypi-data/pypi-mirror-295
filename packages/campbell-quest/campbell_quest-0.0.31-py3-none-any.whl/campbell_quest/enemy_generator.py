from .enemyAgents import enemy_brainstormer, enemy_refiner, enemy_formatter
import json

def get_enemies(quest, required_enemies_schema, enemy_template, model = "llama3.1"):
    """
    Generates a list of enemies based on the given quest and schema.

    @param quest: The quest details used to determine the required enemies.
    @param required_enemies_schema: The schema to format the required enemies.
    @param enemy_template: Template used for generating enemy details.
    @param model: The model version used for enemy generation, defaults to "llama3.1".
    @return: A list of formatted enemies.
    """
    required_items = enemy_refiner.get_required_enemies(quest, model)
    formatted_required_enemies = enemy_formatter.get_formatted_required_enemies(required_items, required_enemies_schema, model)
    required_items_json = json.loads(formatted_required_enemies)
    enemy_cues = required_items_json.get("items", [])

    enemies = []
    for enemy_cue in enemy_cues:
        enemy = enemy_brainstormer.generate_enemy(quest, enemy_cue, enemy_template, model)
        enemy = enemy_formatter.get_formatted_enemy(enemy, model)
        enemies.append(enemy)

    return enemies