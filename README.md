`roll d6`

```
d6
--
min: 1
max: 6
avg: 3.5
--
1: 1 of 6 (16.7%)
2: 1 of 6 (16.7%)
3: 1 of 6 (16.7%)
4: 1 of 6 (16.7%)
5: 1 of 6 (16.7%)
6: 1 of 6 (16.7%)
--
random roll: 3
```

`roll 1+2d12`

```
1 + 2 × d12
-----------
min: 3
max: 25
avg: 14
-----------
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
-----------
random roll: 22
```

# Target check

###### 4 or higher succeeds on a d8

`roll d8 4`

```
d8
--
min: 1
max: 8
avg: 4.5
--
1: 1 of 8 (12.5%)
2: 1 of 8 (12.5%)
3: 1 of 8 (12.5%)
4: 1 of 8 (12.5%)
5: 1 of 8 (12.5%)
6: 1 of 8 (12.5%)
7: 1 of 8 (12.5%)
8: 1 of 8 (12.5%)
target >=4: 5 of 8 (62.5%)
--
random roll: 1
target: Failed
```

###### 4 or LOWER succeeds on a d8

`roll d8 -4`

```
d8
--
min: 1
max: 8
avg: 4.5
--
1: 1 of 8 (12.5%)
2: 1 of 8 (12.5%)
3: 1 of 8 (12.5%)
4: 1 of 8 (12.5%)
target <=4: 4 of 8 (50.0%)
--
random roll: 2
target: Succeeds
```

# Chance of either roll succeeding

`roll d8,d6 4`

```
d8
--
min: 1
max: 8
avg: 4.5
--
d6
--
min: 1
max: 6
avg: 3.5
--
1: 13 of 48 (27.1%)
2: 13 of 48 (27.1%)
3: 13 of 48 (27.1%)
4: 13 of 48 (27.1%)
5: 13 of 48 (27.1%)
6: 13 of 48 (27.1%)
7: 6 of 48 (12.5%)
8: 6 of 48 (12.5%)
target >=4: 39 of 48 (81.2%)
--
random rolls:
d8: 1
d6: 6
target: Succeeds
--
```

# Roll multiple target dice in succession, each roll must succeed

(weird, I know, but this was a feature I needed)

`roll d8 4 d6 4`

```
d8
--
min: 1
max: 8
avg: 4.5
--
target >=4: 5 of 8 (62.5%)
--
random roll: 3
target: Failed
d6
--
min: 1
max: 6
avg: 3.5
--
target >=4: 3 of 6 (50.0%)
--
random roll: 1
target: Failed
--------------------
Total success chance: 31.2%
```
