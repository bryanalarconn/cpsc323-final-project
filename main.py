import re
# Parsing table as a dictionary
parsing_table = {
    'P': {
        'program': ['program', 'I', ';', 'var', 'D', ':', 'T', ';', 'begin', 'S', 'end']
    },
    'I': {
        'a': ['L', 'H'], 'b': ['L', 'H'], 'r': ['L', 'H'], 's': ['L', 'H']
    },
    'H': {
        'a': ['L', 'H'], 'b': ['L', 'H'], 'r': ['L', 'H'], 's': ['L', 'H'],
        '0': ['D', 'H'], '1': ['D', 'H'], '2': ['D', 'H'], '3': ['D', 'H'], '4': ['D', 'H'],
        '5': ['D', 'H'], '6': ['D', 'H'], '7': ['D', 'H'], '8': ['D', 'H'], '9': ['D', 'H'],
        '=': [], ';': [], ')': [], '+': [], '-': [], '*': [], '/': [], ',': []
    },
    'X': {
        'a': ['Y', ':', 'Z'], 'b': ['Y', ':', 'Z'], 'r': ['Y', ':', 'Z'], 's': ['Y', ':', 'Z']
    },
    'Y': {
        'a': ['I', ',', 'Y'], 'b': ['I', ',', 'Y'], 'r': ['I', ',', 'Y'], 's': ['I', ',', 'Y']
    },
    'Z': {
        'integer': ['integer']
    },
    'B' : {
        'show': ['C', 'K'],
        'a': ['C', 'K'], 'b': ['C', 'K'], 'r': ['C', 'K'], 's': ['C', 'K'],
        'end': []
    },
    'K': {
        'show': ['C', 'K'],
        'a': ['C', 'K'], 'b': ['C', 'K'], 'r': ['C', 'K'], 's': ['C', 'K'],
        'end': []
    },
    'C' : {
        'show': ['W'],
        'a': ['A'], 'b': ['A'], 'r': ['A'], 's': ['A']
    },
    'W' : {
        'show' : ['show', '(', 'G', 'I', ')', ';']
    },
    'G' : {
        '"value="' : ['"value="', ','],
        'a': [], 'b': [], 'r': [], 's': []
    },
    'A' : {
        'a': ['I', '=', 'E', ';'], 'b': ['I', '=', 'E', ';'], 'r': ['I', '=', 'E', ';'], 's': ['I', '=', 'E', ';']
    },
    'E': {
        'a': ['T', 'Q'], 'b': ['T', 'Q'], 'r': ['T', 'Q'], 's': ['T', 'Q'],
        '0': ['T', 'Q'], '1': ['T', 'Q'], '2': ['T', 'Q'], '3': ['T', 'Q'], '4': ['T', 'Q'],
        '5': ['T', 'Q'], '6': ['T', 'Q'], '7': ['T', 'Q'], '8': ['T', 'Q'], '9': ['T', 'Q'],
        '+': ['T', 'Q'], '-': ['T', 'Q'], '(': ['T', 'Q'],
    },
    'Q': {
        '+': ['+', 'T', 'Q'], '-': ['-', 'T', 'Q'], ';': [], ')': []
    },
    'T': {
        'a': ['F', 'R'], 'b': ['F', 'R'], 'r': ['F', 'R'], 's': ['F', 'R'],
        '0': ['F', 'R'], '1': ['F', 'R'], '2': ['F', 'R'], '3': ['F', 'R'], '4': ['F', 'R'],
        '5': ['F', 'R'], '6': ['F', 'R'], '7': ['F', 'R'], '8': ['F', 'R'], '9': ['F', 'R'],
        '+': ['F', 'R'], '-': ['F', 'R'], '(': ['F', 'R'],
    },
    'R': {
        '*': ['*', 'F', 'R'], '/': ['/', 'F', 'R'], '+': [], '-': [], ')': [], ';': [],
    },
    'F': {
        'a': ['I'], 'b': ['I'], 'r': ['I'], 's': ['I'],
        '0': ['N'], '1': ['N'], '2': ['N'], '3': ['N'], '4': ['N'],
        '5': ['N'], '6': ['N'], '7': ['N'], '8': ['N'], '9': ['N'],
        '+': ['N'], '-': ['N'],
        '(': ['(', 'E', ')'],
    },
    'N' : {
        '0': ['S', 'D', 'V'], '1': ['S', 'D', 'V'], '2': ['S', 'D', 'V'], '3': ['S', 'D', 'V'], '4': ['S', 'D', 'V'],
        '5': ['S', 'D', 'V'], '6': ['S', 'D', 'V'], '7': ['S', 'D', 'V'], '8': ['S', 'D', 'V'], '9': ['S', 'D', 'V'],
        '+': ['S', 'D', 'V'], '-': ['S', 'D', 'V']
    },
    'V' : {
        '0': ['D', 'V'], '1': ['D', 'V'], '2': ['D', 'V'], '3': ['D', 'V'], '4': ['D', 'V'],
        '5': ['D', 'V'], '6': ['D', 'V'], '7': ['D', 'V'], '8': ['D', 'V'], '9': ['D', 'V'],
        '+': [], '-': [], '*': [], '/': [], '=': [], ';': [], ')': [], ',': []
    },
    'S' : {
        '+' : {'+'}, '-' : {'-'},
        '0': [], '1': [], '2': [], '3': [], '4': [],
        '5': [], '6': [], '7': [], '8': [], '9': [],
    },
    'D'  : {
        '0': ['0'], '1': ['1'], '2': ['2'], '3': ['3'], '4': ['4'],
        '5': ['5'], '6': ['6'], '7': ['7'], '8': ['8'], '9': ['9']
    },
    'L' : {
        'a' : ['a'], 'b' : ['b'], 'r' : ['r'], 's' : ['s']
    }
}

