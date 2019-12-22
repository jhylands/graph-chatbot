# Starting off just trying to build a simple repl
import re
import pickle
from graph import Node, Edge


def save(context, more):
    root = context[-1][-1]
    print("Saving")
    curr_node = root
    node_list = curr_node.global_ref
    with open("database.pkl", "wb") as f:
        pickle.dump(node_list, f)
    return context, "saved"

def load(context, more):
    with open("database.pkl", "rb") as f:
        save_file = pickle.load(f)
    print("Loading")
    context[-1] = ('', save_file[0])
    return context, "loaded {} items".format(len(save_file))
    
        

def anything(context, response):
    return context , "You said %s"%response
        
def add(context, response):
    print("Please enter the regex to check against:")
    response = input()
    print("Given the command what should I respond?")
    new_response = input()
    new_command = lambda context, response: (context, new_response)
    context.insert(0, (response, new_command))
    return context, "%s, added!"%response

def add_formatter(context, response):
    print("Please enter the regex to check against:")
    regex = input()
    print("Given the command what should I respond?")
    new_response = input()
    def new_command(context, response):
        m = re.match(regex, response)
        if m:
            return context, new_response.format(*m.groups())
        else:
            return context, "REGEX ERROR"
    context.insert(0, (regex, new_command))
    return context, "%s, added!"%response

def graph_explore(context, response):
    root = context[-1][-1]
    print("Welcome to graph explore!")
    curr_node = root
    node_list = curr_node.global_ref
    commands = {
        "(\d+)": "goto",
        "add node (\w+)": "add node with name",
        "add edge\s?\((\d+)\)-[(d+)]->\((\d+)\)": "add edge, (node1)-[edge]->(node2)"
    }
    while response!="exit":
        print(node_list)
        print("Instructions")
        for key, value in commands.items():
            print(key, ":", value)
        print("-- %s --"%curr_node)
        if curr_node.outgoing:
            print("# Outgoing")
            print(" - ", "\n - ".join(map(str, curr_node.outgoing)))
        if curr_node.incoming:
            print("# Incoming")
            print(" - ", "\n - ".join(map(str, curr_node.incoming)))
        response = input()
#        for key, function in commands.items():
#        match = re.match(key, response)
        match = re.match("edges", response)
        if match:
            print("# Edges")
            print(" - ", "\n - ".join(map(str, curr_node.edges)))
            
        match = re.match("(\d+)", response)
        if match:
            curr_node = node_list[int(match.group(1))]
        match = re.match("add node (\w+)", response)
        if match:
            #Now we are in an adding node state.
            name = match.group(1)
            curr_node = Node(node_list, name)
            print("Node: {} added with id {}".format(name, curr_node.get_index()))
#        match = re.match("add edge\s?\((\d+)\)-[(d+)]->\((\d+)\)", response)
        match = re.match("add edge (\d+) (\d+) (\d+)", response)
        if match:
            # Simply declaring the edge should add it to the node lists
            # So it doesn't need to be added to another list like the node
            # had to be.
            print("adding edge")
            Edge(node_list[int(match.group(1))], node_list[int(match.group(2))], node_list[int(match.group(3))])
            
    return context, "bye"

def init_context():
    node_list = []
    root = Node(node_list, "root_node")
    primative = Node(node_list, "Primitive edge")
    add_rule = Node(node_list, "add rule", "add rule")
    to_head = Edge(root, primative, add_rule)
    check_next = Node(node_list, "check next")
    anything = Node(node_list, "anything", ".*")
    check_next_link = Edge(add_rule, check_next, anything)
    return root

# I guess this will eventually take context as well
def match_response(response_map, response):
    matches = [function for regex, function in response_map if re.match(regex, response)]
    if len(matches)>1:
        print("More than one regex matched!")
    else:
        #Currently assuming left priority
        pass
    return matches[0]

def main():
    statement = "Welcome to LIRA"
    context = init_context()
    response_map = [("save", save), ("load", load), ("graph explore", graph_explore), ("add formatter", add_formatter), ("add rule", add), (".*", anything), ('', context)]
    context = response_map
    while True:
        print(statement)
        response = input()
        context, statement = match_response(context, response)(response_map, response)

if __name__=="__main__":
    main()
