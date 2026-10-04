# An Honest Attempt at P vs NP — Round 2

This continues [round 1](p-vs-np-attempt.md) with seven more lines of attack.
The labels are the same:

- ✅ **Proven**: a published, accepted theorem, or an exact computation in this repo.
- ❌ **Breaks**: where the argument fails, and why.

**Result: the question is still not settled.**

---

## 7. Attack: brute-force the truth for small n

**Idea.** Compute exactly how hard functions are, with no theory needed.

**Experiment** (`experiments/exact_circuit_size.py`). This is an exhaustive
search over all circuits made of 2-input gates, for every one of the 256
Boolean functions on 3 inputs. ✅ (Exact; it runs in about 5 seconds.)

| Minimum gates | Number of functions |
|---|---|
| 0 | 5 |
| 1 | 33 |
| 2 | 114 |
| 3 | 80 |
| 4 | 24 |

- The hardest 3-input functions need exactly 4 gates. Majority (MAJ3) is one
  of them. 3-bit parity needs only 2.
- For 4 inputs, Knuth computed the full distribution (TAOCP Vol. 4A, §7.1.2).
  The hardest functions need 7 gates. ✅

**Push it further.** Compute larger n until a pattern proves SAT is hard.

❌ **Breaks.**
1. **Size.** There are 2^(2ⁿ) functions on n inputs. At n = 6 that's about
   1.8 × 10¹⁹ functions. Exhaustive search dies almost immediately.
2. **Logic.** P vs NP is about how hardness *grows* as n → ∞. Every finite
   table is consistent with both P = NP and P ≠ NP, because a polynomial
   with huge constants can look exponential for any finite range of n. No
   finite computation, however large, can settle it.

---

## 8. Attack: monotone circuits (Razborov's approximation method)

**Idea.** Ban NOT gates first, prove a lower bound there, then try to add
NOT gates back.

**What it achieves.** ✅
- Razborov (1985): CLIQUE needs superpolynomial-size *monotone* circuits.
- Alon and Boppana (1987): strengthened this to exponential.

Since CLIQUE is NP-complete, this proves "NP-hard problems need huge
circuits" in the monotone world.

**Push it further.** Allow NOT gates.

❌ **Breaks.**
1. **Tardos (1988):** there is a monotone function computable in
   *polynomial time* that still needs exponential-size monotone circuits. ✅
   So monotone hardness says nothing about real hardness: banning NOT gates
   makes even easy problems look hard.
2. **Razborov (1989)** showed the approximation method, in its standard form,
   cannot prove strong lower bounds for general (non-monotone) circuits. ✅
   The method rules itself out.

---

## 9. Attack: formula lower bounds and the KRW conjecture

**Idea.** Formulas are circuits where each gate's output is used only once,
so the circuit is a tree. Proving lower bounds for formulas is easier.

