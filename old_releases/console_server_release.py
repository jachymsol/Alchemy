from alchemy.server import Server

""" This release implements console GUI based on text inputs. """

def connect(server):
    result, team_name = server.connect_new()
    print("Successfully connected team " + team_name)

def add(server, args): 
    if len(args) >= 2:
        conn_no = args[0]
        item = args[1]
        if len(args) >= 3 and args[2]:
            count = args[2] 
        else:
            count = '1' 
        
        data = ' '.join(['add', item, count, '\n'])
        server.send(int(conn_no), bytes(data, 'utf-8'))
        print("Sent", data, end='')
    else: helptext()

def helptext(*args):
    print("The available commands are:")
    print("Connect - connects a new team")
    print("Add <client_no> <item> <count> - adds an item to your inventory")
    print("Help - prints this text")
    print("Quit - quits the game")


def main():
    print("Welcome. This is Alchemy Server version 0.0.1. For a list of possible inputs, type Help.")

    exited = False

    server = Server()
    print("Server successfully started.")

    while not exited:
        print("> ", end="")
        sep_input = input().lower().split(" ")
        command = sep_input[0]
        args = sep_input[1:]
        
        if command in ["c", "connect"]:
            connect(server)
        elif command in ["a", "add"]:
            add(server, args)
        elif command in ["exit", "e", "quit", "q"]: 
            exited = True
        else:
            helptext()

    server.close_all()
    print("Thank you for testing!")

if __name__ == "__main__":
    main()