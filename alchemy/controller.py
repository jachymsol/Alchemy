from .recipes import Recipes
from .inventory import Inventory
from .logging import Logging
from .client import Client

class Controller:
    """ 
        Controller to deal with the logic of the game. 
    """
    
    def __init__(self, recipes=None, start_log_file_name=None, client=False, team_name=None):
        self.BASIC_ITEMS = ["kamen", "voda", "vzduch", "zeme"]
        self.recipes = Recipes(self, recipes)
        self.inventory = Inventory(self)
        self.team_name = team_name
        self.logging = Logging(self, self.team_name)

        if start_log_file_name:
            self.execute_log(start_log_file_name)

        if client:
            self.client = Client(client)
            self.client.connect(team_name)

    def get_basic_items(self):
        return self.BASIC_ITEMS

    def import_recipes(self, file_name):
        self.recipes.import_from_file(file_name)
        self.logging.log_imported_recipes(file_name)
    
    def get_inventory_items(self):
        return self.inventory.get_item_names()

    def get_inventory_as_list(self):
        return self.inventory.list_items()

    def get_inventory_as_string(self):
        return self.inventory.print_items()

    def get_tried_combinations(self):
        return self.recipes.get_tried_combinations()

    def add_item(self, item, count):
        self.inventory.add_item(item, int(count))
        self.logging.log_added_item(item, count)
    
    def experiment(self, item1, item2):
        self.logging.log_experiment_start(item1, item2)
        if not self.inventory.has_items([item1, item2]):
            if not self.inventory.knows_item(item1) or not self.inventory.knows_item(item2):
                self.logging.log_experiment_unknown_items()
                return (False, None)
            else:
                (success, needed) = self.inventory.craft_discovered_simple([item1, item2])
                if not success: 
                    self.logging.log_experiment_missing_items(needed)
                    return (False, needed)
        
        # Execute Experiment
        self.inventory.remove_item(item1)
        self.inventory.remove_item(item2)

        results = self.recipes.crafts(item1, item2)
        self.inventory.add_items(results)
        self.recipes.add_tried_combination(item1, item2, results)
        for result in results:
            self.recipes.add_discovered_recipe(result, item1, item2)

        self.logging.log_experiment_success(results)
        return (True, results)

    def craft_discovered(self, item, count):
        return self.inventory.craft_discovered_count(item, count)

    def check_server(self):
        success, commands = self.client.receive()
        if success:
            for command in commands:
                args = command.split(' ')
                if args[0] == 'add':
                    self.add_item(args[1], args[2])

    def log_inventory(self):
        self.logging.log_inventory(self.get_inventory_as_string())

    def execute_log(self, log_file_name):
        self.logging.execute_log(log_file_name)