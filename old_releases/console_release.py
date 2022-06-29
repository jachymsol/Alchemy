from alchemy.controller import Controller

""" This release implements console GUI based on text inputs. """

def inventory(controller, args):
    print("You have: ", controller.print_inventory())

def import_recipes(controller, args):
    if len(args) >= 1:
        file_name = args[0]
        controller.import_recipes(file_name)
    else: helptext()

def add(controller, args): #TODO: any order of arguments should be possible
    if len(args) >= 1:
        item = args[0]
        if len(args) >= 2 and args[1]:
            count = int(args[1]) 
        else:
            count = 1 
        controller.add_item(item, count)
        print("Added", count, "of", item)
    else: helptext()

def craft(controller, args):
    if len(args) >= 2:
        item1 = args[0]
        item2 = args[1]
        success, result = controller.experiment(item1, item2)
        if success: 
            print("You crafted: ", result)
        else: 
            print("You don't have these items")
    else: helptext()

def make(controller, args): 
    if len(args) >= 1:
        item = args[0]
        if len(args) >= 2 and args[1]:
            count = int(args[1])
        else:
            count = 1
        success, missing = controller.craft_discovered(item, count)
        if success:
            print("Successfully made")
        else:
            print("Missing items: " + str(missing))
    else: helptext()

def helptext(*args):
    print("The available commands are:")
    print("Import <file_name> - imports recipes from a text file")
    print("Inventory - prints what items you currently have")
    print("Add <item> <count> - adds an item to your inventory")
    print("Craft <item1> <item2> - tries crafting item1 and item2, consumes both items regardless of result")
    print("Make <item> <count> - makes an item you already know how to craft, provided you have the necessary ingredients")
    print("Help - prints this text")
    print("Quit - quits the game")


def main():
    print("Welcome. This is Alchemy version 0.2.1. For a list of possible inputs, type Help.")
    exited = False

    controller = Controller()

    while not exited:
        print("> ", end="")
        sep_input = input().lower().split(" ")
        command = sep_input[0]
        args = sep_input[1:]
        
        addresses = {
            "print": inventory,
            "p": inventory,
            "inventory": inventory,
            "inv": inventory,
            "import": import_recipes,
            "add": add,
            "a": add,
            "craft": craft,
            "c": craft,
            "make": make,
            "m": make
        }

        if command in ["exit", "e", "quit", "q"]: exited = True
        else:
            addresses.get(command, helptext)(controller, args)
    
    print("Thank you for testing!")

if __name__ == "__main__":
    main()