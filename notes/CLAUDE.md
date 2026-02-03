# Lecture Dictation Guide

## CRITICAL RULE

**ONLY transcribe what the user dictates.** Do NOT invent content, add theorems, fill in proofs, or generate material beyond what the user provides. Wait for dictation. The only exceptions are:
- When the user explicitly says "fill in" or "clean up my logic"
- When the user asks for a diagram or reader's note
- Formatting/LaTeX conversion of dictated content

If the user says "New Lecture: Topic", create the lecture file structure but DO NOT fill in any content. Wait for dictation.

## Workflow

1. **User provides rough notes** - markdown, shorthand, or verbal dictation
2. **Claude converts to LaTeX** - transcribing only what is dictated, following the style in existing lectures

## Input Formats Accepted

- Markdown with math shorthand: `f: A -> B`, `x in A`, `A int B`, `A U B`
- Incomplete sentences: "Def: countable if A~N"
- Verbal descriptions: "make a diagram showing..."
- Corrections: "clean up my logic", "fill in the definition of X"

## Conversion Rules

### Structure
- Each lecture gets `lecturesummary` (orange box) at the start
- Each subsection gets `summarybox` (baby blue box)
- Use `\defn{term}` for key definitions (renders red bold)
- Use `notebox` (light red) for notes to the reader about techniques

### Math Notation
| Input | Output |
|-------|--------|
| `->` | `\to` |
| `A int B` | `A \cap B` |
| `A U B` | `A \cup B` |
| `x in A` | `x \in A` |
| `A~B` | `A \sim B` (same cardinality) |
| `A^c` | `A^c` (complement) |
| `A \ B` | `A \setminus B` (set difference) |

### Environments
- **Definitions**: `\begin{definition}...\end{definition}`
- **Theorems**: `\begin{theorem}...\end{theorem}`
- **Proofs**: `\begin{proof}...\end{proof}`
- **Examples**: `\begin{example}...\end{example}` (unnumbered)
- **Remarks**: `\begin{remark}...\end{remark}`
- **Notes**: `\begin{notebox}...\end{notebox}` (for proof techniques, reader guidance)

### Auto-Generated Index
- Every `\defn{term}` automatically adds the term to the index with its page number
- No manual glossary maintenance needed
- Index appears at end of document as "Index of Definitions"

### Diagrams
- Use TikZ for diagrams (Venn diagrams, grids, number lines)
- Follow style from lec02 (Cantor set, Archimedean property diagrams)

## Commands

- "New section: [name]" - Create new `\subsection{}`
- "Make a note about X" - Add `notebox` explaining technique/concept
- "Clean up my logic" - Formalize informal proof sketch
- "Fill in [X]" - Complete partial definition or proof
- "Move X below Y" - Reorganize content
- "Run the makefile" - Compile to PDF

## After Session

Run `make` to compile. Output goes to `Math104-Notes.pdf` in repo root.
