"""
This file generates the transition matrix for a markov chain model of a
baseball game.

States
-------
| Number | Outs  | 1 | 2 | 3 | | Number | Outs  | 1 | 2 | 3 |
+--------+-------+---+---+---+-+--------+-------+---+---+---+
|   0    |   0   | N | N | N | |  8     |   1   | N | N | N |
|   1    |   0   | Y | N | N | |  9     |   1   | Y | N | N |
|   2    |   0   | N | Y | N | |  10    |   1   | N | Y | N |
|   3    |   0   | N | N | Y | |  11    |   1   | N | N | Y |
|   4    |   0   | Y | Y | N | |  12    |   1   | Y | Y | N |
|   5    |   0   | Y | N | Y | |  13    |   1   | Y | N | Y |
|   6    |   0   | N | Y | Y | |  14    |   1   | N | Y | Y |
|   7    |   0   | Y | Y | Y | |  15    |   1   | Y | Y | Y |

| Number | Outs  | 1 | 2 | 3 | | Number | Outs  | Runs |
+--------+-------+---+---+---+-+--------+-------+------+
|  16    |   2   | N | N | N | |   24   |   3   |   0  |
|  17    |   2   | Y | N | N | |   25   |   3   |   1  |
|  18    |   2   | N | Y | N | |   26   |   3   |   2  |
|  19    |   2   | N | N | Y | |   27   |   3   |   3  |
|  20    |   2   | Y | Y | N |
|  21    |   2   | Y | N | Y |
|  22    |   2   | N | Y | Y |
|  23    |   2   | Y | Y | Y |
 """
import numpy as np
import pandas as pd
import pprint

pp = pprint.PrettyPrinter(indent=4)

NumOfStates = 28
P = np.zeros((NumOfStates-4, NumOfStates))

# P[1, :] = [1, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

P1 = np.array(
      [[1,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
      [1,1,1,1,1,1,1,0,1,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
      [1,1,1,1,1,1,1,0,1,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
      [1,1,1,1,0,1,1,0,1,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,0,0,0,1,0,0,0],
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,0,0,0,1,0,0,0],
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,0,0,0,1,0,0,0],
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,0],
      [0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1,1,1,0,0,0,0,1,0,0,0],
      [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1,1,1,0,0,0,0,1,0,0,0],
      [0,0,0,0,0,0,0,0,1,1,1,1,0,1,1,0,1,1,1,1,0,0,0,0,1,0,0,0],
      [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,0],
      [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,0],
      [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,0],
      [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,0,0,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1,0,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1,0,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,1,0,1,1,0,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1]])

for i in range(NumOfStates):
    s = sum(P1[:,i])
    r = [np.random.random() for i in range(0,s+1)]
    s1 = sum(r)
    r = [ j/s1 for j in r ]
    a = 0
    for k in range(len(P[:,i])):
        if P1[k][i] == 1:
            P[k][i] = r[a]
            a = a + 1

A = np.zeros(NumOfStates)
A[0] = 1
limit = 10
for i in range(limit):
    print(i)
    B = P.dot(A)
    #print(B)
    print(np.argmax(B))
    print('\n')
    for j in range(len(B)):
        if j == np.argmax(B):
            A[j] = 1
        else:
            A[j] = 0
    #print(A)

#pp.pprint(P)
#print(P1[1])
pd.DataFrame(P).to_csv("out.csv", header=None, index=None)
