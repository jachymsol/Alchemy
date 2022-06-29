import time

class Logging:
    """
        This class logs what actions have been made during the game
    """

    def __init__(self, controller, team_name, verbose=False):
        self.controller = controller
        self.name = "Log " + time.strftime("%Y-%m-%d %H-%M-%S") + ".txt"
        self.verbose = verbose

        log_file = open(self.name, 'w')
        print(time.strftime("%Y-%m-%d %H:%M:%S") + ": Starting session " + self.name + " for team " + team_name, file=log_file)
        log_file.close()

    def log_inventory(self, inventory_as_string):
        message = "Inventory: " + inventory_as_string
        self._log_message(message)
    
    def log_imported_recipes(self, file_name):
        message = "Imported recipes from " + file_name
        self._log_message(message)

    def log_added_item(self, item, count):
        if self.verbose:
            message = "Added " + str(count) + " of " + item
        else:
            message = "add " + item + " " + str(count)
        self._log_message(message)
    
    def log_experiment_start(self, item1, item2):
        if self.verbose:
            message = "Started an experiment with " + item1 + ", " + item2
        else: 
            message = "craft " + item1 + " " + item2
        self._log_message(message)

    def log_experiment_unknown_items(self):
        if self.verbose:
            message = "Some items were not recognized"
            self._log_message(message)
    
    def log_experiment_missing_items(self, missing):
        if self.verbose:
            message = "Missing items: " + ", ".join([miss_item + ': ' + str(miss_count) for (miss_item, miss_count) in missing.items()])
            self._log_message(message)

    def log_experiment_success(self, result):
        if self.verbose:
            message = "Successfully crafted: " + ", ".join(result)
            self._log_message(message)


    def _log_message(self, message):
        log_file = open(self.name, 'a')
        print(time.strftime("%Y-%m-%d %H:%M:%S") + ": " + message, file=log_file)
        log_file.close()


    def execute_log(self, log_file_name):
        addresses = {
            "import": self.controller.import_recipes,
            "add": self.controller.add_item,
            "craft": self.controller.experiment,
            "make": self.controller.craft_discovered,
        }

        lines = self.read_log(log_file_name)
        for line in lines:
            words = line.rstrip('\n').split(' ')
            command = words[0]
            args = words[1:]
            addresses.get(command, self.empty_fun)(*args)
    
    def read_log(self, log_file_name):
        log_file = open(log_file_name, 'r')
        lines = log_file.readlines()
        lines = [line[21:] for line in lines]
        log_file.close()

        return lines

    def empty_fun(self, *args):
        pass