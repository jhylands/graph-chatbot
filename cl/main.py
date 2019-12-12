# Starting off just trying to build a simple repl
import re

class Node:
    outgoing = []
    incoming = []

    def __init__(self, name="", data=None):
        self.name = name
        self.data = data

    def outgoing(self):
        return self.outgoing

    def incoming(self):
        return self.incoming

    def __repr__(self):
        return self.name

class Edge:
    start = None
    style = None
    end = None
    def __init__(self, start, style, end):
        self.start = start
        start.outgoing.append(self)
        self.style = style
        self.end = end
        end.incoming.append(self)

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

def init_context():
    root = Node("root_node")
#    primative = Node("Primitive edge")
#    add_rule = Node("add rule", "add rule")
#    to_head = Edge(root, primative, add_rule)
#    check_next = Node("check next")
#    anything = Node("anything", ".*")
#    check_next_link = Edge(add_rule, check_next, anything)
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
    response_map = [("add rule", add), (".*", anything)]
    context = response_map
    while True:
        print(statement)
        response = input()
        context, statement = match_response(context, response)(response_map, response)

main()
