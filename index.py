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
re_target = r'(/([+-=]?\d+|\d+-\d+))?'
re_final = r'^{}{}$'.format(re_all_dice, re_target)
re_input = re.compile(re_final)
re_target_range = re.compile(r'^\d+-\d+$')

for dice_input in attempts:
    if not re_input.match(dice_input):
        sys.stderr.write(f'Invalid dice: `{dice_input}`\n')
        sys.stderr.write('Dice must be in the form "[+,-]{{M}}+{{N}}d{{X}}(,...more dice)[/{{T}}]" where M, N, X, T are:\n')
        sys.stderr.write('M - Modifier (positive or negative)\n')
        sys.stderr.write('N - Number of dice\n')
        sys.stderr.write('X - Number of sides\n')
        sys.stderr.write('T - Target value\n')
        sys.stderr.write('    4 or +4 means "Greater than or equal to 4"\n')
        sys.stderr.write('    -4 means "Less than or equal to 4"\n')
        sys.stderr.write('    =4 means "Equal to 4"\n')
        sys.stderr.write('    3-5 means "In the range 3-5, inclusive"\n')
        sys.stderr.write('\n')
        sys.stderr.write('When more dice are included, any can be used to match the target (e.g. Savage Worlds Wild Die).\n')
        sys.exit(1)


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


TARGET_GTE = '>='
TARGET_LTE = '<='
TARGET_EQ = '=='
TARGET_RANGE = '[]'
def target_test(val, target, target_op):
    if target_op == TARGET_GTE and val >= target:
        return True
    elif target_op == TARGET_LTE and val <= target:
        return True
    elif target_op == TARGET_EQ and val == target:
        return True
    elif target_op == TARGET_RANGE and val >= target[0] and val <= target[1]:
        return True
    return False

def target_description(target_op, target):
    if target_op == TARGET_GTE:
        return f'>= {target}'
    elif target_op == TARGET_LTE:
        return f'<= {target}'
    elif target_op == TARGET_EQ:
        return f'== {target}'
    elif target_op == TARGET_RANGE:
        return f'{target[0]}<=...<={target[1]}'
    return ''


class Report:
    def __init__(self):
        self.stats = []
        self.percentages = []
        self.rolls = []
        self.successes = None

    def print(self, show_stats, show_rolls):
        if show_stats:
            section('STATS')
            for (header, dice_min, dice_max, avg) in self.stats:
                label(header)
                print(f'min: {dice_min}')
                print(f'max: {dice_max}')
                print(f'avg: {avg}')
                print()

        if show_stats:
            section('PERCENTAGES')
            for data in self.percentages:
                data.print()

        if show_rolls:
            section('ROLLS')

            for (type, roll) in self.rolls:
                if type == 'target':
                    roll.print(show_stats=show_stats, show_rolls=show_rolls)
                else:
                    roll.print()
            print()

        if show_rolls and len(self.successes[1]) > 1:
            did_succeed, successes = self.successes
            success = reduce(lambda m, p: m * p, successes, 1)
            section('TOTAL SUCCESS')
            if show_stats:
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
        self.rolls.append(('target', target))

    def append_rolls(self, rolls):
        self.rolls.append(('roll', rolls))

    def set_successes(self, did_succeed, successes):
        self.successes = (did_succeed, successes)


class Percentages:
    def __init__(self, all_dice, target, target_op):
        self.name = ','.join(all_dice)
        if target:
            self.name += ' ' + target_description(target_op, target)
        self.stats = []
        self.target = None

    def print(self):
        print(self.name)
        print('-' * len(self.name))
        for (val, count, len_all, percent) in self.stats:
            print(f'{val}: {count} of {len_all} ({percent}%)')
        if self.target:
            target, target_op, target_counts, len_all, percent = self.target
            operator = target_description(target_op, target)
            print(f'% of rolls {operator}: {target_counts} of {len_all} ({percent}%)')
        print()

    def append_stats(self, val, count, len_all):
        self.stats.append((val, count, len_all, percent(count, len_all)))

    def set_target_percentages(self, target, target_op, target_counts, len_all):
        self.target = (target, target_op, target_counts, len_all, percent(target_counts, len_all))


class Target:
    def __init__(self, all_dice, target, target_op, all_random_rolls, did_succeed):
        self.name = ','.join(all_dice)
        self.stats = (target, target_op, Rolls(all_random_rolls), did_succeed)

    def print(self, show_stats, show_rolls):
        if ',' in self.name:
            print(self.name)
            print('-' * len(self.name))
        (target, target_op, rolls, did_succeed) = self.stats
        if show_rolls:
            rolls.print()

        if show_rolls:
            operator = target_description(target_op, target)
            success_text = did_succeed and 'Succeeded' or 'Failed'
            print(f'target ({operator}): {success_text}')
        print()


class Rolls:
    def __init__(self, rolls):
        self.rolls = rolls

    def print(self):
        for roll_data in self.rolls:
            total_roll, dice = roll_data
            header = ' + '.join([die.header(show_rolls=len(dice) > 1) for die in dice])
            print(f'  {header} = {total_roll}')


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
        target_op = TARGET_GTE
        target_str = target
        if target.startswith('-'):
            target_op = TARGET_LTE
            target = int(target[1:])
        elif target.startswith('='):
            target_op = TARGET_EQ
            target = int(target[1:])
        elif target.startswith('+'):
            target = int(target[1:])
        elif re_target_range.match(target):
            target_op = TARGET_RANGE
            target = target.split('-', 2)
            target = (int(target[0]), int(target[1]))
        else:
            target = int(target)
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
        total_roll = reduce(lambda a, b: a + b, [die.roll() for die in dice], 0)
        if target:
            any_roll_success = any_roll_success or target_test(total_roll, target, target_op)

        all_rolls.append(total_roll)

        possible_rolls = reduce(add_die_rolls, dice, [0])
        all_possible_rolls = combine_rolls(all_possible_rolls, possible_rolls)
        all_min = min(dice_min, all_min is None and dice_min or all_min)
        all_max = max(dice_max, all_max is None and dice_max or all_max)

        header = ' + '.join(map(lambda d: d.header(), dice))
        all_random_rolls.append((total_roll, dice))
        report.append_stats(header, dice_min, dice_max, avg)

    len_all_possible_rolls = len(all_possible_rolls)

    # probability of any roll
    percentages = Percentages(all_dice_inputs, target, target_op)
    for val in range(all_min, all_max + 1):
        count = len([1 for rolls in all_possible_rolls if any(map(lambda die_val: die_val == val, rolls))])
        percentages.append_stats(val, count, len_all_possible_rolls)
    report.append_percentages(percentages)

    if target:
        target_counts = len([1 for rolls in all_possible_rolls if any(map(lambda die_val: target_test(die_val, target, target_op), rolls))])
        attempt_successes.append(target_counts / float(len_all_possible_rolls))
        attempts_did_succeed = attempts_did_succeed and any_roll_success

        percentages.set_target_percentages(target, target_op, target_counts, len_all_possible_rolls)
        target = Target(all_dice_inputs, target, target_op, all_random_rolls, any_roll_success)
        report.append_target(target)
    else:
        report.append_rolls(Rolls(all_random_rolls))

report.set_successes(attempts_did_succeed, attempt_successes)

show_stats = '--stats' in options or not options
show_rolls = '--roll' in options or not options
report.print(show_stats=show_stats, show_rolls=show_rolls)
