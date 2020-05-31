from functools import reduce
from .util import (percent)


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
    def __init__(self, name, target, target_op):
        self.name = name
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
