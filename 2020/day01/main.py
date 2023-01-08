import sys

if __name__ == "__main__":
    target_num = 2020
    adds_to = {}
    numbers: list[int] = []
    try:
        fname = sys.argv[1]
    except:
        fname = "sample_input.txt"
    with open(fname, "r") as f:
        for line in f:
            try:
                n = int(line)
            except:
                continue
            inv = target_num - n
            if n in adds_to:
                print(n, inv, n * inv)
            index = len(numbers)
            adds_to[inv] = index
            numbers.append(n)
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            a = numbers[i]
            b = numbers[j]
            k = adds_to.get(a + b)
            if k:
                if k < j:
                    continue
                c = numbers[k]
                print(a, b, c, a * b * c)
