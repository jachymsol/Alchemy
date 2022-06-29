import unittest
from ..recipes import Recipes

class TestRecipes(unittest.TestCase):
    """ Test for the Recipes class and its methods """

    def setUp(self):
        self.recipes = Recipes(None)
        self.test_recipes_text = 'fire = stone + stone\nwater = fire + stone\nfire = water + ash\nash = fire + stone'

    def test_add_official_recipe_new(self):
        self.recipes._add_official_recipe('fire', ('stone', 'stone'))
        
        expected = { ('stone', 'stone'): ['fire'] }
        actual = self.recipes.recipes
        self.assertDictEqual(expected, actual)

    def test_add_official_recipe_append(self):
        self.recipes._add_official_recipe('water', ('fire', 'stone'))
        self.recipes._add_official_recipe('ash', ('fire', 'stone'))

        expected = { ('fire', 'stone'): ['water', 'ash'] }
        actual = self.recipes.recipes
        self.assertDictEqual(expected, actual)

    def test_import_from_text(self):
        self.recipes._import_from_text(self.test_recipes_text)

        expected = {
            ('stone', 'stone'): ['fire'],
            ('fire', 'stone'): ['water', 'ash'],
            ('ash', 'water'): ['fire']
        }
        actual = self.recipes.recipes
        self.assertDictEqual(expected, actual)
    
    def test_order_items_correct_order(self):
        expected = ('a', 'b')
        actual = self.recipes._order_items('a', 'b')
        self.assertTupleEqual(expected, actual)

    def test_order_items_wrong_order(self):
        expected = ('a', 'b')
        actual = self.recipes._order_items('b', 'a')
        self.assertTupleEqual(expected, actual)

    def test_order_items_equal(self):
        expected = ('a', 'a')
        actual = self.recipes._order_items('a', 'a')
        self.assertTupleEqual(expected, actual)

    def test_crafts_stuff(self):
        self.recipes._import_from_text(self.test_recipes_text)

        expected = ['water', 'ash']
        actual = self.recipes.crafts('fire', 'stone')
        self.assertListEqual(expected, actual)

    def test_crafts_reverse_order(self):
        self.recipes._import_from_text(self.test_recipes_text)

        expected = ['fire']
        actual = self.recipes.crafts('water', 'ash')
        self.assertListEqual(expected, actual)

    def test_crafts_nothing(self):
        self.recipes._import_from_text(self.test_recipes_text)
        
        expected = []
        actual = self.recipes.crafts('water', 'stone')
        self.assertListEqual(expected, actual)
    
    def test_add_discovered_recipe_new(self):
        self.recipes.add_discovered_recipe('fire', 'stone', 'stone')
        
        expected = { 'fire': [('stone', 'stone')] }
        actual = self.recipes.discovered_recipes
        self.assertDictEqual(expected, actual)

    def test_add_discovered_recipe_append(self):
        self.recipes.add_discovered_recipe('fire', 'stone', 'stone')
        self.recipes.add_discovered_recipe('fire', 'ash', 'water')

        expected = { 'fire': [('stone', 'stone'), ('ash', 'water')] }
        actual = self.recipes.discovered_recipes
        self.assertDictEqual(expected, actual)

    def test_get_discovered_recipes_multiple(self):
        self.recipes.add_discovered_recipe('fire', 'stone', 'stone')
        self.recipes.add_discovered_recipe('fire', 'ash', 'water')

        expected = [('stone', 'stone'), ('ash', 'water')]
        actual = self.recipes.get_discovered_recipes('fire')
        self.assertListEqual(expected, actual)

    def test_get_dicovered_recipes_none(self):
        expected = []
        actual = self.recipes.get_discovered_recipes('stone')
        self.assertListEqual(expected, actual)