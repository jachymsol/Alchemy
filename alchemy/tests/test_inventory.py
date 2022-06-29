import unittest
from ..inventory import Inventory

class TestInventory(unittest.TestCase):
    """ Test for the Inventory class and its methods """

    def setUp(self):
        self.inv = Inventory(None)
    
    def test_empty_on_load(self):
        self.assertEqual(self.inv.items, {})
    
    def test_add_item(self):
        self.inv.add_item("stone")
        self.assertEqual(self.inv.items["stone"], 1)
    
    def test_add_item_multiple(self):
        self.inv.add_item("stone", 3)
        self.assertEqual(self.inv.items["stone"], 3)

    def test_add_items(self):
        self.inv.add_items(["stone", "fire", "stone"])
        self.assertEqual(self.inv.items["stone"], 2)
    
    def test_has_item_successful(self):
        self.inv.add_item("stone")
        self.assertTrue(self.inv.has_item("stone"))
    
    def test_has_item_more_than_has(self):
        self.inv.add_item("stone", 2)
        self.assertFalse(self.inv.has_item("stone", 3))
    
    def test_has_item_not_added(self):
        self.inv.add_item("stone")
        self.assertFalse(self.inv.has_item("fire"))

    def test_remove_item_successful_returns(self):
        self.inv.add_item("stone", 3)
        self.assertTrue(self.inv.remove_item("stone", 2))
    
    def test_remove_item_successful_result(self):
        self.inv.add_item("stone", 3)
        self.inv.remove_item("stone", 2)
        self.assertEqual(self.inv.items["stone"], 1)
    
    def test_remove_item_too_many_returns(self):
        self.inv.add_item("stone", 3)
        self.assertFalse(self.inv.remove_item("stone", 4))
    
    def test_remove_item_too_many_result(self):
        self.inv.add_item("stone", 3)
        self.inv.remove_item("stone", 4)
        self.assertEqual(self.inv.items["stone"], 3)
    
    def test_remove_item_not_present_returns(self):
        self.inv.add_item("stone")
        self.assertFalse(self.inv.remove_item("fire"))

    def test_remove_item_not_present_result(self):
        self.inv.add_item("stone")
        self.inv.remove_item("fire")
        self.assertFalse(self.inv.has_item("fire"))

    def test_has_items_empty(self):
        self.inv.add_item("stone", 3)
        self.inv.add_item("fire")
        self.assertTrue(self.inv.has_items([]))
    
    def test_has_items_successful(self):
        self.inv.add_item("stone", 3)
        self.inv.add_item("fire")
        self.assertTrue(self.inv.has_items(["stone", "fire", "stone"]))
    
    def test_has_items_too_many_of_one(self):
        self.inv.add_item("stone", 3)
        self.inv.add_item("fire")
        self.assertFalse(self.inv.has_items(["stone", "stone", "stone", "stone"]))
    
    def test_has_items_one_not_present(self):
        self.inv.add_item("stone", 3)
        self.inv.add_item("fire")
        self.assertFalse(self.inv.has_items(["stone", "fire", "stone", "earth"]))
    
    def test_print_items(self):
        self.inv.add_item("stone", 3)
        self.inv.add_item("fire")
        self.inv.add_item("earth")
        self.inv.remove_item("earth")
        self.assertEqual(self.inv.print_items(), "{'stone': 3, 'fire': 1, 'earth': 0}")