# Terminals
terminals = [
  '+', '-', '*', '/', '=', ';', ':', ',', '(', ')', '"value="',
  'program', 'var', 'integer', 'begin', 'end', 'show',
  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
  'a', 'b', 'r', 's',
  '$'
]

def tokenize(filename):
    # Matches identifiers, numbers, keywords, strings, or symbols
    token_pattern = r'"value="' + r'|:=|==|!=|[a-zA-Z_][a-zA-Z0-9_]*|\d+|[+\-*/=;:(),]'

    tokens = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue






def parse(input_string):
    stack = ['$', 'P']
    pointer = 0

    print(f"{'Stack':<30} {'Input':<30} {'Action'}")
    print('-' * 80)

    while stack:
        top = stack[-1] # Top of the stack
        current_input = input_string[pointer] # Reads the current char in the input

        print(f"{''.join(stack):<30} {input_string[pointer:]:<30}", end=' ')

        if top == current_input == '$':
            print("ACCEPTED")
            return True

        if top in terminals:
            if top == current_input: # Checking if the input is in the terminal chars
                stack.pop()
                pointer += 1
                print(f"'{top}'")
            else:
                print(f"ERROR: expected '{top}', found '{current_input}'")
                return False
        else:
            rule = parsing_table.get(top, {}).get(current_input) # Retrieving the correct column based on current input char
            if rule is not None:
                stack.pop()
                if rule:  # Not lambda
                    for symbol in reversed(rule):
                        stack.append(symbol)
                    print(f"{top} -> {' '.join(rule)}")
                else:
                    print(f"{top} -> λ")
            else:
                print(f"ERROR: no rule for ({top}, {current_input})")
                return False
    return False

# Test expressions
test_cases = [
    "(a+a)*a$",
    "i*(i+i)$",
    "i(i+i)$"
]

for expr in test_cases:
    print(f"\nParsing: {expr}")
    parse(expr)
