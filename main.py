import re
# Parsing table as a dictionary
parsing_table = {
    # <prog>
    # P -> program
    'P': {
        'program': ['program', 'I', ';', 'var', 'X', 'begin', 'B', 'end']
    },
    # <identifier>
    # I -> LH
    'I': {
        'a': ['L', 'H'], 'b': ['L', 'H'], 'r': ['L', 'H'], 's': ['L', 'H']
    },
    # <post-identifier>
    # H -> LH
    # H -> DH
    # H -> λ
    'H': {
        'a': ['L', 'H'], 'b': ['L', 'H'], 'r': ['L', 'H'], 's': ['L', 'H'],
        '0': ['D', 'H'], '1': ['D', 'H'], '2': ['D', 'H'], '3': ['D', 'H'], '4': ['D', 'H'],
        '5': ['D', 'H'], '6': ['D', 'H'], '7': ['D', 'H'], '8': ['D', 'H'], '9': ['D', 'H'],
        '=': [], ';': [], ')': [], '+': [], '-': [], '*': [], '/': [], ',': [], ':' : []
    },
    # <dec-list>
    # X -> Y:Z;
    'X': {
        'a': ['Y', ':', 'Z',';'], 'b': ['Y', ':', 'Z',';'], 'r': ['Y', ':', 'Z',';'], 's': ['Y', ':', 'Z',';']
    },
    # <dec>
    # X -> I,Y
    'Y': {
        'a' : ['I', 'J'], 'b' : ['I', 'J'], 'r' : ['I', 'J'], 's' : ['I', 'J']
    },
    # <post-dec>
    # J -> ,YJ
    # J -> λ
    'J': {
        ',' : [',','Y','J'],
        ':' : []
    },
    # <type>
    # Z -> integer
    'Z': {
        'integer': ['integer']
    },
    # <stat-list>
    # B -> CK
    # B -> λ
    'B' : {
        'show': ['C', 'K'],
        'a': ['C', 'K'], 'b': ['C', 'K'], 'r': ['C', 'K'], 's': ['C', 'K'],
        'end': []
    },
    # <post-stat-list>
    # K -> CK
    # K -> λ
    'K': {
        'show': ['C', 'K'],
        'a': ['C', 'K'], 'b': ['C', 'K'], 'r': ['C', 'K'], 's': ['C', 'K'],
        'end': []
    },
    # <stat>
    # C -> W
    # C -> A
    'C' : {
        'show': ['W'],
        'a': ['A'], 'b': ['A'], 'r': ['A'], 's': ['A']
    },
    # <write>
    # W -> show(GI);
    'W' : {
        'show' : ['show', '(', 'G', 'I', ')', ';']
    },
    # <str>
    # G -> "value=",
    # G -> λ
    'G' : {
        '“value=”,' : ['“value=”,'],
        'a': [], 'b': [], 'r': [], 's': []
    },
    # <assign>
    # A -> I=E;
    'A' : {
        'a': ['I', '=', 'E', ';'], 'b': ['I', '=', 'E', ';'], 'r': ['I', '=', 'E', ';'], 's': ['I', '=', 'E', ';']
    },
    #<expr>
    # E -> TQ
    'E': {
        'a': ['T', 'Q'], 'b': ['T', 'Q'], 'r': ['T', 'Q'], 's': ['T', 'Q'],
        '0': ['T', 'Q'], '1': ['T', 'Q'], '2': ['T', 'Q'], '3': ['T', 'Q'], '4': ['T', 'Q'],
        '5': ['T', 'Q'], '6': ['T', 'Q'], '7': ['T', 'Q'], '8': ['T', 'Q'], '9': ['T', 'Q'],
        '+': ['T', 'Q'], '-': ['T', 'Q'], '(': ['T', 'Q'],
    },
    # <expr-prime>
    # Q -> +TQ
    # Q -> -TQ
    # Q -> λ
    'Q': {
        '+': ['+', 'T', 'Q'], '-': ['-', 'T', 'Q'], ';': [], ')': []
    },
    # <term>
    # T -> FR
    'T': {
        'a': ['F', 'R'], 'b': ['F', 'R'], 'r': ['F', 'R'], 's': ['F', 'R'],
        '0': ['F', 'R'], '1': ['F', 'R'], '2': ['F', 'R'], '3': ['F', 'R'], '4': ['F', 'R'],
        '5': ['F', 'R'], '6': ['F', 'R'], '7': ['F', 'R'], '8': ['F', 'R'], '9': ['F', 'R'],
        '+': ['F', 'R'], '-': ['F', 'R'], '(': ['F', 'R'],
    },
    # <term-prime>
    # R -> *FR
    # R -> /FR
    # R -> λ
    'R': {
        '*': ['*', 'F', 'R'], '/': ['/', 'F', 'R'], '+': [], '-': [], ')': [], ';': [],
    },
    # <factor>
    # F -> I
    # F -> N
    # F -> (E)
    'F': {
        'a': ['I'], 'b': ['I'], 'r': ['I'], 's': ['I'],
        '0': ['N'], '1': ['N'], '2': ['N'], '3': ['N'], '4': ['N'],
        '5': ['N'], '6': ['N'], '7': ['N'], '8': ['N'], '9': ['N'],
        '+': ['N'], '-': ['N'],
        '(': ['(', 'E', ')'],
    },
    # <number>
    # N -> SDV
    'N' : {
        '0': ['S', 'D', 'V'], '1': ['S', 'D', 'V'], '2': ['S', 'D', 'V'], '3': ['S', 'D', 'V'], '4': ['S', 'D', 'V'],
        '5': ['S', 'D', 'V'], '6': ['S', 'D', 'V'], '7': ['S', 'D', 'V'], '8': ['S', 'D', 'V'], '9': ['S', 'D', 'V'],
        '+': ['S', 'D', 'V'], '-': ['S', 'D', 'V']
    },
    # <post-number>
    # V -> dv
    # V -> λ
    'V' : {
        '0': ['D', 'V'], '1': ['D', 'V'], '2': ['D', 'V'], '3': ['D', 'V'], '4': ['D', 'V'],
        '5': ['D', 'V'], '6': ['D', 'V'], '7': ['D', 'V'], '8': ['D', 'V'], '9': ['D', 'V'],
        '+': [], '-': [], '*': [], '/': [], '=': [], ';': [], ')': [], ',': []
    },
    # <sign>
    # S -> +
    # s -> -
    # S -> λ
    'S' : {
        '+' : {'+'}, '-' : {'-'},
        '0': [], '1': [], '2': [], '3': [], '4': [],
        '5': [], '6': [], '7': [], '8': [], '9': [],
    },
    # <digit>
    # D -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
    'D'  : {
        '0': ['0'], '1': ['1'], '2': ['2'], '3': ['3'], '4': ['4'],
        '5': ['5'], '6': ['6'], '7': ['7'], '8': ['8'], '9': ['9']
    },
    #<letter>
    # L -> a | b | r | s
    'L' : {
        'a' : ['a'], 'b' : ['b'], 'r' : ['r'], 's' : ['s']
    }
}

