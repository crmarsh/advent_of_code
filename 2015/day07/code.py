import re
from pprint import pprint

test_input = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i""".split('\n')

expected_result = {
    'd': 72,
    'e': 507,
    'f': 492,
    'g': 114,
    'h': 65412,
    'i': 65079,
    'x': 123,
    'y': 456,
}

wires = {}
assignRe = re.compile("\s*->\s*")
numberRe = re.compile("[0-9]+$")
variableRe = re.compile("[a-z]+$")
unaryOpRe = re.compile("([A-Z]+)\s*(\w+)")
binaryOpRe = re.compile("(\w+)\s*([A-Z]+)\s*(\w+)")

def set_wire(w, val):
    global wires
    wires[w] = int(val) & 0xffff

def resolve_val(exp):
    if numberRe.match(exp):
        return int(exp) & 0xffff
    return wires[exp]

def apply_line(line):
    global wires
    try: lexp, wire = assignRe.split(line)
    except: return
    if numberRe.match(lexp):
        set_wire(wire, lexp)
    else:
        m = variableRe.match(lexp)
        if m:
            res = resolve_val(lexp)
            set_wire(wire, res)
        else:
            m = unaryOpRe.match(lexp)
            if m:
                op, operand = m.groups()
                operand = resolve_val(operand)
                if op == 'NOT':
                    operand = (~operand) & 0xffff
                set_wire(wire, operand)
            else:
                m = binaryOpRe.match(lexp)
                if m:
                    operand0, op, operand1 = m.groups()
                    operand0 = resolve_val(operand0)
                    operand1 = resolve_val(operand1)
                    if op == 'AND':
                        res = operand0 & operand1
                    elif op == 'OR':
                        res = operand0 | operand1
                    elif op == 'RSHIFT':
                        res = operand0 >> operand1
                    elif op == 'LSHIFT':
                        res = (operand0 << operand1) & 0xffff
                    else:
                        print('bin op', op, operand0, operand1)
                        res = 0
                    set_wire(wire, res)
                else:
                    print('wire', wire)
                    print('exp:', lexp)


def main():
    global wires
    for line in test_input:
        apply_line(line)
    print('test wires:')
    pprint(wires)
    unresolved = set()
    wires = {}
    with open('input-b.txt', 'r') as f:
        for line in f:
            unresolved.add(line.strip())
    while unresolved:
        was_unresolved = len(unresolved)
        to_remove = set()
        for line in unresolved:
            try:
                apply_line(line)
                to_remove.add(line)
            except Exception as e:
                pass
        unresolved -= to_remove
        now_unresolved = len(unresolved)
        if now_unresolved == was_unresolved:
            print("wtf, man", now_unresolved, "still unresolved")
            break
    print('wires:')
    pprint(wires)
    print('a:', wires['a'])

if __name__ == '__main__':
    main()

