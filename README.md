# Roll

The main point of this dice rolling script is to show statistics around the
likelihoods of different values. Plenty of dice rollers are out there, this one
shows all the possible values and their likelihoods.

It supports exploding dice, which technically do not have a highest maximum
value. For the sake of calculating the probabilities of the possible values, the
program assumes that rolling 3 consecutive exploding dice is impossible (i.e.
the highest roll of a d4 exploding die is 12). But the rolling simulator _does_
keep rolling as long as necessary.

Supported dice expressions:

- Any N-sided die, e.g. `d6`, `d8`, `d9`
- Multiple dice of the same kind (added together), e.g. `2d6`, `1d8`, `3d9`
- Modifiers (only the _add_ operation is supported, but negative numbers are
  fine), e.g. `4+d6`, `d6+-2`, `-2+d6+d8`
- Exploding dice, e.g. `d6!`, `d8!`
- Multipliers, e.g. `2*d6`
- Multiple choices, e.g. `d10!,d6!,2+d10`
- Targets, including greater than, less than, equal to, or in a range:
  - `d10/4`, any number ≥ 4 succeeds
  - `d10/-4`, any number ≤ 4 succeeds
  - `d10/=4`, only a roll of 4 succeeds
  - `d10/2-9`, any number 2 through 9 succeeds

Passing multiple arguments with targets are treated as successive target rolls,
e.g. the odds get smaller and smaller to succeed on all rolls.

###### Roll a die

```
$ roll d6
+---------+
|  STATS  |
+---------+
 d6
----
min: 1
max: 6
avg: 3.5

+---------------+
|  PERCENTAGES  |
+---------------+
d6
--
1: 1 of 6 (16.7%)
2: 1 of 6 (16.7%)
3: 1 of 6 (16.7%)
4: 1 of 6 (16.7%)
5: 1 of 6 (16.7%)
6: 1 of 6 (16.7%)

+---------+
|  ROLLS  |
+---------+
  d6 = 6
```

###### Die roll with target

```
$ roll d6/4
+---------+
|  ROLLS  |
+---------+
  d6 = 5
target (>=4): Succeeded
```

###### Die roll with modifier

```
$ roll 2+d12
+---------+
|  ROLLS  |
+---------+
  2 + d12 (12) = 14
```

###### Multi-die rolls

```
$ roll d12+d6
+---------+
|  STATS  |
+---------+
 d12 + d6
----------
min: 2
max: 18
avg: 10.0

+---------------+
|  PERCENTAGES  |
+---------------+
d12+d6
------
2: 1 of 72 (1.4%)
3: 2 of 72 (2.8%)
4: 3 of 72 (4.2%)
5: 4 of 72 (5.6%)
6: 5 of 72 (6.9%)
7: 6 of 72 (8.3%)
8: 6 of 72 (8.3%)
9: 6 of 72 (8.3%)
10: 6 of 72 (8.3%)
11: 6 of 72 (8.3%)
12: 6 of 72 (8.3%)
13: 6 of 72 (8.3%)
14: 5 of 72 (6.9%)
15: 4 of 72 (5.6%)
16: 3 of 72 (4.2%)
17: 2 of 72 (2.8%)
18: 1 of 72 (1.4%)
```

###### Modifier and multiple dice

```
$ roll 1+2d12
+---------+
|  ROLLS  |
+---------+
  1 + 2 × d12 (4, 4) = 9
```

# Target check

###### 4 or higher succeeds on a d8

```
$ roll d8/4 --roll
+---------+
|  STATS  |
+---------+
 d8
----
min: 1
max: 8
avg: 4.5

+---------------+
|  PERCENTAGES  |
+---------------+
d8 >= 4
-------
1: 1 of 8 (12.5%)
2: 1 of 8 (12.5%)
3: 1 of 8 (12.5%)
4: 1 of 8 (12.5%)
5: 1 of 8 (12.5%)
6: 1 of 8 (12.5%)
7: 1 of 8 (12.5%)
8: 1 of 8 (12.5%)
% of rolls >= 4: 5 of 8 (62.5%)

+---------+
|  ROLLS  |
+---------+
  d8 = 8
target (>= 4): Succeeded
```

###### 4 or LOWER succeeds on a d8

```
$ roll d8/-4 --roll
+---------+
|  STATS  |
+---------+
 d8
----
min: 1
max: 8
avg: 4.5

+---------------+
|  PERCENTAGES  |
+---------------+
d8 <= 4
-------
1: 1 of 8 (12.5%)
2: 1 of 8 (12.5%)
3: 1 of 8 (12.5%)
4: 1 of 8 (12.5%)
5: 1 of 8 (12.5%)
6: 1 of 8 (12.5%)
7: 1 of 8 (12.5%)
8: 1 of 8 (12.5%)
% of rolls <= 4: 4 of 8 (50.0%)

+---------+
|  ROLLS  |
+---------+
  d8 = 5
target (<= 4): Failed
```

