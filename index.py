#!/usr/bin/env python
import sys
import re
import random
from functools import reduce
random.seed()


args = sys.argv[1:]
attempts = []
options = []
for arg in args:
    if arg.startswith('--'):
        options.append(arg)
    else:
        attempts.append(arg)
if not attempts:
    sys.stderr.write('Missing dice argument\n')
    sys.exit(1)


re_constant = r'[+-]?\d+'
re_dice = r'\d* *d\d+'
re_either = r'({}|{})'.format(re_constant, re_dice)
re_dice_formula = r'{0}(\+{0})*'.format(re_either)
re_all_dice = r'{0}(,{0})*'.format(re_dice_formula)
re_target = r'(/{})?'.format(re_constant)
re_final = r'^{}{}$'.format(re_all_dice, re_target)
re_input = re.compile(re_final)

for dice_input in attempts:
    if not re_input.match(dice_input):
        sys.stderr.write(f'Invalid dice: `{dice_input}`\n')
        sys.stderr.write('Dice must be in the form "{{M}}+{{N}}d{{X}}(,...more dice)[/{{T}}]" where M, N, X, T are integers.\n')
        sys.stderr.write('M - Modifier (positive or negative)\n')
        sys.stderr.write('N - Number of dice\n')
        sys.stderr.write('X - Number of sides\n')
        sys.stderr.write('T - Target value (4 or +4 means "Greater than or equal to 4" and -4 means "Less than or equal to 4")\n')
        sys.stderr.write('Multiple Dice expressions can be tested against the target value (e.g. Savage Worlds Wild Die).\n')
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
                return f'{self.plus} + d{self.die}'
            else:
                return f'{self.plus} + {self.count} × d{self.die}'
        if self.plus:
            return f'{self.plus}'
        if self.count == 1:
            return f'd{self.die}'
        else:
            return f'{self.count} × d{self.die}'

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
        return f'<{self.header()}, min: {self.min}, max: {self.max}, avg: {self.avg}>'

    @classmethod
    def parse(cls, dice_input):
        if 'd' in dice_input:
            try:
                (count, die) = dice_input.split('d', 2)
            except ValueError:
                sys.stderr.write(f'Invalid dice: `{dice_input}`\n')
                sys.exit(1)
            if count:
                count = int(count)
            else:
                count = 1
            return Die(0, count, int(die))
        else:
            return Die(int(dice_input), 0, 0)


def section(name):
    print('+--' + '-' * len(name) + '--+')
    print(f'|  {name}  |')
    print('+--' + '-' * len(name) + '--+')

def label(name):
    print(f' {name}')
    line(name)

def line(name):
    if isinstance(name, str):
        return line(2 + len(name))
    print('-' * name)


class Report:
    def __init__(self):
        self.stats = []
        self.percentages = []
        self.targets = []
        self.rolls = []
        self.successes = None

    def print(self):
        section('STATS')
        for (header, dice_min, dice_max, avg) in self.stats:
            label(header)
            print(f'min: {dice_min}')
            print(f'max: {dice_max}')
            print(f'avg: {avg}')
            print()

        section('PERCENTAGES')
        for data in self.percentages:
            data.print()

        if self.targets:
            section('TARGET ROLLS')
            for target in self.targets:
                target.print()
        else:
            section('RANDOM ROLLS')
            for roll in self.rolls:
                roll.print()

        if len(self.successes) > 1:
            did_succeed, successes = self.successes
            success = reduce(lambda m, p: m * p, successes, 1)
            section('TOTAL SUCCESS')
            print(f'%chance: {percent(success, 1)}%')
            success_text = did_succeed and 'Succeeded' or 'Failed'
            print(f'Target rolls: {success_text}')

    def append_stats(self, header, dice_min, dice_max, avg):
        if any(map(lambda stat: stat[0] == header, self.stats)):
            return
        self.stats.append((header, dice_min, dice_max, avg))

    def append_percentages(self, data):
        if any(map(lambda entry: entry.name == data.name, self.percentages)):
            return
        self.percentages.append(data)

    def append_target(self, target):
        if any(map(lambda entry: entry.name == target.name, self.targets)):
            return
        self.targets.append(target)

    def append_rolls(self, rolls):
        self.rolls.append(rolls)

    def set_successes(self, did_succeed, successes):
        self.successes = (did_succeed, successes)


