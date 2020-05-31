import re


RE_CONSTANT = r'[+-]?\d+'
RE_DICE = r'\d* *d\d+'
RE_EITHER = r'({}|{})'.format(RE_CONSTANT, RE_DICE)
RE_DICE_FORMULA = r'{0}(\+{0})*'.format(RE_EITHER)
RE_ALL_DICE = r'{0}(,{0})*'.format(RE_DICE_FORMULA)
RE_TARGET = r'(/([+-=]?\d+|\d+-\d+))?'
RE_FINAL = r'^{}{}$'.format(RE_ALL_DICE, RE_TARGET)
RE_INPUT = re.compile(RE_FINAL)
RE_TARGET_RANGE = re.compile(r'^\d+-\d+$')


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
