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
