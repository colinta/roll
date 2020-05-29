#!/usr/bin/env python
import sys
import re
import random
from functools import reduce
random.seed()

attempts = []
is_die = True
attempt_die = None
for arg in sys.argv[1:]:
    if is_die:
        attempt_die = arg
    else:
        attempts.append((attempt_die, arg))
    is_die = not is_die
if not is_die:
    attempts.append((attempt_die, None))

successes = []
for (dice_input, target) in attempts:
    if not attempts:
        sys.stderr.write('Missing dice argument\n')
        sys.exit(1)

    if not re.match(r'(\d+|\d*d\d+)(\+(\d+|\d*d\d+))*', dice_input):
        sys.stderr.write('Invalid dice: `{}`\n'.format(dice_input))
        sys.stderr.write('Dice be in the form "[A]+[N]d[X]" where A, N, X are integers.\n')
        sys.exit(1)

    target_gt = True
    if target == '-':
        target = None
    if target:
        try:
            if target.startswith('-'):
                target_gt = False
                target = target[1:]
            elif target.startswith('+'):
                target = target[1:]

            target = int(target)
        except ValueError:
            sys.stderr.write('Invalid target: `{}`\n'.format(target))
            sys.exit(1)

    class Die:
        def __init__(self, plus, count, die):
            self.plus = plus
            self.count = count
            self.die = die
            self.min = plus + count
            self.max = plus + count * die
            self.avg = plus + count * (die + 1) / 2.0

        def header(self):
            if self.plus and self.die:
                if self.count == 1:
                    return '{} + d{}'.format(self.plus, self.count, self.die)
                else:
                    return '{} + {} × d{}'.format(self.plus, self.count, self.die)
            if self.plus:
                return '{}'.format(self.plus)
            if self.count == 1:
                return 'd{}'.format(self.die)
            else:
                return '{} × d{}'.format(self.count, self.die)

        def roll(self):
            sum = self.plus
            for _ in range(0, self.count):
                roll = random.randint(1, self.die)
                sum += roll
            return sum

        def all_rolls(self):
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
            return '<{}, min: {}, max: {}>'.format(self.header(), self.min, self.max)

        @classmethod
        def parse(cls, dice_input):
            if 'd' in dice_input:
                try:
                    (count, die) = dice_input.split('d', 2)
                except ValueError:
                    sys.stderr.write('Invalid dice: `{}`\n'.format(dice_input))
                    sys.exit(1)
                if count:
                    count = int(count)
                else:
                    count = 1
                return Die(0, count, int(die))
            else:
                return Die(int(dice_input), 0, 0)


    all_dice_inputs = dice_input.split('+')
    dice = [Die.parse(input) for input in all_dice_inputs]

    def add_min(memo, die):
        return memo + die.min
    def add_max(memo, die):
        if die.max == int(die.max):
            return memo + int(die.max)
        return memo + die.max
    def add_avg(memo, die):
        if die.avg == int(die.avg):
            return memo + int(die.avg)
        return memo + die.avg
    def all_rolls(memo, die):
        return [n + r for r in memo for n in die.all_rolls()]

    def percent(val, total):
        return round(1000 * val / float(total)) / 10.0

    min = reduce(add_min, dice, 0)
    max = reduce(add_max, dice, 0)
    avg = reduce(add_avg, dice, 0)
    all_rolls = reduce(all_rolls, dice, [0])
    len_all_rolls = len(all_rolls)

    if len(attempts) == 1:
        header = ' + '.join(map(lambda d: d.header(), dice))
        line = '-' * len(header)
        print(header)
        print(line)
        print('min: {}'.format(min))
        print('max: {}'.format(max))
        print('avg: {}'.format(avg))
        print(line)

    # probability of any roll
    target_counts = 0
    for val in range(min, max + 1):
        count = len([1 for die_val in all_rolls if die_val == val])
        if target and target_gt and val >= target:
            target_counts += count
        elif target and not target_gt and val <= target:
            target_counts += count
        if len(attempts) == 1:
            print('{}: {} of {} ({}%)'.format(val, count, len_all_rolls, percent(count, len_all_rolls)))

    if target:
        if len(attempts) == 1:
            print('target {}{}: {} of {} ({}%)'.format(target_gt and '>=' or '<=', target, target_counts, len_all_rolls, percent(target_counts, len_all_rolls)))
        successes.append(target_counts / float(len_all_rolls))
    else:
        print('random roll:')
        roll = reduce(lambda a, b: a + b, [d.roll() for d in dice], 0)
        print('     {}'.format(roll))

if len(successes) > 1:
    success = reduce(lambda m, p: m * p, successes, 1)
    print('-' * 20)
    print('Total success: {}'.format(percent(success, 1)))
