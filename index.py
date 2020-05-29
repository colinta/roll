#!/usr/bin/env python
import sys
import re
import random
from functools import reduce
random.seed()


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
        return '<{}, min: {}, max: {}, avg: {}>'.format(self.header(), self.min, self.max, self.avg)

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
def add_die_rolls(memo, die):
    return [n + r for r in memo for n in die.all_possible_rolls()]
def combine_rolls(memo, rolls):
    if not memo:
        return [(r,) for r in rolls]
    return [r + (n, ) for r in memo for n in rolls]

def percent(val, total):
    return round(1000 * val / float(total)) / 10.0


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
if not attempts:
    sys.stderr.write('Missing dice argument\n')
    sys.exit(1)

re_constant = r'\d+'
re_dice = r'\d*d\d+'
re_either = r'({}|{})'.format(re_constant, re_dice)
re_dice_formula = r'{0}(\+{0})*'.format(re_either)
re_all_dice = r'^{0}(,{0})*$'.format(re_dice_formula)
re_input = re.compile(re_all_dice)

attempts_did_succeed = True
attempt_random_rolls = []
attempt_successes = []
for (dice_input, target) in attempts:
    if not re_input.match(dice_input):
        sys.stderr.write('Invalid dice: `{}`\n'.format(dice_input))
        sys.stderr.write('Dice must be in the form "[A]+[N]d[X]" where A, N, X are integers.\n')
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

    all_dice_inputs = dice_input.split(',')
    all_possible_rolls = []
    all_min = None
    all_max = None
    all_rolls = []
    all_headers = []
    any_roll_success = False
    for dice_option in all_dice_inputs:
        all_dice_inputs = dice_option.split('+')
        dice = [Die.parse(input) for input in all_dice_inputs]

        dice_min = reduce(add_min, dice, 0)
        dice_max = reduce(add_max, dice, 0)
        avg = reduce(add_avg, dice, 0)
        roll = reduce(lambda a, b: a + b, [d.roll() for d in dice], 0)
        if target_gt:
            any_roll_success = any_roll_success or roll >= target
        else:
            any_roll_success = any_roll_success or roll <= target

        all_rolls.append(roll)

        possible_rolls = reduce(add_die_rolls, dice, [0])
        all_possible_rolls = combine_rolls(all_possible_rolls, possible_rolls)
        all_min = min(dice_min, all_min is None and dice_min or all_min)
        all_max = max(dice_max, all_max is None and dice_max or all_max)

        header = ' + '.join(map(lambda d: d.header(), dice))
        attempt_random_rolls.append((header, roll))
        if not header in all_headers:
            line = '-' * len(header)
            print(header)
            print(line)
            print('min: {}'.format(dice_min))
            print('max: {}'.format(dice_max))
            print('avg: {}'.format(avg))
            print(line)
            all_headers.append(header)
    len_all_possible_rolls = len(all_possible_rolls)

    # probability of any roll
    if target:
        all_attempt_successes = [rolls for rolls in all_possible_rolls if any(map(lambda die_val: die_val >= target, rolls))]
        for val in range(all_min, all_max + 1):
            count = len([1 for rolls in all_possible_rolls if any(map(lambda die_val: die_val == val, rolls))])
            print('{}: {} of {} ({}%)'.format(val, count, len_all_possible_rolls, percent(count, len_all_possible_rolls)))

        if target_gt:
            target_counts = len([1 for rolls in all_possible_rolls if any(map(lambda die_val: die_val >= target, rolls))])
        else:
            target_counts = len([1 for rolls in all_possible_rolls if any(map(lambda die_val: die_val <= target, rolls))])
        attempt_successes.append(target_counts / float(len_all_possible_rolls))
        attempts_did_succeed = attempts_did_succeed and any_roll_success

        print('target {}{}: {} of {} ({}%)'.format(target_gt and '>=' or '<=', target, target_counts, len_all_possible_rolls, percent(target_counts, len_all_possible_rolls)))
        print(line)
        print('random rolls:')
        for (header, roll) in attempt_random_rolls:
            print('{}: {}'.format(header, roll))
        print('target: {}'.format(any_roll_success and 'Succeeds' or 'Failed'))
        print(line)

if len(attempt_successes) > 1:
    success = reduce(lambda m, p: m * p, attempt_successes, 1)
    print('-' * 20)
    print('Total success chance: {}%'.format(percent(success, 1)))
    print('Random rolls: {}'.format(attempts_did_succeed and 'Succeeded' or 'Failed'))
