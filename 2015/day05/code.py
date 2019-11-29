
test_cases0 = {
    'ugknbfddgicrmopn': True,
    'aaa': True,
    'jchzalrnumimnmhp': False,
    'haegwjzuvuyypxyu': False,
    'dvszwmarrgswjxmb': False,
}

vowels = set(['a', 'e', 'i', 'o', 'u'])
naughty = set(['ab', 'cd', 'pq', 'xy'])

def is_nice0(s):
    prev = ''
    vowel_count = 0
    in_a_row = 0
    for c in s:
        if (prev + c) in naughty:
            return False
        if c in vowels:
            vowel_count += 1
        if c == prev:
            in_a_row += 1
        prev = c
    if vowel_count < 3:
        return False
    if in_a_row < 1:
        return False
    return True


test_cases1 = {
    'qjhvhtzxzqqjkmpb': True,
    'xxyxx': True,
    'uurcxstgmygtbstg': False,
    'ieodomkazucvgmuy': False,
    'aaa': False,
}

def is_nice1(s):
    n = len(s)
    appear_twice = False
    for i in range(0, n - 3):
        part = s[i:i+2]
        rest = s[i+2:]
        if part in rest:
            appear_twice = True
            break
    if not appear_twice:
        return False
    for i in range(0, n - 2):
        if s[i] == s[i+2]:
            return True
    return False

def do_tests():
    for t in test_cases0.items():
        res = is_nice0(t[0])
        if res != t[1]:
            print("fails on", t[0])
    for t in test_cases1.items():
        res = is_nice1(t[0])
        if res != t[1]:
            print("fails on", t[0])


def main():
    with open('input.txt', 'r') as f:
        nice_count = 0
        for line in f:
            line = line.strip()
            if not line:
                continue
            if is_nice1(line):
                nice_count += 1
        print("nice:", nice_count)

if __name__ == '__main__':
    main()
