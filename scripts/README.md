# PDF to Markdown Converter

OCR-powered PDF to Markdown converter with book/chapter navigation support.

## Installation

### System Dependencies

```bash
sudo apt install tesseract-ocr poppler-utils
```

### Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Convert to directory structure (recommended for books)
./pdf2md textbook.pdf -o output/

# Convert to single markdown file
./pdf2md textbook.pdf --single-file -o book.md
```

### Output Formats

**Directory Structure** (default) - Best for large books:
```
output/
├── README.md           # Table of contents with links
├── chapter-01/
│   ├── README.md       # Chapter overview with page links
│   ├── page-001.md
│   ├── page-002.md
│   └── ...
├── chapter-02/
│   └── ...
```

**Single File** (`--single-file`) - Best for smaller documents:
- One markdown file with all content
- TOC with anchor links
- Page numbers as headers

### Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Output file or directory (required) |
| `--single-file` | Output as single markdown file |
| `--ocr-only` | Force OCR even for digital PDFs |
| `--no-ocr` | Disable OCR (native extraction only) |
| `--lang LANG` | Tesseract language (default: `eng`) |
| `--dpi DPI` | OCR resolution (default: 300) |
| `--no-chapters` | Skip chapter detection |
| `--start-page N` | Start from page N |
| `--end-page N` | End at page N |
| `-v, --verbose` | Show progress |

### Examples

```bash
# Book with chapter detection
./pdf2md textbook.pdf -o textbook-md/ -v

# Scanned document with multiple languages
./pdf2md scanned.pdf --ocr-only --lang eng+deu -o output/

# Specific page range
./pdf2md book.pdf --start-page 10 --end-page 50 -o chapter1/

# Skip chapter detection (flat structure)
./pdf2md manual.pdf --no-chapters -o manual-md/
```

## Chapter Detection

The script automatically detects chapters using patterns like:
- `Chapter 1: Introduction`
- `CHAPTER I`
- `Part 1`
- `1. Section Name`
- `§1 Topic`

Sections detected:
- `1.1 Subsection`
- `Section 1: Name`

To disable: use `--no-chapters`

## Tips

1. **For scanned PDFs**: Use `--ocr-only` to force OCR
2. **For better OCR**: Increase `--dpi` (400-600 for poor quality scans)
3. **Multiple languages**: Use `--lang eng+fra` for mixed-language documents
4. **Large books**: Directory structure is easier to navigate
5. **Searchability**: Single file is better for text search
