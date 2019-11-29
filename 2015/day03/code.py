

def north(start):
    return (start[0] + 0, start[1] + 1)

def south(start):
    return (start[0] + 0, start[1] - 1)

def east(start):
    return (start[0] + 1, start[1] + 0)

def west(start):
    return (start[0] - 1, start[1] + 0)

cmd_map = {
    '^': north,
    'v': south,
    '>': east,
    '<': west
}

def house_coords(position, seq):
    yield position
    for command in seq:
        f = cmd_map.get(command, None)
        if not f:
            continue
        position = f(position)
        yield position

def santa():
    with open('input.txt', 'r') as f:
        cmd_str = f.read()
        places = set()
        for p in house_coords((0, 0), cmd_str):
            places.add(p)
        print(len(places))

def santa_and_robot():
    with open('input.txt', 'r') as f:
        cmd_str = f.read()
        santa_cmds = cmd_str[0::2]
        robot_cmds = cmd_str[1::2]
        places = set()
        for p in house_coords((0, 0), santa_cmds):
            places.add(p)
        for p in house_coords((0, 0), robot_cmds):
            places.add(p)
        print(len(places))

if __name__ == '__main__':
    santa_and_robot()
