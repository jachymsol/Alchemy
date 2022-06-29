class Recipes:
    """ 
        This class handles official and discovered recipes.
    """

    def __init__(self, controller, recipes_file=None):
        self.controller = controller
        self.recipes = dict()
        if recipes_file: 
            self.import_from_file(recipes_file)
        self.discovered_recipes = dict()
        self.tried_combinations = dict()

    def _add_official_recipe(self, result, ingredients):
        """ Adds a new recipe to official recipes. Result is a string and ingredients are a pair (tuple) of strings. """

        self.recipes[ingredients] = self.recipes.get(ingredients, []) + [result]

    def import_from_file(self, recipes_file_name):
        """ Imports recipes from a file. Each recipe should be in 'result=item1+item2' format. """
        """ TODO: Extract out to a separate class """

        with open(recipes_file_name) as recipes_file:
            self._import_from_text(recipes_file.read())

    def _import_from_text(self, recipes_text):
        """ Imports recipes from text. Each recipe should be in 'result = item1 + item2' format. """

        recipes_file = recipes_text.split('\n')
        recipes_lines = [line.split(' = ') for line in recipes_file]
        recipes_tuples = [(result, (min(ingredients.split(' + ')), max(ingredients.split(' + ')))) for [result, ingredients] in recipes_lines]

        for (result, ingredients) in recipes_tuples:
            self._add_official_recipe(result, ingredients)
    

    def _order_items(self, item1, item2):
        return (min(item1, item2), max(item1, item2))

    
    def crafts(self, item1, item2):
        """ Returns the results of crafting item1 with item2. """

        ingredients = self._order_items(item1, item2)
        return self.recipes.get(ingredients, [])
    

    def add_discovered_recipe(self, result, item1, item2):
        """ Adds a discovered recipe to the set of discovered recipes. """

        ingredients = self._order_items(item1, item2)
        self.discovered_recipes[result] = self.discovered_recipes.get(result, []) + [ingredients]
    
    def get_discovered_recipes(self, item):
        """ Returns the discovered recipes for item. """

        return self.discovered_recipes.get(item, [])


    def add_tried_combination(self, item1, item2, results):
        """ Adds a tried combination to the set of tried combinations. """

        ingredients = self._order_items(item1, item2)
        self.tried_combinations[ingredients] = results
    
    def get_tried_combinations(self):
        """ Returns a sorted copy of to the set of tried combinations. """

        return sorted([item1 + ' + ' + item2 + ' = ' + ', '.join(results) for ((item1, item2), results) in self.tried_combinations.items()])