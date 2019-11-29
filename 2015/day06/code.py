from pprint import pprint

size_x = size_y = 1000
light_grid = []
for i in range(size_y):
    row = []
    for j in range(size_x):
        row.append(0)
    light_grid.append(row)


def count_lights():
    total = 0
    for row in light_grid:
        total += sum(row)
    return total


def parse_point(s):
    res = [x for x in map(int, s.split(','))]
    return res[0], res[1]
    

def parse_command(s):
    a = s.split(' ')
    if len(a) < 4:
        return None, None, None
    if a[0] == "turn":
        if a[1] == "on":
            cmd = lambda x: x + 1
        elif a[1] == "off":
            cmd = lambda x: max(0, x - 1)
        a = a[2:]
    elif a[0] == 'toggle':
        cmd = lambda x: x + 2
        a = a[1:]
    p0str, _, p1str = a
    p0 = parse_point(p0str)
    p1 = parse_point(p1str)
    return p0, p1, cmd
    

def enum_points(a, b):
    y_range = min(a[1], b[1]), max(a[1], b[1])
    x_range = min(a[0], b[0]), max(a[0], b[0])
    for y in range(y_range[0], y_range[1] + 1):
        for x in range(x_range[0], x_range[1] + 1):
            yield x, y
    

def main():
    global light_grid
    with open("input.txt", 'r') as f:
        for line in f:
            p0, p1, cmd = parse_command(line)
            if not cmd:
                continue
            r = [a for a in enum_points(p0, p1)]
            for p in r:
                light_grid[p[0]][p[1]] = cmd(light_grid[p[0]][p[1]])
    print("lights on:", count_lights())


if __name__ == '__main__':
    main()
