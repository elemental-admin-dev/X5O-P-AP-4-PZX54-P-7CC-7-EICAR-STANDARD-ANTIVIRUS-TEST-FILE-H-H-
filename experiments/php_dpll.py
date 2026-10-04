"""Count DPLL search nodes on the pigeonhole formulas PHP(n+1 -> n).

PHP says n+1 pigeons fit in n holes with no two sharing a hole. It is
always unsatisfiable, yet Haken (1985) proved every resolution refutation
of it has size 2^Omega(n). DPLL and CDCL runs are resolution refutations,
so this growth is forced, not a weakness of this particular solver.
"""
import sys

sys.setrecursionlimit(10000)


def php(n):
    var = lambda p, h: p * n + h + 1  # pigeon p in hole h
    clauses = [[var(p, h) for h in range(n)] for p in range(n + 1)]
    for h in range(n):
        for p in range(n + 1):
            for q in range(p + 1, n + 1):
                clauses.append([-var(p, h), -var(q, h)])
    return clauses


def dpll(clauses, assignment, stats):
    stats["nodes"] += 1
    while True:
        simplified = []
        unit = None
        for c in clauses:
            if any(assignment.get(abs(l)) == (l > 0) for l in c):
                continue
            rest = [l for l in c if abs(l) not in assignment]
            if not rest:
                return False
            if len(rest) == 1 and unit is None:
                unit = rest[0]
            simplified.append(rest)
        clauses = simplified
        if unit is None:
            break
        assignment = {**assignment, abs(unit): unit > 0}
    if not clauses:
        return True
    lit = clauses[0][0]
    for value in (lit > 0, lit < 0):
        if dpll(clauses, {**assignment, abs(lit): value}, stats):
            return True
    return False


if __name__ == "__main__":
    print(f"{'n':>2} {'vars':>5} {'clauses':>8} {'DPLL nodes':>11}")
    for n in range(1, 10):
        f = php(n)
        stats = {"nodes": 0}
        assert not dpll(f, {}, stats)
        print(f"{n:>2} {n * (n + 1):>5} {len(f):>8} {stats['nodes']:>11}")
