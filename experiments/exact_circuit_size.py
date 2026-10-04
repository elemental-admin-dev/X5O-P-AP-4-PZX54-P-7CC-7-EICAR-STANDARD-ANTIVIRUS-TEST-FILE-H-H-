"""Exact minimum circuit size of every Boolean function on n = 3 inputs.

Basis: all 2-input gates (B2). Size = number of gates. Exhaustive search,
so every number printed is a theorem for that tiny n, not an estimate.
Shannon's counting argument says that for large n almost every function
needs about 2^n / n gates; here we can see the exact distribution.
"""
from collections import Counter

N = 3
MASK = (1 << (1 << N)) - 1
INPUTS = []
for i in range(N):
    t = 0
    for row in range(1 << N):
        if row >> i & 1:
            t |= 1 << row
    INPUTS.append(t)

# The 10 binary operations that depend on both arguments.
OPS = [
    lambda a, b: a & b, lambda a, b: a & ~b, lambda a, b: ~a & b,
    lambda a, b: ~(a | b), lambda a, b: a | b, lambda a, b: a | ~b,
    lambda a, b: ~a | b, lambda a, b: ~(a & b), lambda a, b: a ^ b,
    lambda a, b: ~(a ^ b),
]

# Constants and inputs are free; NOT x costs one (unary) gate. Gates that
# feed other gates never need explicit NOTs, because OPS is closed under
# negating either input or the output.
best = {0: 0, MASK: 0}
for t in INPUTS:
    best[t] = 0
    best[~t & MASK] = 1


def search(nodes, size, limit):
    if size == limit:
        return
    k = len(nodes)
    for i in range(k):
        for j in range(i + 1, k):
            a, b = nodes[i], nodes[j]
            for op in OPS:
                t = op(a, b) & MASK
                if t in nodes or t == 0 or t == MASK:
                    continue
                if best.get(t, 99) > size + 1:
                    best[t] = size + 1
                nodes.append(t)
                search(nodes, size + 1, limit)
                nodes.pop()


if __name__ == "__main__":
    for limit in range(1, 6):
        search(list(INPUTS), 0, limit)
        if len(best) == 1 << (1 << N):
            break
    dist = Counter(best.values())
    print(f"functions on {N} inputs: {len(best)} of {1 << (1 << N)}")
    for s in sorted(dist):
        print(f"  size {s}: {dist[s]:>3} functions")
    hardest = [t for t, s in best.items() if s == max(dist)]
    print("hardest truth tables:", [format(t, "08b") for t in hardest])
    maj = 0
    for row in range(8):
        if bin(row).count("1") >= 2:
            maj |= 1 << row
    par = INPUTS[0] ^ INPUTS[1] ^ INPUTS[2]
    print("MAJ3 size:", best[maj], "| PARITY3 size:", best[par])
