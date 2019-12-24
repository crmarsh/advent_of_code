

class Base(object):
    def __init__(self, *args, **kwargs): pass

# https://gist.github.com/mrocklin/5786874
class Slotted(Base):
    def __init__(self, *args, **kwargs):
        try:
            for slot, arg in zip(self.__slots__, args):
                setattr(self, slot, arg)
        except AttributeError:
            raise TypeError("%s does not define __slots__" %
                             type(self).__name__)
        super(Slotted, self).__init__(*args, **kwargs)

    def _info(self):
        return (type(self), tuple(map(self.__getattribute__, self.__slots__)))

    def __eq__(self, other):
        return self._info() == other._info()

    def __str__(self):
        return '%s(%s)' % (type(self).__name__,
               ', '.join("%s=%s" % (slot, getattr(self, slot))
                            for slot in self.__slots__))

    __repr__ = __str__


class EffectDesc(Slotted):
    __slots__ = ['name', 'turns', 'damage', 'armor', 'mana']


class SpellDesc(Slotted):
    __slots__ = ['name', 'mana_cost' 'damage', 'heal', 'effect']
        

class CharacterVitals(Slotted):
    __slots__ = ['hp', 'mana', 'armor', 'effects']


class CharacterDesc(Slotted):
    __slots__ = ['name', 'actions']


class World(object):
    player_spells = [
        SpellDesc('Magic Missle', 53, 4, 0, None),
        SpellDesc('Drain', 73, 2, 2, None),
        SpellDesc('Shield', 113, 0, 0, EffectDesc('Shield effect', 6, 0, 7, 0)),
        SpellDesc('Poison', 173, 0, 0, EffectDesc('Poison effect', 6, 3, 0, 0)),
        SpellDesc('Recharge', 229, 0, 0, EffectDesc('Recharge effect', 5, 0, 0, 101)),
    ]

    boss_spells = [
        SpellDesc('Attack', 0, 9, 0, None)
    ]

    def __init__(self):
        self.boss = CharacterDesc('Boss', World.boss_spells)
        self.player = CharacterDesc('Player', World.player_spells)
        self.boss_state = CharacterVitals(58, 0, 0, [])
        self.player_state = CharacterVitals(50, 500, 0, [])
        self.turn = 'player'
        self.mana_spent = 0
    
    def __str__(self):
        state = []
        state.append(str.format('-- {0} turn --', self.turn.title()))
        state.append(str.format('- Player has {0} hit points, {1} armor, {2} mana',
            self.player_state.hp, self.player_state.armor, self.player_state.mana))
        state.append(str.format('- Boss has {0} hit points', self.boss_state.hp))
        return '\n'.join(state)
    
    def apply_status_effects():
        for effect in self.boss_state.effects:
            self.boss_state.hp -= effect.damage
            effect.turns -= 1
        for effect in self.player_state.effects:
            self.

    def turn(player_action_index, boss_action_index):



def main():
    w = World()
    print(w)


if __name__ == '__main__':
    main()