# Terminals
terminals = [
  '+', '-', '*', '/', '=', ';', ':', ',', '(', ')', '“value=”,',
  'program', 'var', 'integer', 'begin', 'end', 'show',
  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
  'a', 'b', 'r', 's',
  '$'
]

reserved_words = ["program", "var", "begin", "end", "integer", "show", '“value=”,']

def tokenize(filename):
    token_pattern = r'“value=”,|:=|==|!=|[a-zA-Z_][a-zA-Z0-9_]*|\d+|[+\-*/=;:(),]'


    tokens = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            line_tokens = re.findall(token_pattern, line)
            
            for tok in line_tokens:
                if tok in reserved_words:
                    tokens.append(tok)
                else:
                    tokens.extend(list(tok))
            

    tokens.append('$')
    return tokens

def searchMissing(filename, char):
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.endswith(char):
                continue
            else:
                print(f"SOME ERRORS: '{char}' is missing")

def parse(tokens):
    stack = ['$', 'P']
    pointer = 0

    print(f"{'Stack':<30} {'Input':<30} {'Action'}")
    print('-' * 90)

    while stack:
        top = stack[-1] # Top of the stack
        current_token = tokens[pointer] if pointer < len(tokens) else '$'

        print(f"{''.join(stack):<30} {current_token:<30}", end=' ')

        if top == current_token == '$':
            print("NO ERROR: ACCEPTED")
            return True

        elif top in terminals:
            if top == current_token: # Checking if the input is in the terminal chars
                stack.pop()
                pointer += 1
                print(f"'{top}'")
            else:
                print(f"SOME ERRORS: '{top}' is expected, found '{current_token}'")
                return False
        else:
            rule = parsing_table.get(top, {}).get(current_token) # Retrieving the correct column based on current input char
            if rule is not None:
                stack.pop()
                if rule:  # Not lambda
                    for symbol in reversed(rule):
                        stack.append(symbol)
                    print(f"{top} -> {' '.join(rule)}")
                else:
                    print(f"{top} -> λ")
            else:
                searchMissing("final25missing.txt", ";")
                return False

def main():
    tokens = tokenize("final25.txt")
    parse(tokens)

if __name__ == '__main__':
    main()