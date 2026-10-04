# An Honest Attempt at P vs NP

**Result: the question is not settled.** This document pushes the main known
lines of attack as far as they go and marks exactly where each one stops.
Every step is labeled:

- ✅ **Proven** — a theorem with a published, accepted proof (or a full proof here).
- ❌ **Breaks** — the point where the argument fails, and why.

Nothing here should be read as a proof of P = NP or P ≠ NP.

---

## 0. The target

To prove **P ≠ NP**, it is enough to show that SAT has no polynomial-size
Boolean circuits (SAT ∉ P/poly), because every polynomial-time algorithm can be
unrolled into polynomial-size circuits. ✅ (Standard; Savage 1972.)

This is the stronger *circuit* version of the question, and it is the version
almost every serious attack uses: circuits are finite, combinatorial objects,
so we can count them, restrict them, and simplify them.

To prove **P = NP**, it is enough to give one polynomial-time algorithm for SAT.

Sections 1–4 attack P ≠ NP. Section 5 attacks P = NP.

---

## 1. Attack: counting (Shannon's argument)

**Claim.** Most Boolean functions on n inputs need circuits of size greater than
2ⁿ/(4n). ✅

**Proof.** A circuit with s gates (fan-in 2, any of the 16 two-input gate types)
is determined by, for each gate, its type (16 choices) and its two inputs (at
most (n+s)² choices). So there are at most (16(n+s)²)ˢ circuits of size s.

Take s = 2ⁿ/(4n). Then log₂ of the count is at most

  s · (4 + 2·log₂(n+s)) ≤ (2ⁿ/(4n)) · (4 + 2n) = 2ⁿ/2 + 2ⁿ/n.

There are 2^(2ⁿ) functions on n inputs. So the fraction computable by circuits of
size s is at most 2^(2ⁿ/2 + 2ⁿ/n − 2ⁿ), which goes to 0. ∎

**Push it further.** Can we make the hard function be SAT, or anything in NP?

Kannan (1982): for every fixed k, there is a language in Σ₂P that has no circuits
of size nᵏ. ✅ It works by searching, inside the polynomial hierarchy, for the
lexicographically first function that beats all size-nᵏ circuits.

❌ **Breaks, twice.**

1. **Wrong bound.** Kannan gives "not size nᵏ" for each *fixed* k. P ≠ NP needs
   "not size nᵏ for *any* k" at once. The diagonal search has to name the
   bound in advance, so it can't beat every polynomial at once.
2. **Wrong class, and it relativizes.** The hard language sits in Σ₂P, not
   NP, and the argument works the same with any oracle attached. By
   Baker–Gill–Solovay (1975), there are oracles A and B with Pᴬ = NPᴬ and
   Pᴮ ≠ NPᴮ. So **no relativizing argument can settle P vs NP**. Counting
   plus diagonalization is exactly that kind of argument.

---

## 2. Attack: random restrictions (Håstad's switching lemma)

**Idea.** Fix most input variables at random. A small circuit should collapse
to something trivial, while a hard function like PARITY stays hard (a
restricted parity is still parity on the remaining variables).

**Switching Lemma (Håstad 1986).** Let f be a k-CNF. Hit it with a random
restriction ρ that leaves each variable free with probability p and otherwise
sets it to 0 or 1 at random. Then

  Pr[ f|ρ cannot be written as a t-DNF ] ≤ (5pk)ᵗ. ✅

**Consequence.** PARITY on n bits needs depth-d AND/OR/NOT circuits of size
2^Ω(n^(1/(d−1))). ✅ Each round of restrictions swaps an AND layer and an OR
layer so they merge, cutting the depth by one. After d − 2 rounds, a small
circuit becomes a shallow decision tree, but parity on the remaining free
variables still depends on all of them. Contradiction.

**Push it further.** Apply the same idea to general circuits (unbounded depth),
or to SAT instead of parity.

❌ **Breaks.**

1. **Depth.** Each round costs one layer of depth. A polynomial-size circuit
   of depth log n or more absorbs every round. Nothing collapses.
2. **Natural proofs barrier (Razborov–Rudich 1994).** The property "stays
   complex under random restrictions" is
   - *constructive*: you can check it in time 2^O(n) from a truth table, and
   - *large*: a random function has it.

   Razborov and Rudich proved that if any such "natural" property worked
   against general polynomial-size circuits, it would distinguish
   pseudorandom functions from truly random ones. That would break
   cryptography widely believed to be secure. So if standard cryptography
   is sound, this whole style of argument **provably cannot** reach
   P/poly. ✅ (The barrier is a theorem; its hypothesis is a belief.)

---

## 3. Attack: gate elimination (attacking general circuits directly)

**Idea.** Work with fully general circuits. Fix one input variable cleverly so
that several gates become constant or redundant and can be deleted, while
the function stays in the same hard family. Repeat once per variable.

**What it achieves.** ✅
- Blum (1984): an explicit function needs circuits of size 3n − o(n).
- Find, Golovnev, Hirsch, Kulikov (2016): (3 + 1/86)n − o(n).
- Li and Yang (2022): 3.1n − o(n).

These are the **best known lower bounds against general circuits for any
explicit function**, even ones in NP or EXP.

**Push it further.**

❌ **Breaks.** Each step removes a *constant* number of gates per variable
fixed, and there are only n variables. So the method's bound is c·n for a
constant c. It is linear by design. P ≠ NP needs to beat *every* polynomial
nᵏ. The gap between 3.1n and superpolynomial is essentially the entire
problem. Golovnev, Kulikov, Smal, and Tamaki (2018) also show that natural
generalizations of gate elimination cannot get far past this.

