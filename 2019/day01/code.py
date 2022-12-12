import os

here = os.path.dirname(__file__)
input_path = os.path.join(here, "input.txt")


def load_input():
    with open(input_path, "r") as f:
        for line in f:
            try:
                val = int(line)
                yield val
            except:
                pass


def main():
    total = 0
    for entry in load_input():
        fuel_needed = entry // 3 - 2
        while fuel_needed > 0:
            total += fuel_needed
            fuel_needed = fuel_needed // 3 - 2

    print("total", total)


if __name__ == "__main__":
    main()
