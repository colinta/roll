import random


class Die:
    def __init__(self):
        raise Error('Die is abstract')

    def header(self, show_rolls=False):
        return ''

    def roll(self):
        return 0

    def all_possible_rolls(self):
        return []

    def __repr__(self):
        return '<Die>'

    @classmethod
    def parse(cls, dice_input):
        if 'd' in dice_input:
            if '*' in dice_input:
                (multiplier, dice_input) = dice_input.split('*', 2)
                multiplier = int(multiplier)
            else:
                multiplier = 1

            if dice_input.endswith('!'):
                return DieExploding(multiplier, int(dice_input[1:-1]))

            if dice_input == 'd%':
                return DiePercentile(multiplier, count)

            (count, die) = dice_input.split('d', 2)

            if count:
                count = int(count)
            else:
                count = 1

            return DieStandard(multiplier, count, int(die))
        else:
            return DieConstant(int(dice_input))


class DieConstant(Die):
    def __init__(self, plus):
        self.plus = plus
        self.count = 0
        self.min = plus
        self.max = plus
        self.avg = plus

    def header(self, show_rolls=False):
        return f'{self.plus}'

    def roll(self):
        return self.plus

    def all_possible_rolls(self):
        return [self.plus]

    def __repr__(self):
        return f'<DieConstant {self.plus}>'


class DieStandard(Die):
    def __init__(self, multiplier, count, die):
        self.multiplier = multiplier
        self.count = count
        self.die = die
        self.min = multiplier * count
        self.max = multiplier * count * die
        self.avg = multiplier * count * (die + 1) / 2.0

        sum = 0
        random_rolls = []
        for _ in range(0, self.count):
            roll = random.randint(1, self.die)
            random_rolls.append(roll)
            sum += self.multiplier * roll
        self.random_roll_sum = sum
        self.random_rolls = random_rolls

    def header(self, show_rolls=False):
        rolls_str = ''
        if show_rolls:
            rolls_str = ' (' + (', '.join([str(i) for i in self.random_rolls])) + ')'

        if self.count == 1:
            die_str = f'd{self.die}{rolls_str}'
        else:
            die_str = f'{self.count}d{self.die}{rolls_str}'

        if self.multiplier and self.multiplier > 1:
            die_str = f'{self.multiplier} × {die_str}'
        return die_str

    def roll(self):
        return self.random_roll_sum

    def all_possible_rolls(self):
        def one_die_roll(die, count):
            roll_range = [self.multiplier * n for n in range(1, die + 1)]
            if count == 1:
                return [n for n in roll_range]
            rolls = one_die_roll(die, count - 1)
            return [n + r for r in rolls for n in roll_range]

        return one_die_roll(self.die, self.count)

    def __repr__(self):
        return f'<DieStandard {self.header(show_rolls=True)}>'


class DiePercentile(DieStandard):
    def __init__(self, multiplier):
        super().__init__(multiplier, 1, 100)

    def header(self, show_rolls=False):
        rolls_str = ''
        if show_rolls:
            rolls_str = ' (' + (', '.join([str(i) for i in self.random_rolls])) + ')'

        if self.count == 1:
            die_str = f'd%{rolls_str}'
        else:
            die_str = f'{self.count}d%{rolls_str}'

        if self.multiplier and self.multiplier > 1:
            die_str = f'{self.multiplier} × {die_str}'
        return die_str

    def roll(self):
        return self.random_roll_sum

    def all_possible_rolls(self):
        def one_die_roll(die, count):
            roll_range = [self.multiplier * n for n in range(1, die + 1)]
            if count == 1:
                return [n for n in roll_range]
            rolls = one_die_roll(die, count - 1)
            return [n + r for r in rolls for n in roll_range]

        return one_die_roll(self.die, self.count)

    def __repr__(self):
        return f'<DiePercentile {self.header(show_rolls=True)}>'


class DieExploding(DieStandard):
    def __init__(self, multiplier, die):
        self.multiplier = multiplier
        self.count = 1
        self.die = die
        self.min = multiplier
        self.max = multiplier * die * 3
        self.avg = multiplier * (die + 1) / 2.0 * die / (die - 1)

        sum = 0
        random_rolls = []
        while True:
            roll = random.randint(1, self.die)
            random_rolls.append(roll)
            sum += roll
            if roll < self.die:
                break

        sum *= self.multiplier
        self.random_roll_sum = sum
        self.random_rolls = random_rolls

    def header(self, show_rolls=False):
        rolls_str = ''
        if show_rolls:
            def exploding_notation(i):
                if i == self.die:
                    return f'{i}!'
                return str(i)
            rolls_str = ' (' + (', '.join([exploding_notation(i) for i in self.random_rolls])) + ')'

        die_str = f'd{self.die}!{rolls_str}'

        if self.multiplier and self.multiplier > 1:
            die_str = f'{self.multiplier} × {die_str}'
        return die_str

    def roll(self):
        return self.random_roll_sum

    def all_possible_rolls(self):
        def one_die_roll(die, count):
            roll_range = [self.multiplier * n for n in range(1, die + 1)]
            if count == 1:
                return [n for n in roll_range]
            rolls = one_die_roll(die, count - 1)
            return [n + r for r in rolls for n in roll_range]

        roll_range = [self.multiplier * n for n in range(1, self.die)]
        roll_range_all = [self.multiplier * n for n in range(1, self.die + 1)]
        d_squared = self.die * self.die
        rolls = [n for n in roll_range for a in range(0, d_squared)]
        rolls += [self.die + n for n in roll_range for a in range(0, self.die)]
        rolls += [2 * self.die + n for n in roll_range_all]
        return rolls

    def __repr__(self):
        return f'<DieExploding {self.header(show_rolls=True)}>'
