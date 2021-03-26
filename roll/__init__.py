import sys
import io
import random
from functools import reduce
from .die import Die
from .result import Result
from .util import (
    RE_INPUT, RE_TARGET_RANGE, add_min, add_max, add_avg, add_die_rolls,
    combine_rolls, percent, target_test,
    TARGET_GTE, TARGET_LTE, TARGET_EQ, TARGET_RANGE
    )
from .report import Report, Percentages, Target, Rolls


def run(attempts, show_stats=True):
    random.seed()

    for dice_input in attempts:
        if not RE_INPUT.match(dice_input):
            err = io.StringIO()
            err.write(f'Invalid dice expression: `{dice_input}`\n')
            err.write('Valid dice expressions include:\n')
            err.write('• N sided die: `d6`, `d8`, `d20`\n')
            err.write('• Percent die: `d%`\n')
            err.write('• Many N-sided dice: `2d6`, `5d4`\n')
            err.write('• Multiplying N-sided dice: `2*d6`, `5*2d4`\n')
            err.write('• N-sided exploding die: `d6!`, `d12!`\n')
            err.write('• Adding a modifier (only add is supported, but negative modifiers are supported):\n')
            err.write('  Example: `5+d6`, `d10+-2`, `-2+d2`\n')
            err.write('• Comma separated list of these expressions, to make multiple rolls\n')
            err.write('  Example: `d10,d6`, `d8!,d6!`\n')
            err.write('• Specifying a target `/T`, with valid targets:\n')
            err.write('    /4 or /+4 means "Greater than or equal to 4"\n')
            err.write('    /-4 means "Less than or equal to 4"\n')
            err.write('    /=4 means "Equal to 4"\n')
            err.write('    /3-5 means "In the range 3-5, inclusive"\n')
            err.write('    Example: `d6/4`, `2d10/=4`\n')
            err.write('\n')
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
            total_roll = reduce(lambda a, b: a + b, [die.roll() for die in dice], 0)
            all_rolls.append(total_roll)
            header = ' + '.join(map(lambda d: d.header(), dice))
            all_random_rolls.append((total_roll, dice))

            if target:
                any_roll_success = any_roll_success or target_test(total_roll, target, target_op)

            if show_stats:
                dice_min = reduce(add_min, dice, 0)
                dice_max = reduce(add_max, dice, 0)
                avg = reduce(add_avg, dice, 0)

                possible_rolls = reduce(add_die_rolls, dice, [0])
                all_possible_rolls = combine_rolls(all_possible_rolls, possible_rolls)
                all_min = min(dice_min, all_min is None and dice_min or all_min)
                all_max = max(dice_max, all_max is None and dice_max or all_max)

                report.append_stats(header, dice_min, dice_max, avg)

        len_all_possible_rolls = len(all_possible_rolls)

        # probability of any roll
        if show_stats:
            percentages = Percentages(dice_input, target, target_op)
            for val in range(all_min, all_max + 1):
                count = len([1 for rolls in all_possible_rolls if any(map(lambda die_val: die_val == val, rolls))])
                percentages.append_stats(val, count, len_all_possible_rolls)
            report.append_percentages(percentages)

        if target:
            if show_stats:
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

    show_stats = not options
    show_rolls = '--roll' in options or not options
    result = run(rolls, show_stats=show_stats)
    if isinstance(result, Result.Err):
        print(result.err)
    else:
        report = result.val
        report.print(show_stats=show_stats, show_rolls=show_rolls)
