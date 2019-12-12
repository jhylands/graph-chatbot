# Starting off just trying to build a simple repl

def handle(response):
    return "You said %s"%response

def main():
    statement = "Welcome to LIRA"
    while True:
        print(statement)
        response = input()
        statement = handle(response)

main()
