# Math 104: Introduction to Real Analysis

Lecture notes for Math 104 (Introduction to Real Analysis) at UC Berkeley, Spring 2026.

## Contents

- **Lecture Notes** - LaTeX notes for each lecture, compilable individually or as a complete set

## Quick Start

### View the Notes

- **`Math104-Notes.pdf`** - All lectures combined (root directory)
- `notes/latex/lec01/lec01.pdf` - Lecture 1 standalone

### Compile from Source

Requires a LaTeX distribution (TeX Live, MiKTeX, etc.) and `make`.

```bash
# Build complete notes (outputs Math104-Notes.pdf in root)
make

# Build a specific lecture
make lec01

# Clean auxiliary files
make clean
```

## Lecture Topics

| Lecture | Date | Topic |
|---------|------|-------|
| 1 | Jan 20 | Ordered sets, least-upper-bound property, fields |
| 2 | Jan 22 | Construction of R, Archimedean property, Euclidean spaces |
| 3 | Jan 24 | Set theory, countability, Cantor's diagonal argument |
| 4 | Jan 29 | Topological spaces, metric topology, closed sets |


## Homework Structure

```
hw/
├── CLAUDE.md           # AI assistant guidelines for homework help
├── temp/               # Templates
│   └── hw_template.tex
├── hw1/
│   ├── assignment.txt  # Problem numbers (Rudin 1.1, 1.5, 1.9, 1.18)
│   ├── book_probs/     # Problem statements from textbook
│   ├── submission/     # Completed homework (hw1.tex, hw1.pdf)
│   └── explainers/     # Visual concept guides
│       ├── p1/         # Rationals + irrationals
│       ├── p2/         # Infimum/supremum duality
│       ├── p3/         # Lexicographic order on C
│       └── p4/         # Orthogonal vectors in R^k
└── hw2/
    ├── assignment.txt  # Problem numbers (Rudin 2.6, 2.22, 2.27, 2.29)
    ├── book_probs/
    ├── submission/
    └── explainers/
        ├── p1/         # Limit points, E' is closed
        ├── p2/         # Separable metric spaces
        ├── p3/         # Condensation points
        └── p4/         # Open sets as disjoint segments
```

### Explainers

Each problem has an optional **explainer** document with visual diagrams explaining the key concepts at an accessible level. These are study aids, not solutions.

## Notes Structure

Each lecture file can be compiled standalone or as part of the master document. The notes use:

- **Orange lecture summary boxes** at the start of each lecture (high-level overview)
- **Baby blue section summary boxes** at the start of each section (detailed key concepts)
- **Red bold text** for definitions of new terms
- Standard theorem environments (theorem, lemma, proposition, definition, example, etc.)

## Course Description

Real analysis is the rigorous study of calculus. Topics include:

- Construction of the real numbers and the least upper bound property
- Sequences, series, and convergence
- Continuity and differentiability
- The Riemann integral
- Sequences and series of functions

## Resources

- **Textbook**: Rudin, *Principles of Mathematical Analysis* (3rd ed.)

## License

These notes are for personal/educational use.