# Chance of either roll succeeding

```
$ roll d8,d6/+4 --roll
+---------+
|  STATS  |
+---------+
 d8
----
min: 1
max: 8
avg: 4.5

 d6
----
min: 1
max: 6
avg: 3.5

+---------------+
|  PERCENTAGES  |
+---------------+
d8,d6 >= 4
----------
1: 13 of 48 (27.1%)
2: 13 of 48 (27.1%)
3: 13 of 48 (27.1%)
4: 13 of 48 (27.1%)
5: 13 of 48 (27.1%)
6: 13 of 48 (27.1%)
7: 6 of 48 (12.5%)
8: 6 of 48 (12.5%)
% of rolls >= 4: 39 of 48 (81.2%)

+---------+
|  ROLLS  |
+---------+
d8,d6
-----
  d8 = 2
  d6 = 4
target (>= 4): Succeeded
```

# Roll multiple target dice in succession, every roll must succeed

```
$ roll d8/4 d6/4 --roll
+---------+
|  STATS  |
+---------+
 d8
----
min: 1
max: 8
avg: 4.5

 d6
----
min: 1
max: 6
avg: 3.5

+---------------+
|  PERCENTAGES  |
+---------------+
d8 >= 4
-------
1: 1 of 8 (12.5%)
2: 1 of 8 (12.5%)
3: 1 of 8 (12.5%)
4: 1 of 8 (12.5%)
5: 1 of 8 (12.5%)
6: 1 of 8 (12.5%)
7: 1 of 8 (12.5%)
8: 1 of 8 (12.5%)
% of rolls >= 4: 5 of 8 (62.5%)

d6 >= 4
-------
1: 1 of 6 (16.7%)
2: 1 of 6 (16.7%)
3: 1 of 6 (16.7%)
4: 1 of 6 (16.7%)
5: 1 of 6 (16.7%)
6: 1 of 6 (16.7%)
% of rolls >= 4: 3 of 6 (50.0%)

+---------+
|  ROLLS  |
+---------+
  d8 = 8
target (>= 4): Succeeded

  d6 = 4
target (>= 4): Succeeded


+-----------------+
|  TOTAL SUCCESS  |
+-----------------+
%chance: 31.2%
Target rolls: Succeeded
```

# Example

###### Scenario

Player needs to first roll a 4 or higher using a `d10` or a `d6` wild dice, _and
then_ needs to roll a 6 or higher using a `d12` with a `+1` modifier, or a `d6`
wild dice.

```
$ roll d10,d6/4 1+d12,d6/6 --roll
+---------+
|  STATS  |
+---------+
 d10
-----
min: 1
max: 10
avg: 5.5

 d6
----
min: 1
max: 6
avg: 3.5

 1 + d12
---------
min: 2
max: 13
avg: 7.5

+---------------+
|  PERCENTAGES  |
+---------------+
d10,d6 >= 4
-----------
1: 15 of 60 (25.0%)
2: 15 of 60 (25.0%)
3: 15 of 60 (25.0%)
4: 15 of 60 (25.0%)
5: 15 of 60 (25.0%)
6: 15 of 60 (25.0%)
7: 6 of 60 (10.0%)
8: 6 of 60 (10.0%)
9: 6 of 60 (10.0%)
10: 6 of 60 (10.0%)
% of rolls >= 4: 51 of 60 (85.0%)

1+d12,d6 >= 6
-------------
1: 12 of 72 (16.7%)
2: 17 of 72 (23.6%)
3: 17 of 72 (23.6%)
4: 17 of 72 (23.6%)
5: 17 of 72 (23.6%)
6: 17 of 72 (23.6%)
7: 6 of 72 (8.3%)
8: 6 of 72 (8.3%)
9: 6 of 72 (8.3%)
10: 6 of 72 (8.3%)
11: 6 of 72 (8.3%)
12: 6 of 72 (8.3%)
13: 6 of 72 (8.3%)
% of rolls >= 6: 52 of 72 (72.2%)

+---------+
|  ROLLS  |
+---------+
d10,d6
------
  d10 = 3
  d6 = 5
target (>= 4): Succeeded

1+d12,d6
--------
  1 + d12 (10) = 11
  d6 = 2
target (>= 6): Succeeded


+-----------------+
|  TOTAL SUCCESS  |
+-----------------+
%chance: 61.4%
Target rolls: Succeeded
```
