import random


class Die:
    def __init__(self, plus, count, die):
        self.plus = plus
        self.count = count
        self.die = die
        self.min = plus + count
        self.max = plus + count * die
        self.avg = plus + count * (die + 1) / 2.0

        sum = self.plus
        rolls = []
        for _ in range(0, self.count):
            roll = random.randint(1, self.die)
            rolls.append(roll)
            sum += roll
        self.random_roll = sum, rolls

    def header(self, show_rolls=False):
        rolls = ''
        if show_rolls and self.die:
            rolls = ' (' + (', '.join([str(i) for i in self.random_roll[1]])) + ')'

        if self.plus and self.die:
            if self.count == 1:
                return f'{self.plus} + d{self.die}{rolls}'
            else:
                return f'{self.plus} + {self.count} × d{self.die}{rolls}'
        if self.plus:
            return f'{self.plus}'
        if self.count == 1:
            return f'd{self.die}{rolls}'
        else:
            return f'{self.count} × d{self.die}{rolls}'

    def roll(self):
        return self.random_roll[0]

    def all_possible_rolls(self):
        if not self.die and not self.plus:
            return []
        if not (self.die and self.count):
            return [self.plus]

        def one_die_roll(die, count):
            roll_range = range(1, die + 1)
            if count == 1:
                return [n for n in roll_range]
            rolls = one_die_roll(die, count - 1)
            return [n + r for r in rolls for n in roll_range]

        return one_die_roll(self.die, self.count)

    def __repr__(self):
        return f'<{self.header(show_rolls=True)}, min: {self.min}, max: {self.max}, avg: {self.avg}>'

    @classmethod
    def parse(cls, dice_input):
        if 'd' in dice_input:
            (count, die) = dice_input.split('d', 2)

            if count:
                count = int(count)
            else:
                count = 1
            return Die(0, count, int(die))
        else:
            return Die(int(dice_input), 0, 0)
