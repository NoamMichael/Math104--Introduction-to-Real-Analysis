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
│   ├── latex/             # LaTeX lecture notes (primary)
│   │   ├── master/        # Master document that combines all lectures
│   │   │   └── master.tex
│   │   ├── lec01/         # Lecture 1: Ordered sets, LUB property, fields
│   │   │   └── lec01.tex
│   │   ├── lec02/         # Lecture 2: (empty)
│   │   │   └── lec02.tex
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
   - Fill in the `summarybox` with section overview
   - Add content
3. Add to master: uncomment/add `\subfile{../lecXX/lecXX}` in `master.tex`

**Important:** Use `\renewcommand` (not `\newcommand`) inside `\begin{document}` so the commands work when included in master.tex. The placeholders are defined in master.tex.

### Custom Commands Available

| Command | Output | Usage |
|---------|--------|-------|
| `\R`, `\N`, `\Z`, `\Q`, `\C` | Blackboard bold | Number sets |
| `\eps` | ε | Epsilon |
| `\defn{text}` | **red bold** | Highlight definitions |
| `summarybox` environment | Baby blue box | Section summaries |

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

The Makefile runs pdflatex twice (for TOC) and copies the output to `Math104-Notes.pdf` in the repo root.

## Course Content (Lecture 1)

**Section 1: Ordered Sets & LUB Property**
- Irrationality of √2 (motivation for gaps in Q)
- Sets, subsets, binary relations
- Partial orders, total orders, ordered sets
- Upper/lower bounds, supremum/infimum
- Least Upper Bound Property (LUBP) - key property of R
- Theorem: LUBP implies GLBP

**Section 1.1: Fields**
- Groups, abelian groups
- Fields (Q, R, C are fields; Z is not)
- Construction of N → Z → Q
- Equivalence relations
- Ordered fields

## Conventions

- Each lecture is one `\section{}` with subsections as needed
- Every section/subsection gets a baby blue `summarybox` at the top
- Definitions use `\defn{}` for key terms (renders red bold)
- Theorem numbering: X.Y where X = section, Y = counter
