# Starting off just trying to build a simple repl
import re

class Node:
    def __init__(self, name=""):
        self.name = name

    def __repr__(self):
        return self.name

class Edge:
    start = None
    style = None
    end = None
    def __init__(self, start, style, end):
        self.start = start
        self.style = style
        self.end = end

def anything(context, response):
    if response=="add handle":
        context = "ADD"
        return context, "Please enter the pattern to match:"
    else:
        return context , "You said %s"%response
        
def add(context, response):
    return "ANYTHING", "Given the command what should I respond?"
    
handlers = {"ANYTHING": anything, "ADD": add}
def handle(context, response):
    
    return handlers[context](context, response)

def init_context():
    root = Node("root_node")
    return root

# I guess this will eventually take context as well
def match_response(response_map, response):
    matches = [function for regex, function in response_map if re.match(regex, response)]
    if len(matches)>1:
        print("More than one regex matched!")
    else:
        return matches[0]

def main():
    statement = "Welcome to LIRA"
    context = init_context()
    response_map = [(".*", anything)]
    while True:
        print(statement)
        response = input()
        context, statement = match_response(response_map, response)(context, response)

main()
