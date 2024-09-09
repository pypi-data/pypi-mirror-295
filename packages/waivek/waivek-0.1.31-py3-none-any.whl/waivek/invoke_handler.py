from waivek.error2 import handler

def foo():
    import json
    string = 'abcd'
    json.loads(string)
    raise Exception("invoke_handler.py: foo()")

def main():
    foo()

with handler():
    main()
