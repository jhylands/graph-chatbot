# Starting off just trying to build a simple repl

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

def main():
    statement = "Welcome to LIRA"
    context = "ANYTHING"
    while True:
        print(statement)
        response = input()
        context, statement = handle(context, response)

main()
