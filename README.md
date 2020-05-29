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

+----------------+
|  RANDOM ROLLS  |
+----------------+
- d6: 1
```

```
$ roll 1+2d12

+---------+
|  STATS  |
+---------+
 1 + 2 × d12
-------------
min: 3
max: 25
avg: 14

+---------------+
|  PERCENTAGES  |
+---------------+
1+2d12
------
3: 1 of 144 (0.7%)
4: 2 of 144 (1.4%)
5: 3 of 144 (2.1%)
6: 4 of 144 (2.8%)
7: 5 of 144 (3.5%)
8: 6 of 144 (4.2%)
9: 7 of 144 (4.9%)
10: 8 of 144 (5.6%)
11: 9 of 144 (6.2%)
12: 10 of 144 (6.9%)
13: 11 of 144 (7.6%)
14: 12 of 144 (8.3%)
15: 11 of 144 (7.6%)
16: 10 of 144 (6.9%)
17: 9 of 144 (6.2%)
18: 8 of 144 (5.6%)
19: 7 of 144 (4.9%)
20: 6 of 144 (4.2%)
21: 5 of 144 (3.5%)
22: 4 of 144 (2.8%)
23: 3 of 144 (2.1%)
24: 2 of 144 (1.4%)
25: 1 of 144 (0.7%)

+----------------+
|  RANDOM ROLLS  |
+----------------+
- 1 + 2 × d12: 15
```

# Target check

###### 4 or higher succeeds on a d8

```
$ roll d8/4

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
d8
--
1: 1 of 8 (12.5%)
2: 1 of 8 (12.5%)
3: 1 of 8 (12.5%)
4: 1 of 8 (12.5%)
5: 1 of 8 (12.5%)
6: 1 of 8 (12.5%)
7: 1 of 8 (12.5%)
8: 1 of 8 (12.5%)

+-----------+
|  TARGETS  |
+-----------+
- d8: 5
%rolls >=4: 5 of 8 (62.5%)
target: Succeeds
```

###### 4 or LOWER succeeds on a d8

```
$ roll d8/-4

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
d8
--
1: 1 of 8 (12.5%)
2: 1 of 8 (12.5%)
3: 1 of 8 (12.5%)
4: 1 of 8 (12.5%)
5: 1 of 8 (12.5%)
6: 1 of 8 (12.5%)
7: 1 of 8 (12.5%)
8: 1 of 8 (12.5%)

+-----------+
|  TARGETS  |
+-----------+
- d8: 3
%rolls <=4: 4 of 8 (50.0%)
target: Succeeds
```

# Chance of either roll succeeding

```
$ roll d8,d6/+4

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
d8,d6
-----
1: 13 of 48 (27.1%)
2: 13 of 48 (27.1%)
3: 13 of 48 (27.1%)
4: 13 of 48 (27.1%)
5: 13 of 48 (27.1%)
6: 13 of 48 (27.1%)
7: 6 of 48 (12.5%)
8: 6 of 48 (12.5%)

+----------------+
|  TARGET ROLLS  |
+----------------+
d8,d6
-----
- d8: 2
- d6: 4
%rolls >=4: 39 of 48 (81.2%)
target: Succeeds
```

# Roll multiple target dice in succession, every roll must succeed

```
$ roll d8/4 d6/4

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
d8
--
1: 1 of 8 (12.5%)
2: 1 of 8 (12.5%)
3: 1 of 8 (12.5%)
4: 1 of 8 (12.5%)
5: 1 of 8 (12.5%)
6: 1 of 8 (12.5%)
7: 1 of 8 (12.5%)
8: 1 of 8 (12.5%)

d6
--
1: 1 of 6 (16.7%)
2: 1 of 6 (16.7%)
3: 1 of 6 (16.7%)
4: 1 of 6 (16.7%)
5: 1 of 6 (16.7%)
6: 1 of 6 (16.7%)

+----------------+
|  TARGET ROLLS  |
+----------------+
- d8: 8
%rolls >=4: 5 of 8 (62.5%)
target: Succeeded
- d6: 1
%rolls >=4: 3 of 6 (50.0%)
target: Failed

+-----------------+
|  TOTAL SUCCESS  |
+-----------------+
%chance: 31.2%
Target rolls: Failed
```

# Example

###### Scenario

Player needs to first roll a 4 or higher using a `d10` or a `d6` wild dice, _and
then_ needs to roll a 6 or higher using a `d12` with a `+1` modifier, or a `d6`
wild dice.

```
$ roll d10,d6/4 1+d12,d6/6

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
d10,d6
------
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

1+d12,d6
--------
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

+----------------+
|  TARGET ROLLS  |
+----------------+
d10,d6
------
- d10: 6
- d6: 3
%rolls >=4: 51 of 60 (85.0%)
target: Succeeded
1+d12,d6
--------
- 1 + d12: 12
- d6: 2
%rolls >=6: 52 of 72 (72.2%)
target: Succeeded

+-----------------+
|  TOTAL SUCCESS  |
+-----------------+
%chance: 61.4%
Target rolls: Succeeded
```