---

## 4. Attack: the algorithmic method (Williams)

**Idea.** Turn the problem around: **faster algorithms imply lower bounds.**
If you can test whether a circuit from class C is satisfiable even slightly
faster than brute force (2ⁿ / superpolynomial), then NEXP has functions
outside C. Otherwise a nondeterministic time-hierarchy theorem would be
violated.

**What it achieves.** ✅
- Williams (2011): NEXP ⊄ ACC⁰ (constant-depth circuits with mod-m gates).
- Murray and Williams (2018): NQP ⊄ ACC⁰.

This was the first major circuit lower bound in about 20 years, and it
avoids all three barriers.

**Push it further.** Apply it to general circuits and to NP.

❌ **Breaks.**

1. **No fast algorithm.** It would need a satisfiability algorithm for
   *general* polynomial-size circuits that beats 2ⁿ by a superpolynomial
   factor. None is known, and finding one is a major open problem in its
   own right.
2. **Wrong class.** Even then, the hard function would be in NEXP
   (nondeterministic exponential time), not NP. Pulling the lower bound
   down from NEXP to NP would need another breakthrough.

---

## 5. Attack: P = NP (find a fast SAT algorithm)

**Idea.** Modern SAT solvers (DPLL and CDCL) handle industrial instances with
millions of variables. Maybe they're secretly polynomial-time.

**Experiment** (`experiments/php_dpll.py`, run in this repo). The
pigeonhole formula PHP(n+1 → n) says n+1 pigeons fit into n holes with at
most one pigeon per hole. It is always false.

| n | variables | clauses | DPLL search nodes |
|---|-----------|---------|-------------------|
| 3 | 12 | 22 | 11 |
| 5 | 30 | 81 | 239 |
| 7 | 56 | 204 | 10,079 |
| 9 | 90 | 415 | 725,759 |

The node count is exactly 2·n! − 1. That's **factorial growth on a formula
with only 90 variables.**

**Is this just a weak solver?** No. ✅
- Haken (1985): every *resolution* refutation of PHP needs size 2^Ω(n).
- Every run of DPLL or CDCL on an unsatisfiable formula is a resolution
  refutation (Beame, Kautz, Sabharwal 2004; Pipatsrisawat and Darwiche 2011).

So **every DPLL/CDCL solver, with any heuristics, takes exponential time on
pigeonhole formulas.** This is a real, unconditional theorem.

**Push it further.** Use a stronger proof system. Extended Frege proofs handle
pigeonhole in polynomial size, for example.

❌ **Breaks.**
- A polynomial-time SAT algorithm would make *every* unsatisfiable formula
  have short certificates in some efficient proof system. That means NP = coNP
  (Cook–Reckhow 1979), itself a famous open problem. Proving lower bounds
  for strong proof systems like Frege is open too.
- No known algorithm beats the Exponential Time Hypothesis, and the best
  general 3-SAT algorithms still run in about 1.3ⁿ time.
- Every candidate polynomial-time SAT algorithm published so far has been
  refuted, usually with an explicit family of hard instances.

---

## 6. Ledger

| Line of attack | Best proven result | Where it stops | Barrier |
|---|---|---|---|
| Counting + diagonalization | Σ₂P ⊄ SIZE(nᵏ) for each fixed k | Can't beat all polynomials at once; class too high | Relativization |
| Random restrictions | PARITY ∉ AC⁰ (exponential) | Constant depth only | Natural proofs |
| Gate elimination | 3.1n for general circuits | Linear by design | Inherent to the method |
| Algorithmic method | NQP ⊄ ACC⁰ | Needs fast general Circuit-SAT; class is NEXP/NQP | None known, but stuck |
| Fast SAT (P = NP) | DPLL/CDCL are exponential on PHP | Would imply NP = coNP | Proof complexity |

**Conclusion.** None of the four main lines of attack on P ≠ NP can get there
in its current form. Three hit proven barriers, and one is stuck on an open
algorithmic problem. The P = NP direction runs into unconditional exponential
lower bounds for every known solver family. A resolution needs a new idea that
is non-relativizing, non-natural, and non-algebrizing. Nobody has one, and
this document doesn't claim to.

## References

- Baker, Gill, Solovay. *Relativizations of the P =? NP Question.* SIAM J. Comput., 1975.
- Haken. *The Intractability of Resolution.* Theor. Comput. Sci., 1985.
- Håstad. *Almost Optimal Lower Bounds for Small Depth Circuits.* STOC 1986.
- Kannan. *Circuit-Size Lower Bounds and Non-Reducibility to Sparse Sets.* Inf. Control, 1982.
- Razborov, Rudich. *Natural Proofs.* JCSS, 1997 (STOC 1994).
- Aaronson, Wigderson. *Algebrization: A New Barrier in Complexity Theory.* STOC 2008.
- Williams. *Nonuniform ACC Circuit Lower Bounds.* CCC 2011 / JACM 2014.
- Murray, Williams. *Circuit Lower Bounds for Nondeterministic Quasi-Polytime.* STOC 2018.
- Find, Golovnev, Hirsch, Kulikov. *A Better-Than-3n Lower Bound for the Circuit Complexity of an Explicit Function.* FOCS 2016.
- Li, Yang. *3.1n − o(n) Circuit Lower Bounds for Explicit Functions.* STOC 2022.
- Cook, Reckhow. *The Relative Efficiency of Propositional Proof Systems.* JSL, 1979.
- Pipatsrisawat, Darwiche. *On the Power of Clause-Learning SAT Solvers as Resolution Engines.* AIJ, 2011.
