#!/usr/bin/env python3
# Hello World for Python debugger test

def make_greeting(name: str) -> str:
    greeting = f"Hello, {name}!"
    return greeting

def main() -> None:
    name = "World"
    greeting = make_greeting(name)  # set breakpoint here to inspect 'name' and 'greeting'
    print(greeting)

    # small computation to step through
    total = 0
    for i in range(5):
        total += i  # step into/over here
    print("Sum 0..4 =", total)

if __name__ == "__main__":
    main()