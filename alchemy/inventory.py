class Inventory:
    """ Class to deal with items and known recipes """

    def __init__(self, controller):
        self.controller = controller
        self.items = {}
        self.known_recipes = []
    
    def has_item(self, item, count=1):
        return item in self.items and self.items[item] >= count

    def has_items(self, items):
        enough_items = [self.has_item(item, items.count(item)) for item in items]
        return all(enough_items)

    def knows_item(self, item):
        return item in self.items

    def add_item(self, item, count=1):
        if item in self.items:
            self.items[item] += count
        else:
            self.items[item] = count
    
    def add_items(self, items):
        for item in items:
            self.add_item(item)

    def remove_item(self, item, count=1):
        if self.has_item(item, count):
            self.items[item] -= count
            return True
        else: return False

    def get_item_names(self):
        return self.items.keys()

    def list_items(self):
        items_list = [''] + sorted([item + ': ' + str(count) for (item, count) in self.items.items()])

        for bitem in reversed(self.controller.get_basic_items()):
            bitemcount = self.items.get(bitem, 0)
            try:
                items_list.remove(bitem + ': ' + str(bitemcount))
            except ValueError:
                pass
            items_list.insert(0, bitem + ': ' + str(bitemcount))

        return '\n'.join(items_list)

    def print_items(self):
        return str(self.items)


    def craft_discovered_to_have(self, items):
        inv_copy = dict(self.items)
        for item in items:
            inv_copy[item] -= 1
        queue = [inv_copy]

        result_inv = self._craft_discovered_from_queue(queue)
        need = list(filter(lambda x: result_inv[x] < 0, result_inv))

        if(len(need) == 0):
            for item in items:
                result_inv[item] += 1
            self.items = result_inv
            return (True, dict())
        else:
            return (False, dict([(item, -result_inv[item]) for item in need]))

    def craft_discovered_count(self, item, count):
        inv_copy = dict(self.items)
        inv_copy[item] = -count # contains the current inventory, but -count of the item we want to craft
        queue = [inv_copy] # keeps copies of inventories, which are possible to craft

        result_inv = self._craft_discovered_from_queue(queue)
        need = list(filter(lambda x: result_inv[x] < 0, result_inv))

        if(len(need) == 0): 
            result_inv[item] += self.items[item]
            result_inv[item] += count
            self.items = result_inv
            return (True, dict())
        else: 
            return (False, dict([(item, -result_inv[item]) for item in need]))
    
    def craft_discovered_list(self, items):
        inv_copy = dict(self.items)
        sitems = set(items)
        for item in sitems:
            inv_copy[item] = 0
        for item in items:
            inv_copy[item] -= 1
        queue = [inv_copy]

        result_inv = self._craft_discovered_from_queue(queue)
        need = list(filter(lambda x: result_inv[x] < 0, result_inv))

        if(len(need) == 0):
            for item in sitems:
                result_inv[item] += self.items[item]
            for item in items:
                result_inv[item] += 1
            self.items = result_inv
            return (True, dict())
        else:
            return (False, dict([(item, -result_inv[item]) for item in need]))

    ''' Given a queue of intermediate copies of inventory, tries to craft things using discovered recipes so that the copy of inventory is viable'''
    def _craft_discovered_from_queue(self, queue):
        number_newly_added_recipes = 1
        while number_newly_added_recipes > 0 and len(queue) < 10000:
            working_inv = queue.pop(0)
            need = list(filter(lambda x: working_inv[x] < 0, working_inv))

            number_newly_added_recipes = 0
            for need_item in need:
                need_count = -working_inv[need_item]

                possible_recipes = self.controller.recipes.get_discovered_recipes(need_item)
                number_newly_added_recipes += len(possible_recipes)

                for (ingredient1, ingredient2) in possible_recipes:
                    new_inv_copy = dict(working_inv)
                    new_inv_copy[need_item] += need_count
                    new_inv_copy[ingredient1] -= need_count
                    new_inv_copy[ingredient2] -= need_count
                    queue.append(new_inv_copy)

        return working_inv

    def craft_discovered_simple(self, items):
        inv_copy = dict(self.items)
        for item in items:
            inv_copy[item] -= 1

        finished = False
        while not finished:
            finished = True
            need = list(filter(lambda x: inv_copy[x] < 0, inv_copy))

            for item in need:
                possible_recipes = self.controller.recipes.get_discovered_recipes(item)
                if possible_recipes:
                    finished = False
                    (ingredient1, ingredient2) = possible_recipes[0]
                    need_count = -inv_copy[item]
                    inv_copy[item] += need_count
                    inv_copy[ingredient1] -= need_count
                    inv_copy[ingredient2] -= need_count


        need = list(filter(lambda x: inv_copy[x] < 0, inv_copy))

        if(len(need) == 0):
            for item in items:
                inv_copy[item] += 1
            self.items = inv_copy
            return (True, dict())
        else:
            return (False, dict([(item, -inv_copy[item]) for item in need]))

