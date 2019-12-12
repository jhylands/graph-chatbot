# Starting off just trying to build a simple repl
import re

class Node:
    def __init__(self, name="", data=None):
        self.outgoing = []
        self.incoming = []
        self.name = name
        self.data = data

    def outgoing(self):
        return self.outgoing

    def incoming(self):
        return self.incoming

    def __repr__(self):
        return self.name

class Edge:
    def __init__(self, start, style, end):
        self.start = start
        start.outgoing.append(self)
        self.style = style
        self.end = end
        end.incoming.append(self)

    def __repr__(self):
        return "({})-[{}]->({})".format(self.start.name , self.style.name, self.end.name)

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
    while response!="exit":
        print("-- %s --"%curr_node)
        if curr_node.outgoing:
            print("# Outgoing")
            print(" - ", "\n - ".join([str(n) for n in curr_node.outgoing]))
        if curr_node.incoming:
            print("# Incoming")
            print(" - ", "\n - ".join([str(n) for n in curr_node.incoming]))
        response = input()
    return context, "bye"

def init_context():
    root = Node("root_node")
    primative = Node("Primitive edge")
    add_rule = Node("add rule", "add rule")
    to_head = Edge(root, primative, add_rule)
    check_next = Node("check next")
    anything = Node("anything", ".*")
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
    response_map = [("graph explore", graph_explore), ("add formatter", add_formatter), ("add rule", add), (".*", anything), ('', context)]
    context = response_map
    while True:
        print(statement)
        response = input()
        context, statement = match_response(context, response)(response_map, response)

main()
