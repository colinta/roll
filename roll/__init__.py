import sys
import io
import random
from functools import reduce
from .die import Die
from .result import Result
from .util import (
    RE_INPUT, RE_TARGET_RANGE, add_min, add_max, add_avg, add_die_rolls,
    combine_rolls, percent
    )
from .report import Report, Percentages, Target, Rolls


def run(attempts):
    random.seed()

    for dice_input in attempts:
        if not RE_INPUT.match(dice_input):
            err = io.StringIO()
            err.write(f'Invalid dice: `{dice_input}`\n')
            err.write('Dice must be in the form "[+,-]{{M}}+{{N}}d{{X}}(,...more dice)[/{{T}}]" where M, N, X, T are:\n')
            err.write('M - Modifier (positive or negative)\n')
            err.write('N - Number of dice\n')
            err.write('X - Number of sides, or `%`\n')
            err.write('T - Target value\n')
            err.write('    4 or +4 means "Greater than or equal to 4"\n')
            err.write('    -4 means "Less than or equal to 4"\n')
            err.write('    =4 means "Equal to 4"\n')
            err.write('    3-5 means "In the range 3-5, inclusive"\n')
            err.write('\n')
            err.write('When more dice are included, any can be used to match the target (e.g. Savage Worlds Wild Die).\n')
            result = Result.Err(err.getvalue())
            return result

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
            elif RE_TARGET_RANGE.match(target):
                target_op = TARGET_RANGE
                target = target.split('-', 2)
                target = (int(target[0]), int(target[1]))
            else:
                target = int(target)
        else:
            target = None
            target_op = None

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
        percentages = Percentages(dice_input, target, target_op)
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
    return Result.Ok(report)


def main():
    args = sys.argv[1:]
    rolls = []
    options = []
    for arg in args:
        if arg.startswith('--'):
            options.append(arg)
        else:
            rolls.append(arg)
    if not rolls:
        sys.stderr.write('Missing dice argument\n')
        sys.exit(1)

    show_stats = '--stats' in options
    show_rolls = '--roll' in options or not options
    result = run(rolls)
    if isinstance(result, Result.Err):
        print(result.err)
    else:
        report = result.val
        report.print(show_stats=show_stats, show_rolls=show_rolls)
