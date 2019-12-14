import itertools
import math


class Equipment(object):
    __slots__ = ['name', 'cost', 'damage', 'armor']
    def __init__(self, name, cost, damage, armor):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.armor = armor
    
    def __repr__(self):
        return str.format('<{0}, {1}, {2}, {3}>', self.name, self.cost, self.damage, self.armor)


class Character(object):
    __slots__ = ['name', 'hp', 'damage', 'armor']
    def __init__(self, name, hp, damage, armor):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.armor = armor
    
    def __repr__(self):
        return str.format('<{0}, {1}, {2}, {3}>', self.name, self.hp, self.damage, self.armor)
    


boss = Character('boss',  100, 8, 2)
you =  Character('you',   100, 0, 0)

weapons = [
    Equipment('Dagger',        8,     4,      0),
    Equipment('Shortsword',   10,     5,      0),
    Equipment('Warhammer',    25,     6,      0),
    Equipment('Longsword',    40,     7,      0),
    Equipment('Greataxe',     74,     8,      0),
]

armors = [
    Equipment('No Armor',      0,     0,      0),
    Equipment('Leather',      13,     0,      1),
    Equipment('Chainmail',    31,     0,      2),
    Equipment('Splintmail',   53,     0,      3),
    Equipment('Bandedmail',   75,     0,      4),
    Equipment('Platemail',   102,     0,      5),
]

rings = [
    Equipment('No Ring 1',     0,     0,      0),
    Equipment('No Ring 2',     0,     0,      0),
    Equipment('Damage +1',    25,     1,      0),
    Equipment('Damage +2',    50,     2,      0),
    Equipment('Damage +3',   100,     3,      0),
    Equipment('Defense +1',   20,     0,      1),
    Equipment('Defense +2',   40,     0,      2),
    Equipment('Defense +3',   80,     0,      3),
]


def enumerate_equipment():
    for weapon in weapons:
        for armor in armors:
            # 2 rings
            for ring_set in itertools.combinations(rings, 2):
                yield [weapon, armor, ring_set[0], ring_set[1]]


def do_combat(equipment):
    you_damage = max(1, sum([e.damage for e in equipment]) - boss.armor)
    boss_damage = max(1, boss.damage - sum([e.armor for e in equipment]))
    you_rounds = math.ceil(boss.hp / you_damage)
    boss_rounds = math.ceil(you.hp / boss_damage)
    return you_rounds <= boss_rounds


def main():
    min_cost = 99999999
    min_cost_equip = None
    for equipment in enumerate_equipment():
        if do_combat(equipment):
            cost = sum([e.cost for e in equipment])
            if cost < min_cost:
                min_cost = cost
                min_cost_equip = equipment
    print(min_cost, min_cost_equip)


if __name__ == '__main__':
    main()