'''The A* search algorithm, where the state is a set of points, and the heuristic is the maximum of the minimum distances from the starting vertices
to the closest endpoint. Before running the algorithm, it will calculate the minimum distances from every non-wall point to the nearest endpoint.
I will use the BFS algorithm, but instead of a queue, I will use a heap - a priority queue with the priority based on the minimal value of f(n)=g(n)+h(n).'''

from cmath import inf
import time
from dataclasses import dataclass, field
from typing import Any
from queue import PriorityQueue


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


start = time.time()


def finish(w, D):
    for e in w:
        if e not in D:
            return False
    return True


# read of inputs
file = open('zad_input.txt', "r")
if file:
    tab = file.readlines()
for g in range(0, len(tab)):
    tab[g] = tab[g].rstrip()
B = set()
g = set()
s = set()
n = len(tab)
m = len(tab[0])
min_init = {}


def letter(l):
    U = [-1, 0]
    L = [0, -1]
    R = [0, 1]
    D = [1, 0]
    if l == U:
        return str("U")
    elif l == L:
        return str("L")
    elif l == R:
        return str("R")
    elif l == D:
        return str("D")
    else:
        return l


for i in range(0, n):
    for j in range(0, m):
        if tab[i][j] == '#':
            s.add((i, j))
        elif tab[i][j] == 'G':
            g.add((i, j))
        elif tab[i][j] == 'B':
            B.add((i, j))
            g.add((i, j))
        elif tab[i][j] == 'S':
            B.add((i, j))


def update(B, move, amount, s):
    h = [1, 1]
    res = set()
    addset = set()
    for i in range(0, amount):
        res = set()
        addset = set()
        for j in B:
            h[0], h[1] = j
            if (move[0]+h[0], move[1]+h[1]) not in s and move[0]+h[0] >= 0 and move[0]+h[0] < n and move[1]+h[1] >= 0 and move[1]+h[1] < m:
                res.add((move[0]+h[0], move[1]+h[1]))
            else:
                addset.add(j)

        B = res.union(addset)
    return B


def col(i, a, b, c, d):
    if i == 0:
        return a
    elif i == 1:
        return b
    elif i == 2:
        return c
    else:
        return d


def lit(i):
    if i == 0:
        return [-1, 0]
    elif i == 1:
        return [0, -1]
    elif i == 2:
        return [1, 0]
    else:
        return [0, 1]


def h(s, g, v):
    queue = []
    idp = 0
    idk = 0
    visited = {}
    visited[tuple(v)] = 1
    min = {}
    for i in g:
        min[i] = ("", 100000000)
    maxx = ("", 100000000000)
    queue.append(("", v))
    while idp != idk+1:
        w = queue[idp]
        U = [-1, 0]
        L = [0, -1]
        R = [0, 1]
        D = [1, 0]
        a1 = update(w[1], U, 1, s)
        a2 = update(w[1], L, 1, s)
        a3 = update(w[1], D, 1, s)
        a4 = update(w[1], R, 1, s)
        for bb in range(0, 4):
            for gg in col(bb, a1, a2, a3, a4):
                if gg in g:
                    for u in w[1]:
                        if min[gg][1] > len(w[0])+1:
                            min[gg] = (w[0]+letter(lit(bb)), len(w[0])+1)

        if visited.get(tuple(a1)) == None or visited.get(tuple(a1)) != 1:
            queue.append((w[0]+"U", a1))
            visited[tuple(a1)] = 1
            idk += 1

        if visited.get(tuple(a2)) == None or visited.get(tuple(a2)) != 1:
            queue.append((w[0]+"L", a2))
            visited[tuple(a2)] = 1
            idk += 1
        if visited.get(tuple(a3)) == None or visited.get(tuple(a3)) != 1:
            queue.append((w[0]+"D", a3))
            visited[tuple(a3)] = 1
            idk += 1

        if visited.get(tuple(a4)) == None or visited.get(tuple(a4)) != 1:
            queue.append((w[0]+"R", a4))
            visited[tuple(a4)] = 1
            idk += 1
        idp += 1
    for goal in g:
        if maxx[1] > min[goal][1]:
            maxx = min[goal]
    return maxx


def upd(K, move, a, v):
    sett = set(map(lambda x: min_init[x][1], a))
    max1 = max(sett)
    K.put((v[0]+1+max1, (v[0]+1, max1, a, v[3]+move)))
    return K


def min_dys(B, s, g):
    for i in range(0, n):
        for j in range(0, m):
            if (i, j) not in s:
                if (i, j) in g:
                    min_init[(i, j)] = ("", 0)
                else:
                    min_init[(i, j)] = h(s, g, {(i, j)})


min_dys(B, s, g)
sett = set(map(lambda x: min_init[x][1], B))
max1 = max(sett)
visited = set()
q = PriorityQueue()
q.put((max1, (0, max1, B, "")))


def print_state(B, g, s, n, m):
    for i in range(0, n):
        for j in range(0, m):
            if (i, j) in s:
                print("#", end='')
            elif (i, j) in B:
                print("B", end='')
            elif (i, j) in g:
                print("G", end='')
            else:
                print(" ", end='')
        print()


start = 1


def BFS(B, g, s, q, start):
    while start == 1 or not q.empty():
        w = q.get()
        start = 0
        if finish(w[1][2], g):
            return w[1][3], w[1][2]
        else:
            U = [-1, 0]
            L = [0, -1]
            R = [0, 1]
            D = [1, 0]
            a1 = update(w[1][2], U, 1, s)
            a2 = update(w[1][2], L, 1, s)
            a3 = update(w[1][2], D, 1, s)
            a4 = update(w[1][2], R, 1, s)
            if frozenset(a1) not in visited:
                q = upd(q, "U", a1, w[1])
                visited.add(frozenset(a1))
            if frozenset(a2) not in visited:
                q = upd(q, "L", a2, w[1])
                visited.add(frozenset(a2))
            if frozenset(a3) not in visited:
                q = upd(q, "D", a3, w[1])
                visited.add(frozenset(a3))
            if frozenset(a4) not in visited:
                q = upd(q, "R", a4, w[1])
                visited.add(frozenset(a4))


# saving the results to an output file
file_2 = open("zad_output.txt", "w")
result = BFS((B, ""), g, s, q, start)
file_2.write(result[0])
file_2.close()
end = time.time()
print(end - start)