class Percentages:
    def __init__(self, all_dice):
        self.name = ','.join(all_dice)
        self.stats = []

    def print(self):
        print(self.name)
        print('-' * len(self.name))
        for (val, count, len_all, percent) in self.stats:
            print(f'{val}: {count} of {len_all} ({percent}%)')
        print()

    def append_stats(self, val, count, len_all, percent):
        self.stats.append((val, count, len_all, percent))


class Target:
    def __init__(self, all_dice, target, target_gt, target_counts, len_all, percent, all_random_rolls, did_succeed):
        self.name = ','.join(all_dice)
        self.stats = (target, target_gt, target_counts, len_all, percent, Rolls(all_random_rolls), did_succeed)

    def print(self):
        if ',' in self.name:
            print(self.name)
            print('-' * len(self.name))
        (target, target_gt, target_counts, len_all, percent, rolls, did_succeed) = self.stats
        rolls.print()
        operator = target_gt and '>=' or '<='
        print(f'%rolls {operator}{target}: {target_counts} of {len_all} ({percent}%)')
        success_text = did_succeed and 'Succeeded' or 'Failed'
        print(f'target: {success_text}')
        print()


class Rolls:
    def __init__(self, rolls):
        self.rolls = rolls

    def print(self):
        for (header, roll) in self.rolls:
            print(f'- {header}: {roll}')
        print()


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


attempts_did_succeed = True
attempt_successes = []
report = Report()
for dice_input in attempts:
    if '/' in dice_input:
        dice_input, target = dice_input.split('/', 2)
        target_gt = True
        if target == '-':
            target = None
        elif target:
            if target.startswith('-'):
                target_gt = False
                target = target[1:]
            elif target.startswith('+'):
                target = target[1:]

            try:
                target = int(target)
            except ValueError:
                sys.stderr.write(f'Invalid target: `{target}`\n')
                sys.exit(1)
    else:
        target = None

    all_dice_inputs = dice_input.split(',')
    all_dice = []
    all_possible_rolls = []
    all_random_rolls = []
    all_min = None
    all_max = None
    all_rolls = []
    any_roll_success = False
    for dice_option in all_dice_inputs:
        dice_inputs = dice_option.split('+')
        dice = [Die.parse(input) for input in dice_inputs]
        all_dice.append(dice)

        dice_min = reduce(add_min, dice, 0)
        dice_max = reduce(add_max, dice, 0)
        avg = reduce(add_avg, dice, 0)
        roll = reduce(lambda a, b: a + b, [d.roll() for d in dice], 0)
        if target and target_gt:
            any_roll_success = any_roll_success or roll >= target
        elif target:
            any_roll_success = any_roll_success or roll <= target

        all_rolls.append(roll)

        possible_rolls = reduce(add_die_rolls, dice, [0])
        all_possible_rolls = combine_rolls(all_possible_rolls, possible_rolls)
        all_min = min(dice_min, all_min is None and dice_min or all_min)
        all_max = max(dice_max, all_max is None and dice_max or all_max)

        header = ' + '.join(map(lambda d: d.header(), dice))
        all_random_rolls.append((header, roll))
        report.append_stats(header, dice_min, dice_max, avg)

    len_all_possible_rolls = len(all_possible_rolls)

    # probability of any roll
    percentages = Percentages(all_dice_inputs)
    for val in range(all_min, all_max + 1):
        count = len([1 for rolls in all_possible_rolls if any(map(lambda die_val: die_val == val, rolls))])
        percentages.append_stats(val, count, len_all_possible_rolls, percent(count, len_all_possible_rolls))
    report.append_percentages(percentages)

    if target:
        if target_gt:
            target_counts = len([1 for rolls in all_possible_rolls if any(map(lambda die_val: die_val >= target, rolls))])
        else:
            target_counts = len([1 for rolls in all_possible_rolls if any(map(lambda die_val: die_val <= target, rolls))])
        attempt_successes.append(target_counts / float(len_all_possible_rolls))
        attempts_did_succeed = attempts_did_succeed and any_roll_success

        target = Target(all_dice_inputs, target, target_gt, target_counts, len_all_possible_rolls, percent(target_counts, len_all_possible_rolls), all_random_rolls, any_roll_success)
        report.append_target(target)
    else:
        report.append_rolls(Rolls(all_random_rolls))

report.set_successes(attempts_did_succeed, attempt_successes)
report.print()
