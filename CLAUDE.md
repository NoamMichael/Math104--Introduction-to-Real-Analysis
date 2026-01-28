# Math 104: Introduction to Real Analysis

## Repository Structure

```
math104/
├── CLAUDE.md              # This file - repo navigation guide
├── README.md              # Human-facing intro
├── Makefile               # Build system (make, make lec01, make clean)
├── Math104-Notes.pdf      # Compiled master notes (after running make)
├── hw/                    # Homework assignments
├── notes/
│   ├── CLAUDE.md          # Dictation workflow guide
│   ├── latex/             # LaTeX lecture notes (primary)
│   │   ├── master/        # Master document that combines all lectures
│   │   │   └── master.tex
│   │   ├── lec01/         # Lecture 1: Ordered sets, LUB property, fields
│   │   │   └── lec01.tex
│   │   ├── lec02/         # Lecture 2: Construction of R, properties, C, Euclidean spaces
│   │   │   └── lec02.tex
│   │   ├── lec03/         # Lecture 3: Set theory, countability
│   │   │   └── lec03.tex
│   │   └── temp/          # Template for new lectures
│   │       └── temp.tex
│   └── markdown/          # Markdown notes (if any)
```

## LaTeX Notes System

### Key Files

| File | Purpose |
|------|---------|
| `notes/latex/master/master.tex` | **Preamble + combined document**. Contains all packages, theorem environments, commands. Compiles all lectures into one PDF. |
| `notes/latex/temp/temp.tex` | **Template** for creating new lecture files. Copy this to start a new lecture. |
| `notes/latex/lecXX/lecXX.tex` | Individual lecture files using `subfiles` package. |

### How Subfiles Work

- **Master** (`master.tex`): Has full preamble + placeholder commands (`\lecturenum`, `\lecturedate`, `\lecturetopic`), uses `\subfile{../lecXX/lecXX}` to include lectures
- **Lectures** (`lecXX.tex`): Use `\documentclass[../master/master.tex]{subfiles}`, contain only content between `\begin{document}...\end{document}`
- Each lecture uses `\renewcommand` to set its topic/date/number (these appear in TOC)
- Each lecture can be compiled **standalone** (inherits master's preamble) or as **part of master**

### Adding a New Lecture

1. Create folder and copy template:
   ```bash
   mkdir notes/latex/lecXX
   cp notes/latex/temp/temp.tex notes/latex/lecXX/lecXX.tex
   ```
2. Edit the new file:
   - Update `\renewcommand{\lecturenum}{X}` with lecture number
   - Update `\renewcommand{\lecturedate}{...}` with date
   - Update `\renewcommand{\lecturetopic}{...}` with topic (this appears in TOC)
   - Fill in the `lecturesummary` (orange) with high-level lecture overview
   - Fill in the `summarybox` (baby blue) for each subsection
   - Add content
3. Add to master: uncomment/add `\subfile{../lecXX/lecXX}` in `master.tex`

**Important:** Use `\renewcommand` (not `\newcommand`) inside `\begin{document}` so the commands work when included in master.tex. The placeholders are defined in master.tex.

### Custom Commands Available

| Command | Output | Usage |
|---------|--------|-------|
| `\R`, `\N`, `\Z`, `\Q`, `\C` | Blackboard bold | Number sets |
| `\eps` | ε | Epsilon |
| `\defn{text}` | **red bold** + index entry | Highlight definitions (auto-adds to index) |
| `lecturesummary` environment | Orange box | Lecture overview (one per lecture) |
| `summarybox` environment | Baby blue box | Section summaries (one per subsection) |
| `notebox` environment | Light red box | Notes to reader about techniques |

### Theorem Environments

All numbered within sections: `theorem`, `lemma`, `proposition`, `corollary`, `definition`, `remark`

Unnumbered: `example`

### Compiling

```bash
# Build complete notes (outputs Math104-Notes.pdf in root)
make

# Build a specific lecture
make lec01

# Clean auxiliary files
make clean
```

The Makefile runs pdflatex, makeindex (for auto-generated index), then pdflatex again. Output goes to `Math104-Notes.pdf` in the repo root.

## Course Content

### Lecture 1: Ordered Sets, LUB Property, Fields
- Irrationality of √2 (motivation for gaps in Q)
- Sets, subsets, binary relations
- Partial orders, total orders, ordered sets
- Upper/lower bounds, supremum/infimum
- Least Upper Bound Property (LUBP) - key property of R
- Theorem: LUBP implies GLBP
- Groups, abelian groups, fields
- Construction of N → Z → Q
- Ordered fields

### Lecture 2: Construction of R
- Dedekind cuts
- Field operations on cuts, LUBP for cuts
- Embedding Q into R
- Archimedean property, density of Q in R
- Existence of nth roots
- Decimals, ternary expansions, Cantor set
- Complex numbers (C is not an ordered field)
- Euclidean spaces, inner products, norms, Cauchy-Schwarz

### Lecture 3: Set Theory & Countability
- Functions, images, preimages
- Injective, surjective, bijective
- Cardinality, finite, infinite, countable sets
- Z is countable, sequences
- Infinite subsets of countable sets are countable
- Unions/intersections, De Morgan's laws, distributive law
- Countable unions of countable sets are countable
- Q is countable (corollary)
- Cantor's diagonal argument: R is uncountable
- Algebraic vs transcendental numbers
- Cantor set is uncountable

## Conventions

- Each lecture is one `\section{}` with subsections as needed
- **Orange `lecturesummary`** at the start of each lecture (high-level overview of entire lecture)
- **Baby blue `summarybox`** at the start of each subsection (detailed section overview)
- Definitions use `\defn{}` for key terms (renders red bold)
- Theorem numbering: X.Y where X = section, Y = counter

### Lecture Structure

```latex
\section{Lecture X : Date}

\begin{lecturesummary}
\textbf{Lecture Overview:} [High-level summary of entire lecture...]
\end{lecturesummary}

\subsection{Topic Name}

\begin{summarybox}
\textbf{Section Overview:} [Detailed section summary...]
\end{summarybox}

% Content...
```