**What it achieves.** ✅ The best formula lower bound for an explicit
function is about n³ (Andreev's function; Håstad 1998, Tal 2014), using
"shrinkage" under random restrictions.

The **Karchmer–Raz–Wigderson (KRW) conjecture** says that composing functions
makes formula depth add up. If true, it would prove P ⊄ NC¹ (some problem in
P has no polynomial-size formulas).

❌ **Breaks.**
1. KRW is unproven. Only special cases are known.
2. Even if it were proven, it would separate P from NC¹, not P from NP.
   Formulas are weaker than circuits, so formula lower bounds don't
   transfer to circuits.
3. Shrinkage arguments are natural in the Razborov–Rudich sense, so they
   cannot reach P/poly if standard cryptography is secure.

---

## 10. Attack: algebraic complexity and Geometric Complexity Theory

**Idea.** Replace Boolean circuits with polynomials over a field, and attack
Valiant's algebraic version of the problem: **VP vs VNP**, essentially
"determinant vs permanent." Then use algebraic geometry and representation
theory (Mulmuley and Sohoni's Geometric Complexity Theory) to find
*obstructions*: representation-theoretic certificates that the permanent
can't be written as a small determinant.

**What it achieves.** ✅
- Mignon and Ressayre (2004): writing the n×n permanent as a determinant needs
  matrices of size at least n²/2. The truth is believed to be exponential.
- GCT has produced deep structure theorems, but no superpolynomial separation.

❌ **Breaks.**
1. **No-go theorem:** Bürgisser, Ikenmeyer, and Panova (2016/2019) proved the
   simplest kind of GCT obstruction, "occurrence obstructions," **cannot
   exist** for permanent vs determinant. ✅ The original plan needs
   subtler multiplicity obstructions, which are far harder to find.
2. **Wrong question.** Even VP ≠ VNP would not directly prove P ≠ NP. It is
   the algebraic analogue, and the two aren't known to be equivalent.
3. The best algebraic bound (n²/2) is only quadratic. Superpolynomial is the
   whole fight, just as in round 1.

---

## 11. Attack: hardness magnification

**Idea.** This one is surprising. Oliveira and Santhanam (2018), McKay,
Murray, and Williams (2019), and others proved theorems of this form: ✅

> If some specific NP problem (for example a variant of MCSP, "does this
> truth table have a small circuit?") needs circuits of size n^(1+ε), then
> NP ⊄ P/poly, and so P ≠ NP.

So a *slightly superlinear* lower bound would be enough. We already have n³
formula lower bounds and 3.1n circuit lower bounds (round 1). Why not
apply them?

**Push it.** Apply the known n³ formula technique to the magnification target.

❌ **Breaks: the locality barrier.** Chen, Hirahara, Oliveira, Pich,
Rajgopal, and Santhanam (2020) showed that essentially all known lower-bound
techniques also work against circuits allowed to use small "oracle gates."
But the magnification target problems *do* have small circuits with such
gates. ✅ So current techniques provably cannot prove the needed bound for
exactly the problems where it would matter. Magnification moves the
difficulty to another spot; it doesn't remove it.

---

## 12. Attack: show it's unprovable (independence)

**Idea.** Prove that weak logical theories can't prove circuit lower bounds,
then strengthen the theory step by step.

**What it achieves.** ✅
- Razborov (1995): certain fragments of bounded arithmetic cannot prove
  superpolynomial circuit lower bounds for SAT, assuming strong
  pseudorandom generators exist.
- Pich and Santhanam (2021), among others: further unprovability results for
  weak theories.

❌ **Breaks.**
1. These theories are vastly weaker than ZFC, or even Peano arithmetic.
   Ordinary mathematics uses much more.
2. Gödel's second incompleteness theorem means ZFC can never prove "P vs NP
   is independent of ZFC" (see the earlier discussion). A proof would have
   to come from a strictly stronger theory.
3. The results are conditional on cryptographic assumptions that are
   themselves unproven, and that would in fact *imply* P ≠ NP.

---

## 13. Attack: P = NP via a polynomial-size linear program

**Idea.** Linear programming can be solved in polynomial time. Write TSP or
another NP-complete problem as a polynomial-size linear program, possibly
using extra variables (an "extended formulation"), and P = NP follows. Many
published "P = NP proofs" take exactly this approach.

**What it achieves.** ✅ It is impossible, and this is proven.
- Yannakakis (1988): *symmetric* polynomial-size LPs for TSP cannot exist.
- Fiorini, Massar, Pokutta, Tiwary, and de Wolf (2012): **no** polynomial-size
  extended formulation exists for the TSP polytope, symmetric or not. It
  needs exponential size unconditionally.
- Rothvoss (2014): even the *perfect matching* polytope, a problem in P,
  needs exponential-size LPs. So LP size isn't even a faithful measure of
  difficulty.
- Lee, Raghavendra, and Steurer (2015): the same holds for semidefinite
  programs (SDPs) for max-cut and related problems.
- Grigoriev (2001): the Sum-of-Squares hierarchy needs degree Ω(n) on certain
  parity (XOR) and knapsack instances.

❌ **Breaks.** Every "write it as one small convex program" approach to
P = NP is ruled out unconditionally. Getting a polynomial-time SAT algorithm
this way would require a method that isn't a compact LP or SDP formulation
of the problem's polytope. No one knows what that would look like.

---

## Updated ledger (rounds 1 + 2)

| # | Line of attack | Best proven result | Where it stops |
|---|---|---|---|
| 1 | Counting + diagonalization | Σ₂P ⊄ SIZE(nᵏ) | Relativization |
| 2 | Random restrictions | PARITY ∉ AC⁰ | Constant depth; natural proofs |
| 3 | Gate elimination | 3.1n | Linear by design |
| 4 | Algorithmic method | NQP ⊄ ACC⁰ | Needs fast general Circuit-SAT |
| 5 | Fast SAT solvers | DPLL/CDCL exponential on PHP | Would imply NP = coNP |
| 7 | Exact computation | All 3-input functions ≤ 4 gates | Finite data can't settle asymptotics |
| 8 | Monotone circuits | CLIQUE needs exponential monotone size | Tardos gap; method rules itself out |
| 9 | Formulas / KRW | n³ formula bound | Only reaches P vs NC¹; KRW open |
| 10 | Algebraic / GCT | perm vs det ≥ n²/2 | Occurrence obstructions don't exist |
| 11 | Hardness magnification | n^(1+ε) ⇒ P ≠ NP | Locality barrier |
| 12 | Independence | Unprovable in weak arithmetic | Far from ZFC; Gödel |
| 13 | Small LP/SDP for TSP | Exponential, unconditionally | Rules out a whole class of P = NP proofs |

**Conclusion.** After twelve lines of attack, there is still no proof. The
pattern is consistent: every technique either has a proven barrier or
reaches a bound far short of superpolynomial. What's missing is a new idea,
not more effort along these lines.

## References (new in round 2)

- Knuth. *The Art of Computer Programming, Vol. 4A,* §7.1.2. 2011.
- Razborov. *Lower Bounds on the Monotone Complexity of Some Boolean Functions.* 1985.
- Alon, Boppana. *The Monotone Circuit Complexity of Boolean Functions.* Combinatorica, 1987.
- Tardos. *The Gap Between Monotone and Non-Monotone Circuit Complexity Is Exponential.* Combinatorica, 1988.
- Razborov. *On the Method of Approximations.* STOC 1989.
- Håstad. *The Shrinkage Exponent of De Morgan Formulas Is 2.* SIAM J. Comput., 1998.
- Tal. *Shrinkage of De Morgan Formulae by Spectral Techniques.* FOCS 2014.
- Karchmer, Raz, Wigderson. *Super-Logarithmic Depth Lower Bounds via Direct Sum.* 1995.
- Mignon, Ressayre. *A Quadratic Bound for the Determinant and Permanent Problem.* IMRN, 2004.
- Bürgisser, Ikenmeyer, Panova. *No Occurrence Obstructions in Geometric Complexity Theory.* FOCS 2016 / JAMS 2019.
- Oliveira, Santhanam. *Hardness Magnification for Natural Problems.* FOCS 2018.
- McKay, Murray, Williams. *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations.* STOC 2019.
- Chen, Hirahara, Oliveira, Pich, Rajgopal, Santhanam. *Beyond Natural Proofs: Hardness Magnification and Locality.* ITCS 2020 / JACM 2022.
- Razborov. *Unprovability of Lower Bounds on Circuit Size in Certain Fragments of Bounded Arithmetic.* Izvestiya, 1995.
- Yannakakis. *Expressing Combinatorial Optimization Problems by Linear Programs.* STOC 1988.
- Fiorini, Massar, Pokutta, Tiwary, de Wolf. *Linear vs. Semidefinite Extended Formulations.* STOC 2012.
- Rothvoss. *The Matching Polytope Has Exponential Extension Complexity.* STOC 2014.
- Lee, Raghavendra, Steurer. *Lower Bounds on the Size of Semidefinite Programming Relaxations.* STOC 2015.
- Grigoriev. *Linear Lower Bound on Degrees of Positivstellensatz Calculus Proofs for the Parity.* 2001.
